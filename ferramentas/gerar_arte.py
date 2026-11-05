"""Gera as artes da Líder (feed 1080x1350 e story 1080x1920) a partir de um JSON.

Uso: python3 gerar_arte.py arte.json pasta_saida
arte.json:
{
  "foto": "fotos/parede-pneus.jpg",        # caminho relativo à raiz do repositório
  "selo": "PRONTA ENTREGA",                 # pílula amarela no topo (curta)
  "chamada": "ESTOQUE COMPLETO",            # linha amarela acima do título
  "linha1": "Pneus e",                      # título branco (curto, 1-2 palavras)
  "linha2": "baterias",                     # título amarelo (1 palavra, até ~9 letras no feed)
  "subtitulo": "Para carros e motos, das melhores marcas.",
  "posicao_foto": "center 35%"              # opcional: object-position da foto
}
Saída: feed.jpg e story.jpg na pasta_saida.
Requer: playwright (node) com chromium já instalado, Pillow.
"""
import json, os, sys, subprocess, tempfile, html
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

def fontes():
    f = os.path.join(AQUI, 'fontes')
    css = ''
    for w, st in ((600, 'normal'), (800, 'normal'), (700, 'italic'), (800, 'italic'), (900, 'italic')):
        css += f"@font-face{{font-family:'Exo 2';font-weight:{w};font-style:{st};src:url('file://{f}/exo-2-latin-{w}-{st}.woff2')}}\n"
    for w in (500, 600, 700):
        css += f"@font-face{{font-family:'Inter';font-weight:{w};font-style:normal;src:url('file://{f}/inter-latin-{w}-normal.woff2')}}\n"
    return css

def main():
    cfg = json.load(open(sys.argv[1]))
    out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
    foto = os.path.join(RAIZ, cfg['foto'])
    vals = {
        '{{FOTO}}': 'file://' + foto,
        '{{LOGO}}': 'file://' + os.path.join(RAIZ, 'marca', 'logo.png'),
        '{{SELO}}': html.escape(cfg.get('selo', 'PRONTA ENTREGA')),
        '{{CHAMADA}}': html.escape(cfg.get('chamada', '')),
        '{{LINHA1}}': html.escape(cfg['linha1']),
        '{{LINHA2}}': html.escape(cfg['linha2']),
        '{{SUBTITULO}}': html.escape(cfg.get('subtitulo', '')),
    }
    tmp = tempfile.mkdtemp()
    jobs = []
    for nome, modelo, h in (('feed', 'modelo_feed.html', 1350), ('story', 'modelo_story.html', 1920)):
        body = open(os.path.join(AQUI, modelo)).read()
        for k, v in vals.items():
            body = body.replace(k, v)
        if cfg.get('posicao_foto'):
            body = body.replace('object-position: center 35%', 'object-position: ' + cfg['posicao_foto'])
            body = body.replace('object-position: center 40%', 'object-position: ' + cfg['posicao_foto'])
        page = f"<!doctype html><html><head><meta charset='utf-8'><style>{fontes()}body{{margin:0}}</style></head><body>{body}</body></html>"
        p = os.path.join(tmp, nome + '.html'); open(p, 'w').write(page)
        jobs.append((p, os.path.join(tmp, nome + '.png'), h, os.path.join(out, nome + '.jpg')))
    js = os.path.join(tmp, 'shot.js')
    open(js, 'w').write("""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch();
  for (const [src, png, h] of jobs) {
    const p = await b.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + src);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(400);
    await p.screenshot({ path: png });
  }
  await b.close();
})();
""")
    subprocess.run(['node', js, json.dumps([j[:3] for j in jobs])], check=True)
    for _, png, _, jpg in jobs:
        Image.open(png).convert('RGB').resize((1080, Image.open(png).height // 2), Image.LANCZOS).save(jpg, quality=95, subsampling=0)
        print(jpg)

if __name__ == '__main__':
    main()
