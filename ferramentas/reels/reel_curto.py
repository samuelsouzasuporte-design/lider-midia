"""Reels CURTO "problema real" (7-12 s): 1 clipe principal + textos grandes por tempo + tela final.
Uso: python3 ferramentas/reels/reel_curto.py reel_curto.json saida.mp4
{"clipe":"loja-IMG_8388.mp4","inicio":0,"dur":7.5,"velocidade":0.87,"musica_seed":180,
 "textos":[[0,3,["CARRO NÃO","PEGOU HOJE?"]],[3,6,["A GENTE","LEVA E INSTALA"]]],
 "final":["SEGUE A GENTE","(88) 9.8865-5130","Chama no zap e diz que viu no Instagram"],"final_dur":2.6}
A 1ª linha de cada texto sai branca e a 2ª amarela, numa faixa escura no terço superior. Sem logo na abertura.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
FB = os.path.join(RAIZ, 'ferramentas', 'fontes', 'Poppins-BoldItalic.ttf')
FM = os.path.join(RAIZ, 'ferramentas', 'fontes', 'Poppins-MediumItalic.ttf')
W, H = 1080, 1920; YEL = (255, 184, 0)
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]; tmp = tempfile.mkdtemp()

def fit(txt, font, maxw, start):
    s = start
    while ImageFont.truetype(font, s).getlength(txt) > maxw and s > 40: s -= 4
    return ImageFont.truetype(font, s)

def card_texto(linhas, path):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fs = [fit(l, FB, W - 120, 150) for l in linhas]
    hs = [f.size * 1.12 for f in fs]; tot = sum(hs) + 60; y0 = 330
    d.rounded_rectangle([40, y0 - 30, W - 40, y0 + tot - 10], 36, fill=(8, 14, 40, 215))
    d.rectangle([40, y0 + tot - 24, W - 40, y0 + tot - 10], fill=YEL + (255,))
    y = y0
    for i, (l, f) in enumerate(zip(linhas, fs)):
        w = f.getlength(l); c = (255, 255, 255) if i == 0 else YEL
        d.text(((W - w) / 2 + 4, y + 5), l, font=f, fill=(0, 0, 0, 160)); d.text(((W - w) / 2, y), l, font=f, fill=c)
        y += hs[i]
    im.save(path)

src = os.path.join(RAIZ, 'videos', cfg['clipe']); sp = cfg['velocidade']; vdur = cfg['dur'] / sp
base = f'{tmp}/base.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(cfg['inicio']), '-t', str(cfg['dur']), '-i', src, '-an', '-vf',
    f"setpts=PTS/{sp},fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=contrast=1.07:saturation=1.2,unsharp=5:5:0.5,format=yuv420p",
    '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', base], check=True)
# tela final: último quadro borrado + logo + textos
last = f'{tmp}/last.png'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.2', '-i', base, '-frames:v', '1', last], check=True)
bg = Image.open(last).convert('RGB').filter(ImageFilter.GaussianBlur(18))
bg = Image.blend(bg, Image.new('RGB', (W, H), (8, 14, 40)), 0.62); d = ImageDraw.Draw(bg)
logo = Image.open(os.path.join(RAIZ, 'marca', 'logo.png')).convert('RGBA'); lw = 760
logo = logo.resize((lw, int(logo.height * lw / logo.width))); bg.paste(logo, ((W - lw) // 2, 460), logo)
f1, f2, f3 = fit(cfg['final'][0], FB, W - 140, 120), fit(cfg['final'][1], FB, W - 160, 110), fit(cfg['final'][2], FM, W - 120, 46)
y = 860
d.rounded_rectangle([90, y - 10, W - 90, y + f1.size * 1.25], 30, fill=YEL)
d.text(((W - f1.getlength(cfg['final'][0])) / 2, y), cfg['final'][0], font=f1, fill=(8, 14, 40)); y += f1.size * 1.25 + 70
d.text(((W - f2.getlength(cfg['final'][1])) / 2, y), cfg['final'][1], font=f2, fill=(255, 255, 255)); y += f2.size * 1.3
d.text(((W - f3.getlength(cfg['final'][2])) / 2, y), cfg['final'][2], font=f3, fill=YEL); y += f3.size * 1.6
end = 'Rua Deolino Barreto, 860 - Centro, Crateús/CE'; f4 = fit(end, FM, W - 140, 40)
d.text(((W - f4.getlength(end)) / 2, y), end, font=f4, fill=(230, 230, 230))
bg.save(f'{tmp}/final.png'); fd = cfg.get('final_dur', 2.6); total = vdur + fd
# overlays de texto
inputs = ['-i', base, '-loop', '1', '-t', str(fd), '-i', f'{tmp}/final.png']; filt = []; cur = '[0:v]'
for k, (a, b, linhas) in enumerate(cfg['textos']):
    p = f'{tmp}/t{k}.png'; card_texto(linhas, p); inputs += ['-i', p]
    filt.append(f"{cur}[{k+2}:v]overlay=0:0:enable='between(t,{a},{min(b, vdur)})'[v{k}]"); cur = f'[v{k}]'
filt.append(f"[1:v]fps=30,format=yuv420p,fade=in:st=0:d=0.25[fin]")
filt.append(f"{cur}format=yuv420p[vv];[vv][fin]concat=n=2:v=1:a=0[vout]")
# música
wav = f'{tmp}/m.wav'
subprocess.run([sys.executable, os.path.join(AQUI, 'musica.py'), wav, str(cfg['musica_seed'])], check=True, stdout=subprocess.DEVNULL)
ini = cfg.get('musica_inicio', 60 / 124 * 8)
inputs += ['-ss', str(ini), '-t', str(total), '-i', wav]; ai = len(cfg['textos']) + 2
filt.append(f"[{ai}:a]afade=t=in:d=0.05,afade=t=out:st={total-0.8}:d=0.8,volume=0.9[aout]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(filt), '-map', '[vout]', '-map', '[aout]',
    '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-r', '30',
    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(total), out], check=True)
print(out, round(total, 2), 's')
