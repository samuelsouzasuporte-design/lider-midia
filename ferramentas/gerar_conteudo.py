"""Artes de DICA e de MEME da Líder. Gera feed.jpg (1080x1350) e story.jpg (1080x1920).

Uso: python3 ferramentas/gerar_conteudo.py arte.json pasta_saida

DICA (cartão com 3 a 4 dicas numeradas):
{
  "tipo": "dica",
  "categoria": "BATERIA DE CARRO",          # BATERIA DE CARRO | BATERIA DE MOTO | PNEU DE CARRO | PNEU DE MOTO
  "titulo1": "3 SINAIS DE",                 # branco (curto)
  "titulo2": "BATERIA FRACA",               # amarelo (curto)
  "dicas": ["Carro demora a pegar de manhã", "Luzes do painel fracas", "Bateria com mais de 2 anos"],
  "rodape": "Na dúvida, a gente testa pra você!",   # chamada final (curta)
  "foto": "fotos/bateria-carro-07-moura.jpg",       # opcional: faixa de foto no topo
  "posicao_foto": "center 50%"
}

MEME (formato clássico de meme, com foto própria da loja ou ilustração; NUNCA usar imagem de meme famoso/pessoas reais):
{
  "tipo": "meme",
  "topo": "EU ACHANDO QUE A BATERIA AGUENTA MAIS UM MÊS",
  "foto": "fotos/ilustracao-bateria-moto.jpg",
  "posicao_foto": "center 50%",
  "baixo": "A BATERIA ÀS 6H DA MANHÃ DE SEGUNDA:",   # opcional
  "emoji": "💀"                                      # opcional (aparece grande sobre a foto)
}
"""
import os, sys, json, html, subprocess, tempfile
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
F = os.path.join(AQUI, 'fontes'); Y = '#FFB800'
WA = '<path d="M3.5 20.5l1.3-4A8.5 8.5 0 1 1 8 19.6z"/><path d="M9 8.5c0 3 2.5 6 6 6.5l1.2-1.4-2-1.1-.9.8c-1-.4-2-1.4-2.4-2.4l.8-.9-1.1-2z"/>'
IG = '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".8" fill="currentColor"/>'
BULB = '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>'
def svg(p, s, c, w=2.2):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" style="color:{c};flex:none">{p}</svg>'
CSS = ''.join(f"@font-face{{font-family:'BC';font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}"
              for w, st in ((600, 'normal'), (700, 'normal'), (700, 'italic'), (800, 'italic'), (900, 'italic')))
CSS += ''.join(f"@font-face{{font-family:'Inter';font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}" for w in (500, 600, 700))
LOGO = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
e = html.escape

def rodape(story):
    if story:
        return f'''<div style="position:absolute;left:60px;right:60px;bottom:200px;background:{Y};border-radius:24px;padding:18px 30px;display:flex;align-items:center;gap:18px">{svg(WA, 64, '#111', 2)}
          <div style="font-family:BC;line-height:.95;color:#111"><div style="font-weight:700;font-size:26px;letter-spacing:1px">CHAMA NO WHATSAPP</div>
          <div style="font-weight:900;font-style:italic;font-size:66px">(88) 9.8865-5130</div></div></div>
          <div style="position:absolute;left:60px;right:60px;bottom:140px;display:flex;justify-content:space-between;font-family:Inter;font-weight:600;font-size:25px;color:#E8ECF6">
          <span>Rua Deolino Barreto, 860 - Centro</span><span style="display:flex;gap:8px;align-items:center">{svg(IG, 26, Y)}@liderbateriasepneus</span></div>'''
    return f'''<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:{Y};display:flex;align-items:center;justify-content:space-between;padding:0 50px;box-sizing:border-box">
      <div style="display:flex;align-items:center;gap:14px">{svg(WA, 52, '#111', 2)}<div style="font-family:BC;font-weight:900;font-style:italic;font-size:52px;color:#111">(88) 9.8865-5130</div></div>
      <div style="text-align:right;font-family:Inter;font-weight:700;font-size:21px;color:#111;line-height:1.45">Rua Deolino Barreto, 860 - Centro<br>@liderbateriasepneus</div></div>'''

def dica(c, W, H):
    story = H > 1500
    foto = c.get('foto'); fh = 600 if story else 400
    topo = 300 if story else 70
    itens = ''
    for i, d in enumerate(c['dicas'][:4]):
        itens += f'''<div style="display:flex;align-items:center;gap:22px;background:rgba(255,255,255,.06);border:2px solid rgba(255,184,0,.35);border-radius:22px;padding:{'30px 30px' if story else '22px 24px'}">
          <div style="width:{76 if story else 62}px;height:{76 if story else 62}px;flex:none;border-radius:50%;background:{Y};display:flex;align-items:center;justify-content:center;font-family:BC;font-weight:900;font-style:italic;font-size:{48 if story else 40}px;color:#0B0C10">{i+1}</div>
          <div style="font-family:Inter;font-weight:700;font-size:{40 if story else 33}px;line-height:1.2;color:#fff">{e(d)}</div></div>'''
    img = (f'<img src="file://{os.path.join(RAIZ, foto)}" style="position:absolute;left:0;top:0;width:{W}px;height:{fh + topo}px;object-fit:cover;object-position:{c.get("posicao_foto","center 50%")}">'
           f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{fh + topo}px;background:linear-gradient(180deg,rgba(6,9,22,.8) 0%,rgba(6,9,22,.35) 35%,rgba(6,9,22,.55) 70%,#060916 100%)"></div>') if foto else ''
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:radial-gradient(120% 70% at 80% 0%,#13214F 0%,#060916 60%)">
      {img}
      <img src="{LOGO}" style="position:absolute;left:56px;top:{topo - 40 if story else 40}px;width:{300 if story else 230}px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.7))">
      <div style="position:absolute;right:56px;top:{topo - 30 if story else 48}px;background:{Y};color:#0B0C10;border-radius:999px;padding:10px 22px;display:flex;align-items:center;gap:10px;font-family:BC;font-weight:900;font-style:italic;font-size:{34 if story else 28}px">{svg(BULB, 34 if story else 28, '#0B0C10', 2.4)}DICA DA LÍDER</div>
      <div style="position:absolute;left:56px;right:56px;top:{(fh + topo - 230) if story else (fh - 130)}px">
        <div style="font-family:BC;font-weight:800;font-style:italic;font-size:{40 if story else 34}px;color:{Y};letter-spacing:2px">{e(c.get('categoria',''))}</div>
        <div style="font-family:BC;font-weight:900;font-style:italic;line-height:.88;text-transform:uppercase">
          <div style="font-size:{120 if story else 96}px;color:#fff;text-shadow:0 6px 20px rgba(0,0,0,.7)">{e(c['titulo1'])}</div>
          <div style="font-size:{130 if story else 104}px;color:{Y};text-shadow:0 6px 20px rgba(0,0,0,.7)">{e(c['titulo2'])}</div></div></div>
      <div style="position:absolute;left:56px;right:56px;top:{fh + topo + 70 if story else fh + 150}px;display:flex;flex-direction:column;gap:{26 if story else 16}px">{itens}
        <div style="margin-top:{14 if story else 6}px;font-family:BC;font-weight:800;font-style:italic;font-size:{46 if story else 38}px;color:{Y};text-align:center">{e(c.get('rodape',''))}</div></div>
      {rodape(story)}</div>'''

def meme(c, W, H):
    story = H > 1500
    top = 330 if story else 70
    foto = os.path.join(RAIZ, c['foto'])
    ph = 900 if story else 700
    baixo = c.get('baixo', '')
    emoji = c.get('emoji', '')
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:#0B0C10">
      <img src="{LOGO}" style="position:absolute;left:50%;transform:translateX(-50%);top:{top - 230 if story else 0}px;width:{320 if story else 0}px;{'' if story else 'display:none'}">
      <div style="position:absolute;left:40px;right:40px;top:{top}px;background:#fff;border-radius:22px 22px 0 0;padding:{'34px 40px' if story else '30px 36px'};box-sizing:border-box">
        <div style="font-family:Inter;font-weight:700;font-size:{52 if story else 48}px;line-height:1.18;color:#111">{e(c['topo'])}</div></div>
      <div style="position:absolute;left:40px;right:40px;top:{top + (190 if story else 170)}px;height:{ph}px;overflow:hidden;border-radius:0 0 22px 22px">
        <img src="file://{foto}" style="width:100%;height:100%;object-fit:cover;object-position:{c.get('posicao_foto','center 50%')}">
        {f'<div style="position:absolute;left:0;right:0;bottom:0;padding:26px 30px;background:linear-gradient(0deg,rgba(0,0,0,.85),rgba(0,0,0,0));font-family:BC;font-weight:900;font-size:{64 if story else 58}px;line-height:1;color:#fff;text-transform:uppercase;text-align:center;-webkit-text-stroke:2px #000">{e(baixo)}</div>' if baixo else ''}
        {f'<div style="position:absolute;right:26px;top:22px;font-size:{120 if story else 110}px;line-height:1">{e(emoji)}</div>' if emoji else ''}</div>
      <div style="position:absolute;left:40px;right:40px;top:{top + (190 if story else 170) + ph + 24}px;display:flex;justify-content:space-between;align-items:center">
        <img src="{LOGO}" style="width:{0 if story else 230}px;{'display:none' if story else ''}">
        <div style="font-family:BC;font-weight:800;font-style:italic;font-size:{44 if story else 38}px;color:{Y};{'width:100%;text-align:center' if story else ''}">{e(c.get('chamada','Na Líder você não fica na mão! ⚡'))}</div></div>
      {rodape(story)}</div>'''

def main():
    c = json.load(open(sys.argv[1])); out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(); jobs = []
    fn = dica if c.get('tipo') == 'dica' else meme
    for nome, H in (('feed', 1350), ('story', 1920)):
        p = f'{tmp}/{nome}.html'
        open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}body{{margin:0}}</style></head><body>{fn(c, 1080, H)}</body></html>")
        jobs.append((p, f'{tmp}/{nome}.png', H))
    js = f'{tmp}/s.js'; open(js, 'w').write("""const { chromium } = require('playwright');
(async () => { const j = JSON.parse(process.argv[2]); const b = await chromium.launch();
for (const [s, o, h] of j) { const p = await b.newPage({ viewport: { width: 1080, height: h } }); await p.goto('file://' + s);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400); await p.screenshot({ path: o }); } await b.close(); })();""")
    subprocess.run(['node', js, json.dumps(jobs)], check=True)
    for nome in ('feed', 'story'):
        Image.open(f'{tmp}/{nome}.png').convert('RGB').save(f'{out}/{nome}.jpg', quality=92); print(f'{out}/{nome}.jpg')

if __name__ == '__main__':
    main()
