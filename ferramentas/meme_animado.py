"""MEME ANIMADO (Story em vídeo, 8s) contado em 3 tempos, com trilha própria e efeitos sonoros.
  0,0s  aparece só o texto de cima (com leve zoom)
  1,2s  a foto entra com "pop" (zoom de entrada) + som de pop
  3,4s  PUNCHLINE: frase de baixo + emoji aparecem com flash, tremida e som de impacto
Uso: python3 ferramentas/meme_animado.py posts/<data>/<nome>.json posts/<data>/<nome>/story.mp4 [seed_musica]
O JSON é o mesmo do meme de gerar_conteudo.py ("tipo":"meme"; "baixo" e "emoji" são a punchline).
Agende como STORY 4 minutos antes do horário (vídeo).
"""
import os, sys, json, subprocess, tempfile, shutil
import numpy as np
from PIL import Image, ImageEnhance
from scipy.io import wavfile

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, D = 1080, 1920, 30, 8.0
TOP = 330; FX0, FX1 = 40, 1040; FY0 = TOP + 190; FY1 = FY0 + 900   # área da foto no meme (story)
T_FOTO, T_PUNCH = 1.2, 3.4
SR = 44100


def render(cfg, tmp, nome):
    js = os.path.join(tmp, nome + '.json'); out = os.path.join(tmp, nome)
    json.dump(cfg, open(js, 'w'), ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(AQUI, 'gerar_conteudo.py'), js, out], check=True, stdout=subprocess.DEVNULL)
    return Image.open(os.path.join(out, 'story.jpg')).convert('RGB')


def ease_out_back(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def zoom(img, s, dx=0, dy=0):
    if abs(s - 1) < 1e-4 and dx == 0 and dy == 0:
        return img
    w, h = img.size; nw, nh = int(w * s), int(h * s)
    big = img.resize((nw, nh), Image.BICUBIC)
    x = (nw - w) // 2 - int(dx); y = (nh - h) // 2 - int(dy)
    canvas = Image.new('RGB', (w, h), (11, 12, 16))
    canvas.paste(big, (-x, -y))
    return canvas


def sons(seed, tmp):
    wav = os.path.join(tmp, 'm.wav')
    subprocess.run([sys.executable, os.path.join(AQUI, 'reels', 'musica.py'), wav, str(seed)], check=True, stdout=subprocess.DEVNULL)
    sr, m = wavfile.read(wav); m = m.astype(np.float32)
    if m.ndim == 1: m = np.stack([m, m], 1)
    m /= (np.abs(m).max() + 1e-9)
    st = int(3.87 * sr); n = int(D * sr)
    m = m[st:st + n] * 0.45
    if len(m) < n: m = np.pad(m, ((0, n - len(m)), (0, 0)))
    t = np.arange(n) / sr
    fx = np.zeros(n, np.float32)
    # pop (entrada da foto)
    i = int(T_FOTO * sr); k = np.arange(int(0.12 * sr)) / sr
    fx[i:i + len(k)] += 0.6 * np.sin(2 * np.pi * (900 - 5000 * k) * k) * np.exp(-k * 35)
    # whoosh antes da punchline
    i0 = int((T_PUNCH - 0.45) * sr); k = np.arange(int(0.45 * sr)) / sr
    nz = np.random.default_rng(3).standard_normal(len(k)).astype(np.float32)
    nz = np.convolve(nz, np.ones(25) / 25, 'same')
    fx[i0:i0 + len(k)] += 0.5 * nz * (k / k.max()) ** 2
    # impacto (punchline): bumbo grave + estalo
    i = int(T_PUNCH * sr); k = np.arange(int(0.6 * sr)) / sr
    boom = np.sin(2 * np.pi * (120 * np.exp(-k * 8) + 45) * k) * np.exp(-k * 6)
    snap = np.random.default_rng(5).standard_normal(len(k)) * np.exp(-k * 40)
    fx[i:i + len(k)] += 0.9 * boom + 0.35 * snap
    # duck da música na punchline
    duck = np.ones(n, np.float32); j = (t > T_PUNCH - 0.05) & (t < T_PUNCH + 0.8)
    duck[j] = 0.35 + 0.65 * np.clip((t[j] - T_PUNCH) / 0.8, 0, 1)
    out = m * duck[:, None] + fx[:, None]
    fade = np.ones(n); fo = int(0.8 * sr); fade[-fo:] = np.linspace(1, 0, fo)
    out *= fade[:, None]
    out /= max(1.0, np.abs(out).max() / 0.95)
    p = os.path.join(tmp, 'a.wav'); wavfile.write(p, SR if sr == SR else sr, (out * 32767).astype(np.int16))
    return p


def main():
    src, dst = sys.argv[1], sys.argv[2]
    seed = sys.argv[3] if len(sys.argv) > 3 else '9'
    c = json.load(open(src)); c['tipo'] = 'meme'
    tmp = tempfile.mkdtemp()
    A = render(c, tmp, 'A')                                     # completo
    B = render({k: v for k, v in c.items() if k not in ('baixo', 'emoji')}, tmp, 'B')   # sem punchline
    S1 = B.copy(); S1.paste(Image.new('RGB', (FX1 - FX0, FY1 - FY0), (24, 26, 34)), (FX0, FY0))
    foto = B.crop((FX0, FY0, FX1, FY1))
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    aud = sons(seed, tmp)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', aud, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', dst], stdin=subprocess.PIPE)
    N = int(D * FPS)
    for f in range(N):
        t = f / FPS
        if t < T_FOTO:
            fr = zoom(S1, 1.04 - 0.03 * t / T_FOTO)
            if t < 0.25:   # entrada suave
                fr = Image.blend(Image.new('RGB', (W, H), (11, 12, 16)), fr, t / 0.25)
        elif t < T_PUNCH:
            x = min(1, (t - T_FOTO) / 0.45); s = 0.55 + 0.45 * ease_out_back(x)
            fr = S1.copy()
            fw, fh = int(foto.width * s), int(foto.height * s)
            fz = foto.resize((max(1, fw), max(1, fh)), Image.BICUBIC)
            cx, cy = (FX0 + FX1) // 2, (FY0 + FY1) // 2
            # recorta o que passar da área (mantém o cartão alinhado)
            fr.paste(fz, (cx - fw // 2, cy - fh // 2))
            if x >= 1:
                fr = B.copy()
            fr = zoom(fr, 1.0 + 0.012 * (t - T_FOTO))
        else:
            k = t - T_PUNCH
            amp = 18 * np.exp(-k * 7)
            dx = amp * np.sin(k * 70); dy = amp * np.cos(k * 53)
            s = 1.0 + 0.07 * np.exp(-k * 9) + 0.015 * k
            fr = zoom(A, s, dx, dy)
            if k < 0.18:   # flash branco
                fr = Image.blend(fr, Image.new('RGB', (W, H), (255, 255, 255)), 0.75 * (1 - k / 0.18))
        if t > D - 0.4:
            fr = ImageEnhance.Brightness(fr).enhance(max(0, (D - t) / 0.4))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    shutil.rmtree(tmp, ignore_errors=True)
    print(dst)


if __name__ == '__main__':
    main()
