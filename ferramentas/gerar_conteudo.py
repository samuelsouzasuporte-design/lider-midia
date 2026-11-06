"""Artes de DICA e de MEME da Líder. Gera feed.jpg (1080x1350) e story.jpg (1080x1920).

Uso: python3 ferramentas/gerar_conteudo.py arte.json pasta_saida

DICA (cartão com 3 dicas numeradas):
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
    for i, d in enumerate(c['dicas'][:3]):
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


CORES = {  # pares (cor A, cor B) para o modelo split; o amarelo da marca é sempre o destaque
    'vermelho_azul': ('#C8102E', '#0B2A8A'), 'azul_laranja': ('#0B2A8A', '#E87A00'), 'roxo_amarelo': ('#4B1FA8', '#C98A00'),
    'preto_amarelo': ('#0B0C10', '#C98A00'), 'royal_vermelho': ('#1E4FD8', '#B3121F'),
}

def marcas(c, W, H):
    """Vitrine 'A MAIOR VARIEDADE' com as marcas em selos de texto (sem logos de terceiros)."""
    story = H > 1500
    acc = c.get('acento', Y)
    def chips(lst):
        return ''.join(
            f'<div style="background:#fff;border-radius:14px;padding:{16 if story else 11}px 8px;text-align:center;font-family:BC;font-weight:900;font-style:italic;font-size:{40 if story else 32}px;color:#0B0C10;box-shadow:0 6px 18px rgba(0,0,0,.4)">{e(m)}</div>'
            for m in lst)
    pneu_ic = svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/>', 40, acc)
    bat_ic = svg('<rect x="3" y="7" width="18" height="12" rx="1"/><path d="M7 7V5h3v2M14 7V5h3v2M7 13h3M15.5 11.5v3M14 13h3"/>', 40, acc)
    secs = ''
    for g in c['grupos']:
        ic = pneu_ic if 'PNEU' in g['titulo'].upper() else bat_ic
        secs += (f'<div><div style="display:flex;align-items:center;gap:12px;justify-content:center;border:2px solid {acc};border-radius:16px;padding:8px 0;margin-bottom:14px;'
                 f'font-family:BC;font-weight:900;font-style:italic;font-size:{48 if story else 38}px;color:#fff">{ic}{e(g["titulo"])}</div>'
                 f'<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px">{chips(g["marcas"])}</div></div>')
    foto = c.get('foto'); fh = 620 if story else 380
    img = ''
    if foto:
        img = (f'<img src="file://{os.path.join(RAIZ, foto)}" style="position:absolute;left:0;bottom:0;width:{W}px;height:{fh}px;object-fit:cover;object-position:{c.get("posicao_foto", "center 60%")};opacity:.6">'
               f'<div style="position:absolute;left:0;bottom:0;width:{W}px;height:{fh}px;background:linear-gradient(180deg,#05060A 0%,rgba(5,6,10,.15) 45%,rgba(5,6,10,.55) 100%)"></div>')
    raios = ''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:600px;height:{h}px;background:{acc};opacity:{o};transform:rotate(-35deg)"></div>'
                    for x, y, h, o in ((-260, 120, 10, .5), (-300, 190, 4, .4), (760, H - 560, 10, .45), (800, H - 500, 4, .35)))
    sub = e(c.get('subtitulo', 'EM BATERIAS E PNEUS'))
    return (f'<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:radial-gradient(110% 70% at 50% 20%,#1A1C24 0%,#05060A 70%)">'
            f'{raios}{img}'
            f'<img src="{LOGO}" style="position:absolute;left:50%;transform:translateX(-50%);top:{150 if story else 34}px;width:{440 if story else 300}px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.7))">'
            f'<div style="position:absolute;left:0;right:0;top:{330 if story else 165}px;text-align:center;font-family:BC;font-weight:900;font-style:italic;line-height:.88">'
            f'<div style="font-size:{110 if story else 86}px;color:#fff">{e(c.get("titulo1", "A MAIOR"))}</div>'
            f'<div style="font-size:{130 if story else 100}px;color:{acc};text-shadow:0 0 30px {acc}55">{e(c.get("titulo2", "VARIEDADE"))}</div>'
            f'<div style="font-weight:800;font-size:{46 if story else 36}px;color:#fff;margin-top:10px;letter-spacing:1px">&#8212; {sub} &#8212;</div></div>'
            f'<div style="position:absolute;left:56px;right:56px;top:{690 if story else 430}px;display:grid;grid-template-columns:repeat({len(c["grupos"])},minmax(0,1fr));gap:28px">{secs}</div>'
            f'{rodape(story)}</div>')

def split(c, W, H):
    """Diagonal de duas cores com foto no topo (estilo 'SEM BATERIA? TEMOS A SOLUÇÃO!')."""
    story = H > 1500
    a, b = CORES.get(c.get('cores', 'vermelho_azul'), CORES['vermelho_azul'])
    foto = os.path.join(RAIZ, c['foto'])
    fh = int(H * (0.50 if story else 0.46))
    l1, l2, l3 = (list(c.get('linhas', ['SEM', 'BATERIA?', 'TEMOS A SOLUÇÃO!'])) + ['', '', ''])[:3]
    clip = 'clip-path:polygon(0 0,100% 0,100% 72%,0 100%)'
    dest = c.get('destaque', '')
    dest_html = (f'<div style="display:inline-flex;margin-top:24px;background:#fff;color:#0B0C10;border-radius:14px;padding:10px 26px;font-size:{46 if story else 36}px;transform:skewX(-8deg)">{e(dest)}</div>') if dest else ''
    return (f'<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{b}">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(135deg,{a} 0%,{a} 49.8%,{b} 50.2%,{b} 100%)"></div>'
            f'<img src="file://{foto}" style="position:absolute;left:0;top:0;width:{W}px;height:{fh}px;object-fit:cover;object-position:{c.get("posicao_foto", "center 40%")};{clip}">'
            f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{fh}px;{clip};background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,0) 40%)"></div>'
            f'<img src="{LOGO}" style="position:absolute;right:44px;top:{110 if story else 30}px;width:{300 if story else 230}px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.9))">'
            f'<div style="position:absolute;left:60px;right:60px;top:{fh + (40 if story else 10)}px;font-family:BC;font-weight:900;font-style:italic;text-transform:uppercase;line-height:.9;color:#fff;text-shadow:0 6px 22px rgba(0,0,0,.6)">'
            f'<div style="font-size:{150 if story else 112}px">{e(l1)}</div>'
            f'<div style="font-size:{150 if story else 112}px;color:{Y}">{e(l2)}</div>'
            f'<div style="font-size:{80 if story else 60}px;margin-top:12px">{e(l3)}</div>{dest_html}</div>'
            f'{rodape(story)}</div>')


def main():
    c = json.load(open(sys.argv[1])); out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(); jobs = []
    fn = {'dica': dica, 'meme': meme, 'marcas': marcas, 'split': split}.get(c.get('tipo'), meme)
    for nome, H in (('feed', 1350), ('story', 1920)):
        p = f'{tmp}/{nome}.html'
        open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}body{{margin:0}}</style></head><body>{fn(c, 1080, H)}</body></html>")
        jobs.append((p, f'{tmp}/{nome}.png', H))
    js = f'{tmp}/s.js'; open(js, 'w').write("""const { chromium } = require('playwright');
(async () => { const j = JSON.parse(process.argv[2]); const b = await chromium.launch();
for (const [s, o, h] of j) { const p = await b.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 2 }); await p.goto('file://' + s);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400); await p.screenshot({ path: o }); } await b.close(); })();""")
    subprocess.run(['node', js, json.dumps(jobs)], check=True)
    for nome in ('feed', 'story'):
        Image.open(f'{tmp}/{nome}.png').convert('RGB').resize((1080, Image.open(f'{tmp}/{nome}.png').height // 2), Image.LANCZOS).save(f'{out}/{nome}.jpg', quality=95, subsampling=0); print(f'{out}/{nome}.jpg')

if __name__ == '__main__':
    main()
