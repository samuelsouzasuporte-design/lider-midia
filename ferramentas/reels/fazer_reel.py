"""Gera um Reels da Líder (1080x1920, ~35s) a partir de clipes em videos/ e um JSON.

Uso: python3 ferramentas/reels/fazer_reel.py reel.json saida.mp4
Demora ~10 min (2 CPUs). Rode a partir da raiz do repositório.

reel.json:
{
  "musica_seed": 3,                         # muda a música (acordes/tom); use um número diferente a cada Reels
  "gancho": ["TUDO PARA O SEU", "CARRO E MOTO"],
  "tema1": ["PNEUS", "para carros e motos"],
  "tema2": ["BATERIAS", "as melhores marcas"],
  "pausa": ["ESTOQUE", "COMPLETO", "pronta entrega"],
  "palavras": ["QUALIDADE", "VARIEDADE", "CONFIANÇA", "VEM PRA LÍDER!"],
  "segmentos": [  # EXATAMENTE 20: [arquivo em videos/, inicio_s, velocidade]
     1 abertura (3,9s, plano bonito, velocidade ~1.0),
     4 do tema 1 (1,9s cada, ~1.3), 4 do tema 2 (1,9s cada, ~1.3),
     2 da pausa (1,9s cada, ~1.0), 8 rápidos (0,97s cada, ~1.4),
     1 fundo da tela final (4,6s, ~0.8)
  ]
}
Confira que inicio + duração*velocidade cabe no clipe (ffprobe). Evite trechos borrados.
"""
import cv2, numpy as np, subprocess, sys, os, json, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FONTES = os.path.join(RAIZ, 'ferramentas', 'fontes')
FB = os.path.join(FONTES, 'Poppins-BoldItalic.ttf')
FM = os.path.join(FONTES, 'Poppins-MediumItalic.ttf')
W, H, FPS = 1080, 1920, 30
BEAT = 60 / 124
BAR = 4 * BEAT
BEATS = [8] + [4] * 8 + [4, 4] + [2] * 8 + [9.5]
YEL = (255, 184, 0)
T_DROP1, T_BRK, T_DROP2, T_END = 2 * BAR, 10 * BAR, 12 * BAR, 16 * BAR

def bounds():
    out, t = [], 0.0
    for b in BEATS:
        a = round(t * FPS); t += b * BEAT; out.append((a, round(t * FPS)))
    return out

def preparar(args):
    i, (arq, ss, sp), tmp = args
    a, b = bounds()[i]; nf = b - a
    srcdur = nf / FPS * sp + 0.6
    src = os.path.join(RAIZ, 'videos', arq)
    trf = f'{tmp}/{i:02d}.trf'; out = f'{tmp}/{i:02d}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(srcdur), '-i', src,
                    '-vf', f'vidstabdetect=shakiness=6:accuracy=12:result={trf}', '-f', 'null', '-'], check=True)
    vf = (f'vidstabtransform=input={trf}:smoothing=18:optzoom=1:interpol=bicubic,setpts=(PTS-STARTPTS)/{sp},fps={FPS},'
          "eq=contrast=1.07:saturation=1.22:gamma=0.97,curves=all='0/0 0.25/0.22 0.75/0.79 1/1',unsharp=5:5:0.6,format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(srcdur), '-i', src, '-vf', vf,
                    '-frames:v', str(nf), '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', out], check=True)
    return i

# ---------- texto ----------
def ease_out(x): x = np.clip(x, 0, 1); return 1 - (1 - x) ** 3
def ease_in(x): x = np.clip(x, 0, 1); return x ** 3
def back_out(x):
    x = np.clip(x, 0, 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def text_img(txt, size, color=(255, 255, 255), font=FB):
    f = ImageFont.truetype(font, size)
    l, t, r, b = f.getbbox(txt); pad = 40
    im = Image.new('RGBA', (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((pad - l + 4, pad - t + 8), txt, font=f, fill=(0, 0, 0, 170))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(im).text((pad - l, pad - t), txt, font=f, fill=color + (255,))
    return im

def fit(txt, size, maxw, color=(255, 255, 255), font=FB):
    im = text_img(txt, size, color, font)
    while im.width > maxw and size > 40:
        size -= 6; im = text_img(txt, size, color, font)
    return im

def label_img(big, small):
    fb = ImageFont.truetype(FB, 120); l, t, r, b = fb.getbbox(big)
    padx, pady, slant = 50, 34, 40
    bw, bh = (r - l) + 2 * padx + slant, (b - t) + 2 * pady
    sub = text_img(small, 58)
    im = Image.new('RGBA', (max(bw, sub.width) + 60, bh + sub.height + 30), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(slant + 10, 18), (bw + 10, 18), (bw - slant + 10, bh + 18), (10, bh + 18)], fill=(0, 0, 0, 140))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.polygon([(slant, 0), (bw, 0), (bw - slant, bh), (0, bh)], fill=YEL + (255,))
    d.text((padx + slant / 2 - l, pady - t), big, font=fb, fill=(15, 15, 15, 255))
    im.alpha_composite(sub, (10, bh - 10))
    return im

def glow(im, r=18, a=150):
    pad = 50
    g = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    m = Image.new('RGBA', g.size, (0, 0, 0, 0)); m.paste((0, 0, 0, a), (pad, pad), im.split()[3])
    g = Image.alpha_composite(g, m.filter(ImageFilter.GaussianBlur(r))); g.alpha_composite(im, (pad, pad)); return g

def comp(frame, im, cx, cy, alpha=1.0, s=1.0):
    if alpha <= 0.01: return
    if abs(s - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32) / 255.0
    rgb, a = arr[..., :3][..., ::-1], arr[..., 3:4] * alpha
    x0 = int(cx - im.width / 2); y0 = int(cy - im.height / 2)
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + im.width), min(H, y0 + im.height)
    if fx1 <= fx0 or fy1 <= fy0: return
    sx, sy = fx0 - x0, fy0 - y0
    sub = frame[fy0:fy1, fx0:fx1]
    rr = rgb[sy:sy + fy1 - fy0, sx:sx + fx1 - fx0]; aa = a[sy:sy + fy1 - fy0, sx:sx + fx1 - fx0]
    sub[:] = sub * (1 - aa) + rr * aa

def card_final():
    def line(txt, size, color=(255, 255, 255), font=FM): return text_img(txt, size, color, font)
    addr = Image.new('RGBA', (900, 160), (0, 0, 0, 0))
    l1 = line('Rua Deolino Barreto, 860 - Centro', 50); l2 = line('Crateús / CE', 50)
    pin = Image.new('RGBA', (90, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(pin)
    d.ellipse((15, 10, 75, 70), fill=YEL + (255,)); d.polygon([(19, 52), (71, 52), (45, 100)], fill=YEL + (255,))
    d.ellipse((33, 28, 57, 52), fill=(20, 20, 20, 255))
    addr = Image.new('RGBA', (90 + max(l1.width, l2.width), l1.height + l2.height - 50), (0, 0, 0, 0))
    addr.alpha_composite(pin, (10, (addr.height - 120) // 2)); addr.alpha_composite(l1, (90, 0)); addr.alpha_composite(l2, (90, l1.height - 50))
    t = text_img('(88) 9.8865-5130', 66)
    ic = Image.new('RGBA', (110, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    G = (37, 211, 102, 255); Wt = (255, 255, 255, 255)
    d.ellipse((5, 5, 105, 105), fill=G); d.ellipse((27, 25, 87, 85), outline=Wt, width=7)
    d.polygon([(26, 92), (34, 66), (48, 80)], fill=Wt); d.line((48, 48, 64, 65), fill=Wt, width=8)
    wa = Image.new('RGBA', (100 + t.width, max(110, t.height)), (0, 0, 0, 0))
    wa.alpha_composite(ic, (0, (wa.height - 110) // 2)); wa.alpha_composite(t, (100, (wa.height - t.height) // 2))
    f = ImageFont.truetype(FB, 58); txt = '@liderbateriasepneus'; l, tt, r, b = f.getbbox(txt)
    w = 80 + 72 + 22 + (r - l); h = 120
    ig = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(ig)
    d.rounded_rectangle((0, 0, w, h), radius=60, fill=YEL + (255,)); k = (20, 20, 20, 255)
    d.rounded_rectangle((40, 24, 112, 96), radius=20, outline=k, width=7); d.ellipse((59, 43, 93, 77), outline=k, width=7)
    d.ellipse((90, 35, 100, 45), fill=k); d.text((134 - l, (h - (b - tt)) // 2 - tt), txt, font=f, fill=k)
    return addr, wa, ig

def main():
    cfg = json.load(open(sys.argv[1])); saida = os.path.abspath(sys.argv[2])
    segs = cfg['segmentos']; assert len(segs) == 20, 'precisa de exatamente 20 segmentos'
    tmp = tempfile.mkdtemp()
    subprocess.run([sys.executable, os.path.join(AQUI, 'musica.py'), f'{tmp}/m.wav', str(cfg.get('musica_seed', 7))], check=True)
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(preparar, [(i, s, tmp) for i, s in enumerate(segs)]))

    logo = Image.open(os.path.join(RAIZ, 'marca', 'logo.png')).convert('RGBA')
    lw = lambda w: logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    LOGO_BIG = glow(lw(900), 30, 170); LOGO_WM = glow(lw(250), 14, 160)
    g1, g2 = cfg.get('gancho', ['TUDO PARA O SEU', 'CARRO E MOTO'])
    T_H1 = fit(g1, 70, 980, (255, 255, 255), FM); T_H2 = fit(g2, 118, 1000, YEL)
    L1 = label_img(*cfg.get('tema1', ['PNEUS', 'para carros e motos']))
    L2 = label_img(*cfg.get('tema2', ['BATERIAS', 'as melhores marcas']))
    p1, p2, p3 = cfg.get('pausa', ['ESTOQUE', 'COMPLETO', 'pronta entrega'])
    T_P = [fit(p1, 150, 1000), fit(p2, 150, 1000, YEL), fit(p3, 64, 1000, (255, 255, 255), FM)]
    WORDS = cfg.get('palavras', ['QUALIDADE', 'VARIEDADE', 'CONFIANÇA', 'VEM PRA LÍDER!'])[:4]
    T_W = [fit(w, 130, 1000, YEL if i == 3 else (255, 255, 255)) for i, w in enumerate(WORDS)]
    T_FIM = text_img(cfg.get('fim', 'Venha nos visitar!'), 84)
    T_ADDR, T_WA, T_IG = card_final()

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    VIG = (1 - 0.38 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)).clip(0.45, 1)[..., None]
    BAND_C = np.exp(-((yy - 990) / 260) ** 2)[..., None]; BAND_L = np.exp(-((yy - 1340) / 220) ** 2)[..., None]
    GRAD_TOP = np.clip(1 - yy / 420, 0, 1)[..., None] * 0.45

    B = bounds(); TOTAL = B[-1][1]; LAST = 19
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-i', f'{tmp}/m.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '21', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                            '-af', f'afade=t=out:st={TOTAL / FPS - 1.5:.2f}:d=1.5', '-movflags', '+faststart', '-shortest', saida],
                           stdin=subprocess.PIPE)
    fi = 0
    for si in range(20):
        a, b = B[si]; cap = cv2.VideoCapture(f'{tmp}/{si:02d}.mp4'); last = None
        for k in range(b - a):
            ok, fr = cap.read()
            if not ok: fr = last
            last = fr; t = fi / FPS; tl = k / FPS; dur = (b - a) / FPS
            drop = si >= 1 and si not in (9, 10, LAST)
            s = 1.0 + (0.10 * (1 - ease_out(tl / 0.32)) if drop else 0) + 0.05 * (tl / dur)
            if si == 0: s = 1.12 - 0.08 * ease_out(tl / dur)
            M = np.float32([[s, 0, (1 - s) * W / 2], [0, s, (1 - s) * H / 2]])
            f = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255.0
            if 11 <= si < LAST and k < 4:
                o = int(14 * (1 - k / 4)); f[..., 2] = np.roll(f[..., 2], o, 1); f[..., 0] = np.roll(f[..., 0], -o, 1)
            if si == LAST:
                bl = ease_out(tl / 0.6); f = cv2.GaussianBlur(f, (0, 0), 1 + 22 * bl) * (1 - 0.55 * bl)
            if si == 0: f = f * 0.55
            f = f * VIG
            if T_DROP1 <= t < T_END: f = f * (1 - GRAD_TOP)
            if T_BRK <= t < T_END: f = f * (1 - 0.5 * ease_out((t - T_BRK) / 0.4) * BAND_C)
            elif T_DROP1 <= t < T_BRK: f = f * (1 - 0.35 * BAND_L)
            if t < T_DROP1:
                p = back_out((t - 0.25) / 0.6); ex = ease_in((t - (T_DROP1 - 0.25)) / 0.25)
                comp(f, LOGO_BIG, W / 2, 760, alpha=min(1, max(0, t - 0.25) / 0.2) * (1 - ex), s=max(0.01, 0.6 + 0.4 * p + 0.6 * ex))
                q1 = ease_out((t - 1.3) / 0.4); comp(f, T_H1, W / 2 - 120 * (1 - q1), 1080, alpha=q1 * (1 - ex))
                q2 = ease_out((t - 1.7) / 0.4); comp(f, T_H2, W / 2 + 120 * (1 - q2), 1185, alpha=q2 * (1 - ex), s=1 + 0.15 * (1 - q2))
            if T_DROP1 <= t < T_END:
                comp(f, LOGO_WM, 70 + LOGO_WM.width / 2 - 50, 120 + LOGO_WM.height / 2, alpha=ease_out((t - T_DROP1) / 0.5) * 0.95)
            for lab, t0, t1 in ((L1, T_DROP1 + 0.15, T_DROP1 + 4 * BAR - 0.1), (L2, T_DROP1 + 4 * BAR + 0.15, T_BRK - 0.1)):
                if t0 <= t < t1:
                    pin, pout = ease_out((t - t0) / 0.45), ease_in((t - (t1 - 0.3)) / 0.3)
                    comp(f, lab, 60 + lab.width / 2 - (lab.width + 120) * (1 - pin) - (lab.width + 120) * pout, 1330)
            if T_BRK <= t < T_DROP2:
                for im, y, dl in ((T_P[0], 820, 0.1), (T_P[1], 975, 0.35), (T_P[2], 1110, 0.7)):
                    pin, pout = ease_out((t - T_BRK - dl) / 0.5), ease_in((t - (T_DROP2 - 0.3)) / 0.25)
                    comp(f, im, W / 2, y + 60 * (1 - pin), alpha=pin * (1 - pout), s=1 + 0.08 * (t - T_BRK) / (2 * BAR))
            if T_DROP2 <= t < T_END:
                wi = int((t - T_DROP2) / BAR)
                if wi < len(T_W):
                    t0 = T_DROP2 + wi * BAR; pin = back_out((t - t0) / 0.3); pout = ease_in((t - (t0 + BAR - 0.18)) / 0.18)
                    comp(f, T_W[wi], W / 2, 1000, alpha=min(1, (t - t0) / 0.1) * (1 - pout), s=max(0.05, 0.5 + 0.5 * pin + 0.3 * pout))
            if t >= T_END:
                te = t - T_END
                comp(f, LOGO_BIG, W / 2, 640, alpha=min(1, max(0, te - 0.15) / 0.2), s=max(0.05, 0.5 + 0.5 * back_out((te - 0.15) / 0.6)))
                q = ease_out((te - 0.6) / 0.5); comp(f, T_FIM, W / 2, 900 + 50 * (1 - q), alpha=q)
                q = ease_out((te - 0.95) / 0.5); comp(f, T_ADDR, W / 2, 1065 + 50 * (1 - q), alpha=q)
                q = ease_out((te - 1.25) / 0.5); comp(f, T_WA, W / 2, 1255 + 50 * (1 - q), alpha=q)
                comp(f, T_IG, W / 2, 1410, alpha=min(1, max(0, te - 1.6) / 0.15), s=max(0.05, 0.6 + 0.4 * back_out((te - 1.6) / 0.5)))
                f = f * (1 - ease_in((te - 3.95) / 0.6))
            for tf in (T_DROP1, T_DROP2, T_END):
                d = t - tf
                if 0 <= d < 0.3: fl = 0.85 * (1 - d / 0.3) ** 2; f = f * (1 - fl) + fl
            enc.stdin.write((np.clip(f, 0, 1) * 255).astype(np.uint8).tobytes()); fi += 1
        cap.release()
    enc.stdin.close(); enc.wait()
    print('ok', saida, TOTAL, 'frames')

if __name__ == '__main__':
    main()
