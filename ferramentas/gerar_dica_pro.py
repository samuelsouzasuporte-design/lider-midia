"""DICA PRO (estilo "consultivo", inspirado na referência que o dono mandou em 09/11/2026):
foto real em tela cheia, degradê azul da esquerda, logo pequeno, título em itálico com a última
linha em amarelo, subtítulo, seta e uma lista com barra amarela ao lado. Fica profissional para
DICAS, capas de carrossel e posts de serviço/confiança.

Uso: python3 ferramentas/gerar_dica_pro.py arte.json pasta_saida  -> feed.jpg (1080x1350) e story.jpg (1080x1920)
arte.json:
{
  "foto": "fotos/servico-teste-bateria.jpg",
  "posicao_foto": "center 45%",
  "titulo": ["NÃO SABE QUAL", "BATERIA É A", "CERTA PRO SEU CARRO?"],   # 2 a 4 linhas curtas; a última fica amarela
  "amarelas": [2],                       # opcional: índices das linhas amarelas (padrão: a última)
  "subtitulo": "Antes de trocar, a gente confere com você:",
  "lista": ["Teste da bateria atual", "Amperagem certa", "Modelo do carro", "Encaixe e polos"],
  "selo": "ARRASTA PRO LADO ➜",         # opcional (capa de carrossel) — ou "1/5"
  "frase": "A BATERIA CERTA É PARTE DO ATENDIMENTO",   # opcional: fecho em amarelo abaixo da lista
  "lista_posicao": "baixo",              # opcional: baixo (padrão) | topo (lista logo abaixo do subtítulo)
  "cor": "azul"                          # azul | noite | grafite | royal
}
Modo PERGUNTAS ("dúvidas que recebemos todo dia"): em vez de titulo/lista, passe
  "titulo_duplo": [["DÚVIDAS QUE", "A GENTE OUVE"], ["TODO DIA", "NA LÍDER"]],   # [branco, amarelo] por linha
  "perguntas": ["...?", "...?", "...?", "...?"],                                 # 3 a 5, alternam esquerda/direita
  "cta": ["Tem dúvida?", "Chama no zap que a gente responde."]
Regras: só fotos da pasta fotos/; textos verdadeiros e confirmados no CLAUDE.md.
"""
import json, os, sys, subprocess, tempfile, html
from PIL import Image, ImageFilter, ImageEnhance

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
Y = '#FFC21A'
CORES = {
    'azul':    ('rgba(8,24,84,', '#0A1A55'),
    'noite':   ('rgba(6,10,32,', '#060A20'),
    'grafite': ('rgba(18,20,26,', '#121418'),
    'royal':   ('rgba(18,52,170,', '#12349A'),
}


def fontes():
    f = os.path.join(AQUI, 'fontes')
    css = ''
    for w, st in ((600, 'normal'), (700, 'italic'), (800, 'italic'), (900, 'italic')):
        css += f"@font-face{{font-family:'EX';font-weight:{w};font-style:{st};src:url('file://{f}/exo-2-latin-{w}-{st}.woff2')}}\n"
    css += f"@font-face{{font-family:'PO';font-weight:500;font-style:italic;src:url('file://{f}/Poppins-MediumItalic.ttf')}}\n"
    css += f"@font-face{{font-family:'PO';font-weight:700;font-style:italic;src:url('file://{f}/Poppins-BoldItalic.ttf')}}\n"
    return css


def montar(cfg, W, H, foto):
    story = H > 1500
    e = html.escape
    tint, solido = CORES.get(cfg.get('cor', 'azul'), CORES['azul'])
    pos = cfg.get('posicao_foto', 'center 45%')
    tit = cfg.get('titulo', [])
    am = set(cfg.get('amarelas', [len(tit) - 1]))
    fs_t = (96 if story else 84) if max((len(t) for t in tit), default=0) <= 16 else (80 if story else 70)
    linhas = ''.join(f'<div style="color:{Y if i in am else "#fff"}">{e(t)}</div>' for i, t in enumerate(tit))
    lista = ''.join(f'<div>{e(t)}</div>' for t in cfg.get('lista', []))
    selo = cfg.get('selo', '')
    selo_html = (f'<div style="position:absolute;right:{60}px;top:{150 if story else 70}px;background:{Y};color:#0B0B0B;font-family:EX;font-weight:800;font-style:italic;'
                 f'font-size:{34 if story else 28}px;padding:10px 22px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.4)">{e(selo)}</div>') if selo else ''
    logo = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
    if cfg.get('lista_posicao') == 'topo':   # texto em cima: escurece só a parte de cima e deixa a cena de baixo aparecer
        grad = f'linear-gradient(180deg,{tint}.92) 0%,{tint}.80) 40%,{tint}.15) 62%,{tint}0) 80%)'
    else:
        grad = f'linear-gradient(90deg,{tint}.96) 0%,{tint}.88) 38%,{tint}.45) 68%,{tint}.10) 100%)'
    frase = cfg.get('frase', '')   # opcional: frase de fechamento em destaque abaixo da lista
    frase_html = (f'<div style="margin-top:{26 if story else 20}px;display:flex;gap:28px;align-items:stretch"><div style="width:7px;border-radius:4px;background:{Y}"></div>'
                  f'<div style="font-family:EX;font-weight:800;font-style:italic;font-size:{44 if story else 38}px;line-height:1.15;color:{Y};text-transform:uppercase;max-width:{760 if story else 680}px;text-shadow:0 3px 12px rgba(0,0,0,.7)">{e(frase)}</div></div>') if frase else ''
    bloco = (f'<div style="display:flex;gap:28px;align-items:stretch">'
             f'<div style="width:7px;border-radius:4px;background:{Y}"></div>'
             f'<div style="font-family:EX;font-weight:600;font-size:{50 if story else 44}px;line-height:1.32;color:#fff;text-shadow:0 3px 12px rgba(0,0,0,.7)">{lista}</div></div>' + frase_html)
    chev = (f'<svg width="{40 if story else 34}" height="{24 if story else 20}" viewBox="0 0 24 14" style="margin-top:18px" fill="none" stroke="#fff" stroke-width="3" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l9 8 9-8"/></svg>')
    if cfg.get('lista_posicao') == 'topo':   # lista logo abaixo do subtítulo (quando a parte de baixo da foto é a cena principal)
        lista_topo = f'<div style="margin-top:{26 if story else 20}px;display:inline-block;background:rgba(5,9,25,.62);border-radius:18px;padding:{"22px 30px" if story else "18px 26px"};box-shadow:0 10px 30px rgba(0,0,0,.35)">{bloco}</div>'
        lista_baixo = ''
    else:
        lista_topo = chev
        lista_baixo = f'<div style="position:absolute;left:{110 if story else 100}px;bottom:{330 if story else 150}px">{bloco}</div>'
    top = 360 if story else 225
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{solido}">
  <img src="file://{foto}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};filter:saturate(1.05)">
  <div style="position:absolute;inset:0;background:{grad}"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,{tint}.55) 0%,{tint}0) 22%,{tint}0) 70%,{tint}.75) 100%)"></div>
  <img src="{logo}" style="position:absolute;left:70px;top:{150 if story else 70}px;width:{300 if story else 250}px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.5))">
  {selo_html}
  <div style="position:absolute;left:70px;right:90px;top:{top}px">
    <div style="font-family:EX;font-weight:900;font-style:italic;font-size:{fs_t}px;line-height:1.1;letter-spacing:-1px;text-shadow:0 4px 18px rgba(0,0,0,.45)">{linhas}</div>
    <div style="margin-top:{34 if story else 26}px;font-family:PO;font-weight:700;font-style:italic;font-size:{44 if story else 38}px;line-height:1.25;color:#fff;max-width:{760 if story else 700}px;text-shadow:0 3px 12px rgba(0,0,0,.5)">{e(cfg.get('subtitulo', ''))}</div>
    {lista_topo}
  </div>
  {lista_baixo}
  <div style="position:absolute;left:0;right:0;bottom:0;height:{120 if story else 92}px;display:flex;align-items:center;justify-content:space-between;padding:0 70px;box-sizing:border-box;
       font-family:EX;font-weight:800;font-style:italic;font-size:{38 if story else 32}px;color:#fff;background:linear-gradient(90deg,{tint}.95),{tint}.6))">
    <span><span style="color:{Y}">WhatsApp</span> (88) 9.8865-5130</span><span style="font-family:PO;font-weight:500;font-size:{28 if story else 24}px">@liderbateriasepneus</span>
  </div>
</div>'''


def montar_inferior(cfg, W, H, foto):
    """Layout INFERIOR (como a referência do dono "Por que não indicamos uma bateria apenas pelo preço?"):
    foto do produto em cima, degradê para azul embaixo, logo no canto direito, título branco em itálico embaixo
    e 1 a 2 blocos com barra amarela. Campos: titulo, amarelas (opcional, padrão nenhuma), blocos [[linha amarela, linha branca], [LINHA BRANCA]]."""
    story = H > 1500
    e = html.escape
    tint, solido = CORES.get(cfg.get('cor', 'azul'), CORES['azul'])
    pos = cfg.get('posicao_foto', 'center 40%')
    tit = cfg.get('titulo', [])
    am = set(cfg.get('amarelas', []))
    mx = max((len(t) for t in tit), default=1)
    fs_t = min(88 if story else 78, int((1500 if story else 1480) / max(mx, 1)))
    linhas = ''.join(f'<div style="color:{Y if i in am else "#fff"}">{e(t)}</div>' for i, t in enumerate(tit))
    blocos = ''
    for b in cfg.get('blocos', []):
        if len(b) >= 2:
            txt = (f'<div style="color:{Y};font-family:PO;font-weight:700;font-size:{40 if story else 34}px;letter-spacing:-.5px">{e(b[0])}</div>'
                   f'<div style="color:#fff;font-family:PO;font-weight:700;font-size:{38 if story else 32}px;letter-spacing:-.5px">{e(b[1])}</div>')
        else:
            txt = f'<div style="color:#fff;font-family:PO;font-weight:700;font-size:{38 if story else 32}px;text-transform:uppercase;letter-spacing:-.5px">{e(b[0])}</div>'
        blocos += (f'<div style="display:flex;gap:22px;align-items:stretch;margin-top:{34 if story else 26}px">'
                   f'<div style="width:5px;border-radius:3px;background:{Y};flex:none"></div><div style="line-height:1.3">{txt}</div></div>')
    logo = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
    fh = int(H * (0.62 if story else 0.66))
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{solido}">
  <img src="file://{foto}" style="position:absolute;left:0;top:0;width:100%;height:{fh}px;object-fit:cover;object-position:{pos};filter:saturate(1.05) contrast(1.04)">
  <div style="position:absolute;left:0;top:0;width:100%;height:{fh + 2}px;background:linear-gradient(180deg,{tint}.25) 0%,{tint}.05) 30%,{tint}.35) 62%,{solido} 100%)"></div>
  <img src="{logo}" style="position:absolute;right:70px;top:{150 if story else 80}px;width:{260 if story else 220}px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.6))">
  <div style="position:absolute;left:80px;right:60px;bottom:{330 if story else 150}px">
    <div style="font-family:EX;font-weight:900;font-style:italic;font-size:{fs_t}px;line-height:1.08;letter-spacing:-1px;text-shadow:0 4px 18px rgba(0,0,0,.55)">{linhas}</div>
    {blocos}
  </div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:{120 if story else 92}px;display:flex;align-items:center;justify-content:space-between;padding:0 70px;box-sizing:border-box;
       font-family:EX;font-weight:800;font-style:italic;font-size:{38 if story else 32}px;color:#fff;background:linear-gradient(90deg,{tint}.95),{tint}.6))">
    <span><span style="color:{Y}">WhatsApp</span> (88) 9.8865-5130</span><span style="font-family:PO;font-weight:500;font-size:{28 if story else 24}px">@liderbateriasepneus</span>
  </div>
</div>'''


def montar_perguntas(cfg, W, H, foto):
    """Layout "DÚVIDAS QUE RECEBEMOS": título centralizado em 2 cores + perguntas em etiquetas amarelas alternando lados."""
    story = H > 1500
    e = html.escape
    tint, solido = CORES.get(cfg.get('cor', 'azul'), CORES['azul'])
    pos = cfg.get('posicao_foto', 'center 40%')
    logo = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
    # título: cada linha é [parte branca, parte amarela]
    tit = ''.join(f'<div>{e(a)} <span style="color:{Y}">{e(b)}</span></div>' for a, b in cfg.get('titulo_duplo', []))
    pergs = cfg.get('perguntas', [])
    n = max(1, len(pergs))
    nl = len(cfg.get('titulo_duplo', []))
    y0 = (290 + 80 * nl + 60) if story else (175 + 69 * nl + 45)
    y1 = 1365 if story else (H - 330)
    passo = (y1 - y0) / max(1, n - 1) if n > 1 else 0
    tags = ''
    for i, q in enumerate(pergs):
        lado = 'left:70px' if i % 2 == 0 else 'right:70px'
        tags += (f'<div style="position:absolute;{lado};top:{int(y0 + i*passo)}px;max-width:{820 if story else 760}px;background:{Y};color:#0B1440;'
                 f'font-family:EX;font-weight:800;font-style:italic;font-size:{40 if story else 34}px;line-height:1.1;padding:{"18px 26px" if story else "14px 22px"};'
                 f'border-radius:8px;box-shadow:0 10px 26px rgba(0,0,0,.45)">{e(q)}</div>')
    cta_a, cta_b = cfg.get('cta', ['Tem dúvida?', 'Chama no zap que a gente responde.'])
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{solido}">
  <img src="file://{foto}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};filter:blur(3px) saturate(1.05);transform:scale(1.03)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,{tint}.92) 0%,{tint}.55) 30%,{tint}.45) 60%,{tint}.92) 100%)"></div>
  <img src="{logo}" style="position:absolute;left:50%;transform:translateX(-50%);top:{150 if story else 60}px;width:{280 if story else 230}px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.5))">
  <div style="position:absolute;left:50px;right:50px;top:{290 if story else 175}px;text-align:center;font-family:EX;font-weight:900;font-style:italic;font-size:{74 if story else 64}px;line-height:1.08;color:#fff;letter-spacing:-1px;text-shadow:0 4px 18px rgba(0,0,0,.5)">{tit}</div>
  {tags}
  <div style="position:absolute;left:60px;right:60px;bottom:{330 if story else 140}px;text-align:center;font-family:PO;font-style:italic;font-size:{42 if story else 36}px;color:#fff;line-height:1.3;text-shadow:0 3px 12px rgba(0,0,0,.6)">
    <b style="font-weight:700">{e(cta_a)}</b> <span style="font-weight:500">{e(cta_b)}</span></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:{120 if story else 92}px;display:flex;align-items:center;justify-content:space-between;padding:0 70px;box-sizing:border-box;
       font-family:EX;font-weight:800;font-style:italic;font-size:{38 if story else 32}px;color:#fff;background:linear-gradient(90deg,{tint}.95),{tint}.6))">
    <span><span style="color:{Y}">WhatsApp</span> (88) 9.8865-5130</span><span style="font-family:PO;font-weight:500;font-size:{28 if story else 24}px">@liderbateriasepneus</span>
  </div>
</div>'''


def main():
    cfg = json.load(open(sys.argv[1]))
    out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    ft = Image.open(os.path.join(RAIZ, cfg['foto'])).convert('RGB')
    if ft.width > 2200: ft = ft.resize((2200, int(ft.height * 2200 / ft.width)), Image.LANCZOS)
    ft = ImageEnhance.Contrast(ft.filter(ImageFilter.UnsharpMask(radius=1.4, percent=80, threshold=2))).enhance(1.05)
    fp = os.path.join(tmp, 'foto.jpg'); ft.save(fp, quality=95)
    jobs = []
    for nome, W, H in (('feed', 1080, 1350), ('story', 1080, 1920)):
        page = f"<!doctype html><html><head><meta charset='utf-8'><style>{fontes()}body{{margin:0}}</style></head><body>{(montar_perguntas if cfg.get('perguntas') else montar_inferior if cfg.get('blocos') else montar)(cfg, W, H, fp)}</body></html>"
        p = os.path.join(tmp, nome + '.html'); open(p, 'w').write(page)
        jobs.append((p, os.path.join(tmp, nome + '.png'), H, os.path.join(out, nome + '.jpg')))
    js = os.path.join(tmp, 'shot.js')
    open(js, 'w').write("""
const { chromium } = require('playwright');
(async () => { const jobs = JSON.parse(process.argv[2]); const b = await chromium.launch();
  for (const [src, png, h] of jobs) { const p = await b.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    await p.screenshot({ path: png }); }
  await b.close(); })();
""")
    subprocess.run(['node', js, json.dumps([j[:3] for j in jobs])], check=True)
    for _, png, _, jpg in jobs:
        im = Image.open(png).convert('RGB'); im.resize((1080, im.height // 2), Image.LANCZOS).save(jpg, quality=95, subsampling=0); print(jpg)


if __name__ == '__main__':
    main()
