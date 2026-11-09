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
  "cor": "azul"                          # azul | noite | grafite | royal
}
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
    top = 360 if story else 225
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{solido}">
  <img src="file://{foto}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};filter:saturate(1.05)">
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,{tint}.96) 0%,{tint}.88) 38%,{tint}.45) 68%,{tint}.10) 100%)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,{tint}.55) 0%,{tint}0) 22%,{tint}0) 70%,{tint}.75) 100%)"></div>
  <img src="{logo}" style="position:absolute;left:70px;top:{150 if story else 70}px;width:{300 if story else 250}px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.5))">
  {selo_html}
  <div style="position:absolute;left:70px;right:90px;top:{top}px">
    <div style="font-family:EX;font-weight:900;font-style:italic;font-size:{fs_t}px;line-height:1.1;letter-spacing:-1px;text-shadow:0 4px 18px rgba(0,0,0,.45)">{linhas}</div>
    <div style="margin-top:{34 if story else 26}px;font-family:PO;font-weight:700;font-style:italic;font-size:{44 if story else 38}px;line-height:1.25;color:#fff;max-width:{760 if story else 700}px;text-shadow:0 3px 12px rgba(0,0,0,.5)">{e(cfg.get('subtitulo', ''))}</div>
    <svg width="{40 if story else 34}" height="{24 if story else 20}" viewBox="0 0 24 14" style="margin-top:18px" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l9 8 9-8"/></svg>
  </div>
  <div style="position:absolute;left:{110 if story else 100}px;bottom:{330 if story else 150}px;display:flex;gap:28px;align-items:stretch">
    <div style="width:7px;border-radius:4px;background:{Y}"></div>
    <div style="font-family:EX;font-weight:600;font-size:{50 if story else 44}px;line-height:1.32;color:#fff;text-shadow:0 3px 12px rgba(0,0,0,.6)">{lista}</div>
  </div>
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
        page = f"<!doctype html><html><head><meta charset='utf-8'><style>{fontes()}body{{margin:0}}</style></head><body>{montar(cfg, W, H, fp)}</body></html>"
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
