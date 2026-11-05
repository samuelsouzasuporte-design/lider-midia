"""Adapta artes quadradas da Moura (1080x1080 com faixa branca embaixo a partir de y~870)
para a Líder: substitui a faixa branca por uma faixa com logo + WhatsApp + endereço + @,
mantendo o símbolo da Moura num selo branco. Gera feed (1080x1350) e story (1080x1920).

Uso: python3 ferramentas/adaptar_moura.py marcas/moura-original/<arquivo>.png marcas/moura-lider/<nome>
"""
import os, sys, json, subprocess, tempfile
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
F = os.path.join(AQUI, 'fontes'); Y = '#FFB800'
WA = '<path d="M3.5 20.5l1.3-4A8.5 8.5 0 1 1 8 19.6z"/><path d="M9 8.5c0 3 2.5 6 6 6.5l1.2-1.4-2-1.1-.9.8c-1-.4-2-1.4-2.4-2.4l.8-.9-1.1-2z"/>'
IG = '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".8" fill="currentColor"/>'
PIN = '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'
def svg(p, s, c, w=2.2):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" style="color:{c};flex:none">{p}</svg>'
CSS = ''.join(f"@font-face{{font-family:'BC';font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}"
              for w, st in ((600, 'normal'), (700, 'normal'), (700, 'italic'), (800, 'italic'), (900, 'italic')))
CSS += ''.join(f"@font-face{{font-family:'Inter';font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}" for w in (500, 600, 700))

def main():
    src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    im = Image.open(src).convert('RGB')
    im.save(f'{tmp}/top.png')
    # faixa branca livre à esquerda? (só escreve 'AQUI TEM MOURA!' se a área estiver vazia)
    import numpy as np
    zona = np.asarray(im.crop((30, 900, 520, 1070))).astype(int)
    limpo = (zona.min() > 235)
    im.crop((890, 920, 1050, 1035)).save(f'{tmp}/mm.png')   # símbolo Moura da faixa
    logo = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
    faixa = lambda h: f'''<div style="height:{h}px;background:linear-gradient(90deg,#0B0C10,#121522);border-top:8px solid {Y};display:flex;align-items:center;justify-content:space-between;padding:0 50px;box-sizing:border-box;gap:20px">
      <img src="{logo}" style="width:300px;flex:none">
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:12px">
        <div style="background:{Y};border-radius:18px;padding:10px 22px;display:flex;align-items:center;gap:12px">{svg(WA, 48, '#111', 2)}
          <div style="font-family:BC;line-height:.95;color:#111"><div style="font-weight:700;font-size:20px;letter-spacing:1px">CHAMA NO WHATSAPP</div>
          <div style="font-weight:900;font-style:italic;font-size:50px;white-space:nowrap">(88) 9.8865-5130</div></div></div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px;font-family:Inter;font-weight:600;font-size:21px;color:#E8ECF6;white-space:nowrap">
          <span style="display:flex;align-items:center;gap:6px">{svg(PIN, 22, Y)}Rua Deolino Barreto, 860 - Centro, Crateús/CE</span>
          <span style="display:flex;align-items:center;gap:6px">{svg(IG, 22, Y)}@liderbateriasepneus</span></div></div></div>'''
    selo = '''<div style="position:absolute;left:44px;top:930px;font-family:BC;font-weight:900;font-style:italic;font-size:70px;color:#0B1A4A;line-height:.9">AQUI TEM<br><span style="color:#E3A400">MOURA!</span></div>'''
    feed = f'''<div style="width:1080px;height:1350px;background:#0B0C10;display:flex;flex-direction:column;position:relative">
      <img src="file://{tmp}/top.png" style="width:1080px;height:1080px;display:block">{faixa(270)}{selo if limpo else ''}</div>'''
    story = f'''<div style="width:1080px;height:1920px;background:radial-gradient(120% 70% at 50% 30%,#14204F 0%,#05070F 70%);display:flex;flex-direction:column;align-items:center">
      <img src="{logo}" style="width:420px;margin-top:120px">
      <div style="font-family:BC;font-weight:900;font-style:italic;font-size:64px;color:#fff;margin:20px 0 30px">AQUI TEM <span style="color:{Y}">MOURA!</span></div>
      <img src="file://{tmp}/top.png" style="width:960px;height:960px;border-radius:28px;box-shadow:0 20px 60px rgba(0,0,0,.6)">
      <div style="margin-top:36px;background:{Y};border-radius:26px;padding:22px 36px;display:flex;align-items:center;gap:22px">{svg(WA, 76, '#111', 2)}
        <div style="font-family:BC;line-height:.95;color:#111"><div style="font-weight:700;font-size:30px;letter-spacing:1px">CHAMA NO WHATSAPP</div>
        <div style="font-weight:900;font-style:italic;font-size:76px">(88) 9.8865-5130</div></div></div>
      <div style="margin-top:30px;display:flex;gap:30px;font-family:Inter;font-weight:600;font-size:27px;color:#E8ECF6">
        <span style="display:flex;align-items:center;gap:8px">{svg(PIN, 30, Y)}Rua Deolino Barreto, 860 - Centro</span>
        <span style="display:flex;align-items:center;gap:8px">{svg(IG, 30, Y)}@liderbateriasepneus</span></div></div>'''
    jobs = []
    for nome, body, h in (('feed', feed, 1350), ('story', story, 1920)):
        p = f'{tmp}/{nome}.html'; open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}body{{margin:0}}</style></head><body>{body}</body></html>")
        jobs.append((p, f'{tmp}/{nome}.png', h))
    js = f'{tmp}/s.js'; open(js, 'w').write("""const { chromium } = require('playwright');
(async () => { const j = JSON.parse(process.argv[2]); const b = await chromium.launch();
for (const [s, o, h] of j) { const p = await b.newPage({ viewport: { width: 1080, height: h } }); await p.goto('file://' + s);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); await p.screenshot({ path: o }); } await b.close(); })();""")
    subprocess.run(['node', js, json.dumps(jobs)], check=True)
    for nome in ('feed', 'story'):
        Image.open(f'{tmp}/{nome}.png').convert('RGB').save(f'{out}/{nome}.jpg', quality=92)
    print(out)

if __name__ == '__main__':
    main()
