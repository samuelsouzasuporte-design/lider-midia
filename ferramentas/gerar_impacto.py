"""Modelo "IMPACTO" da Líder: estilo das artes de referência da loja
(fundo azul-noite, raios, faixas amarelas, título condensado gigante, tarja de destaque,
ícones de benefícios e rodapé com contatos).

Uso: python3 gerar_impacto.py arte.json pasta_saida   -> feed.jpg (1080x1350) e story.jpg (1080x1920)
arte.json:
{
  "foto": "fotos/bateria-carro-01.jpg",   # relativo à raiz do repositório
  "posicao_foto": "center 40%",            # opcional
  "pergunta": "PRECISOU DE BATERIA?",      # linha pequena acima do título (até ~24 letras)
  "linha1": "AQUI TEM",                    # título branco (até ~10 letras)
  "linha2": "BATERIA!",                    # título amarelo (até ~9 letras)
  "destaque": "PRONTA ENTREGA",            # tarja amarela (até ~18 letras)
  "beneficios": ["partida", "rapido", "instalacao"],   # 3 chaves (ver BENEFICIOS)
  "cor": "azul"                            # opcional: "azul" (padrão) ou "preto"
}
"""
import json, os, sys, subprocess, tempfile, html
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
Y = '#FFB800'

ICON = {
    'bolt': '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'wrench': '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 3.4 8 8 9 4.6-1 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    'medal': '<circle cx="12" cy="9" r="6"/><path d="m9 14-2 7 5-3 5 3-2-7"/>',
    'tag': '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    'truck': '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
    'tire': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v5M12 16v5M3 12h5M16 12h5"/>',
}
BENEFICIOS = {
    'partida': ('bolt', 'MAIS', 'PARTIDA'),
    'rapido': ('clock', 'ATENDIMENTO', 'RÁPIDO'),
    'instalacao': ('wrench', 'INSTALAÇÃO EM', 'ATÉ 30 MIN'),
    'qualidade': ('medal', 'PRODUTOS DE', 'QUALIDADE'),
    'marcas': ('tag', 'AS MELHORES', 'MARCAS'),
    'seguranca': ('shield', 'MAIS', 'SEGURANÇA'),
    'durabilidade': ('shield', 'MAIOR', 'DURABILIDADE'),
    'orcamento': ('chat', 'ORÇAMENTO', 'NO WHATSAPP'),
    'linhapesada': ('truck', 'LINHA PESADA', 'CAMINHÕES'),
    'aderencia': ('tire', 'MELHOR', 'ADERÊNCIA'),
    'entrega': ('truck', 'ENTREGA E', 'INSTALAÇÃO GRÁTIS'),
    'parcela': ('tag', 'MOURA EM ATÉ', '10X SEM JUROS'),
}
WA = '<path d="M3.5 20.5l1.3-4A8.5 8.5 0 1 1 8 19.6z"/><path d="M9 8.5c0 3 2.5 6 6 6.5l1.2-1.4-2-1.1-.9.8c-1-.4-2-1.4-2.4-2.4l.8-.9-1.1-2z"/>'
IG = '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".8" fill="currentColor"/>'
PIN = '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'
CHECK = '<path d="M20 6 9 17l-5-5"/>'

def svg(p, size, color, sw=2.2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="color:{color};flex:none">{p}</svg>')

BOLT_BIG = ('<svg viewBox="0 0 200 400" width="{w}" height="{h}" style="position:absolute;{pos};filter:drop-shadow(0 0 18px rgba(255,184,0,.9)) drop-shadow(0 0 40px rgba(255,140,0,.6))">'
            '<path d="M120 0 20 230h70L60 400 190 140h-80z" fill="url(#gb)"/>'
            '<defs><linearGradient id="gb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE14D"/><stop offset="1" stop-color="#FF9500"/></linearGradient></defs></svg>')

def lightning(x, y, w, h, rot, color='#7FB8FF', op=.85):
    # raio "elétrico" ramificado
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 100 300" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg);opacity:{op};'
            f'filter:drop-shadow(0 0 6px {color}) drop-shadow(0 0 16px {color})" fill="none" stroke="#EAF4FF" stroke-width="1.6" stroke-linejoin="round">'
            '<path d="M50 0 L42 40 L58 70 L38 120 L55 150 L30 210 L48 240 L35 300"/>'
            '<path d="M58 70 L80 95 L72 120 L92 150"/><path d="M38 120 L15 140 L22 165"/><path d="M30 210 L10 230"/></svg>')

def fontes():
    f = os.path.join(AQUI, 'fontes')
    css = ''
    for w, st in ((600, 'normal'), (700, 'normal'), (700, 'italic'), (800, 'italic'), (900, 'italic')):
        css += f"@font-face{{font-family:'BC';font-weight:{w};font-style:{st};src:url('file://{f}/barlow-condensed-latin-{w}-{st}.woff2')}}\n"
    for w in (500, 600, 700):
        css += f"@font-face{{font-family:'Inter';font-weight:{w};font-style:normal;src:url('file://{f}/inter-latin-{w}-normal.woff2')}}\n"
    return css

def montar(cfg, W, H):
    e = lambda k, d='': html.escape(cfg.get(k, d))
    foto = 'file://' + os.path.join(RAIZ, cfg['foto'])
    logo = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
    pos = cfg.get('posicao_foto', 'center 40%')
    preto = cfg.get('cor') == 'preto'
    bg1, bg2 = ('#0B0C10', '#020203') if preto else ('#0C1A4A', '#040817')
    tint = 'rgba(4,8,23,' if not preto else 'rgba(2,2,3,'
    story = H > 1500
    # medidas
    fh = int(H * (0.62 if story else 0.60))          # altura da foto
    t_kick = 340 if story else 205
    s_l1 = 178 if story else 138
    s_l2 = 200 if story else 152
    ben_top = H - (560 if story else 300)
    bens = ''
    for k in cfg.get('beneficios', ['partida', 'rapido', 'instalacao'])[:3]:
        ic, a, b = BENEFICIOS.get(k, BENEFICIOS['qualidade'])
        bens += (f'<div style="display:flex;align-items:center;gap:16px;flex:1;min-width:0">'
                 f'<div style="width:{84 if story else 70}px;height:{84 if story else 70}px;border-radius:50%;border:4px solid {Y};display:flex;align-items:center;justify-content:center;flex:none;box-shadow:0 0 18px rgba(255,184,0,.35)">{svg(ICON[ic], 44 if story else 36, Y, 2.3)}</div>'
                 f'<div style="font-family:BC;font-style:italic;line-height:1.02;color:#fff"><div style="font-weight:700;font-size:{28 if story else 24}px">{a}</div>'
                 f'<div style="font-weight:900;font-size:{34 if story else 28}px;color:{Y}">{b}</div></div></div>')
    sep = '<div style="width:2px;align-self:stretch;background:rgba(255,184,0,.35)"></div>'
    bens = sep.join(bens.split('</div></div></div>')[:-1])  # placeholder (substituído abaixo)
    # reconstrói com separadores
    items = []
    for k in cfg.get('beneficios', ['partida', 'rapido', 'instalacao'])[:3]:
        ic, a, b = BENEFICIOS.get(k, BENEFICIOS['qualidade'])
        items.append(f'<div style="display:flex;align-items:center;gap:14px;flex:1;min-width:0">'
                     f'<div style="width:{84 if story else 68}px;height:{84 if story else 68}px;border-radius:50%;border:4px solid {Y};display:flex;align-items:center;justify-content:center;flex:none;box-shadow:0 0 18px rgba(255,184,0,.35)">{svg(ICON[ic], 44 if story else 34, Y, 2.3)}</div>'
                     f'<div style="font-family:BC;font-style:italic;line-height:1.02;color:#fff"><div style="font-weight:700;font-size:{28 if story else 23}px">{a}</div>'
                     f'<div style="font-weight:900;font-size:{34 if story else 27}px;color:{Y}">{b}</div></div></div>')
    bens = sep.join(items)

    if story:
        rodape = f'''
  <div style="position:absolute;left:60px;right:60px;top:{H-370}px;display:flex;align-items:center;gap:22px;background:linear-gradient(90deg,{Y},#FFCC33);border-radius:26px;padding:22px 34px;box-shadow:0 10px 40px rgba(255,184,0,.35)">
    {svg(WA, 72, '#111', 2)}
    <div><div style="font-family:BC;font-weight:700;font-size:30px;color:#111;letter-spacing:1px">CHAMA NO WHATSAPP</div>
    <div style="font-family:BC;font-weight:900;font-style:italic;font-size:76px;line-height:.95;color:#111">(88) 9.8865-5130</div></div>
  </div>
  <div style="position:absolute;left:60px;right:60px;top:{H-200}px;display:flex;justify-content:space-between;align-items:center;font-family:Inter;font-weight:600;font-size:27px;color:#E8ECF6">
    <div style="display:flex;align-items:center;gap:10px">{svg(PIN, 30, Y)}Rua Deolino Barreto, 860 - Centro</div>
    <div style="display:flex;align-items:center;gap:10px">{svg(IG, 30, Y)}@liderbateriasepneus</div>
  </div>'''
    else:
        rodape = f'''
  <div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:linear-gradient(90deg,{Y},#FFCC33);display:flex;align-items:center;justify-content:space-between;padding:0 54px;box-sizing:border-box">
    <div style="display:flex;align-items:center;gap:16px">{svg(WA, 60, '#111', 2)}
      <div><div style="font-family:BC;font-weight:700;font-size:24px;color:#111;letter-spacing:1px">CHAMA NO WHATSAPP</div>
      <div style="font-family:BC;font-weight:900;font-style:italic;font-size:58px;line-height:.95;color:#111;white-space:nowrap">(88) 9.8865-5130</div></div></div>
    <div style="text-align:right;font-family:Inter;font-weight:700;font-size:22px;color:#111;line-height:1.5;white-space:nowrap">
      <div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">{svg(PIN, 24, '#111')}Rua Deolino Barreto, 860 - Centro, Crateús/CE</div>
      <div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">{svg(IG, 24, '#111')}@liderbateriasepneus</div></div>
  </div>'''

    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:radial-gradient(120% 80% at 70% 30%,{bg1} 0%,{bg2} 70%);font-family:Inter">
  <img src="{foto}" style="position:absolute;left:0;top:{int(H*0.16) if story else int(H*0.13)}px;width:{W}px;height:{fh}px;object-fit:cover;object-position:{pos};filter:saturate(1.15) contrast(1.05)">
  <div style="position:absolute;left:0;top:{int(H*0.16) if story else int(H*0.13)}px;width:{W}px;height:{fh}px;background:linear-gradient(180deg,{tint}1) 0%,{tint}.25) 30%,{tint}.15) 55%,{tint}1) 100%)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,{tint}.85) 0%,{tint}.25) 60%,{tint}0) 100%)"></div>
  <!-- faixas amarelas -->
  <div style="position:absolute;right:-160px;top:-60px;width:520px;height:46px;background:{Y};transform:rotate(-38deg);opacity:.95"></div>
  <div style="position:absolute;right:-120px;top:40px;width:420px;height:14px;background:{Y};transform:rotate(-38deg);opacity:.7"></div>
  <div style="position:absolute;left:-140px;top:{ben_top-100}px;width:400px;height:26px;background:{Y};transform:rotate(-22deg);opacity:.85"></div>
  <div style="position:absolute;left:-140px;top:{ben_top-64}px;width:280px;height:9px;background:{Y};transform:rotate(-22deg);opacity:.6"></div>
  {lightning(W-210, int(H*0.30), 150, 450, 18)}
  {lightning(40, int(H*0.42), 110, 330, -12, '#8CC4FF', .6)}
  {BOLT_BIG.format(w=150 if story else 110, h=300 if story else 220, pos=f"right:60px;top:{int(H*0.50)}px")}
  <img src="{logo}" style="position:absolute;left:56px;top:{110 if story else 48}px;width:{400 if story else 300}px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))">
  <div style="position:absolute;left:60px;right:60px;top:{t_kick}px">
    <div style="display:flex;align-items:center;gap:12px;font-family:BC;font-weight:800;font-style:italic;font-size:{62 if story else 48}px;color:#fff;letter-spacing:.5px;text-shadow:0 4px 18px rgba(0,0,0,.7)">{e('pergunta')}{svg(ICON['bolt'], 54 if story else 42, Y, 2.4)}</div>
    <div style="font-family:BC;font-weight:900;font-style:italic;text-transform:uppercase;line-height:.86;margin-top:6px">
      <div style="font-size:{s_l1}px;color:#fff;text-shadow:0 6px 24px rgba(0,0,0,.75)">{e('linha1')}</div>
      <div style="font-size:{s_l2}px;color:{Y};text-shadow:0 0 30px rgba(255,184,0,.35),0 6px 24px rgba(0,0,0,.8)">{e('linha2')}</div>
    </div>
    <div style="display:inline-flex;align-items:center;gap:14px;margin-top:22px;background:{Y};color:#0B0B0B;padding:{'14px 34px' if story else '10px 26px'};border-radius:16px;transform:skewX(-10deg) rotate(-2deg);box-shadow:0 10px 30px rgba(0,0,0,.5)">
      <div style="width:{50 if story else 40}px;height:{50 if story else 40}px;border-radius:50%;background:#0B0B0B;display:flex;align-items:center;justify-content:center">{svg(CHECK, 30 if story else 24, Y, 3.4)}</div>
      <span style="font-family:BC;font-weight:900;font-style:italic;font-size:{58 if story else 44}px;letter-spacing:.5px">{e('destaque')}</span>
    </div>
  </div>
  <div style="position:absolute;left:50px;right:50px;top:{ben_top}px;display:flex;gap:18px;align-items:center;background:rgba(5,9,25,.78);border:2px solid rgba(255,184,0,.45);border-radius:24px;padding:{'26px 26px' if story else '18px 20px'}">{bens}</div>
  {rodape}
</div>'''

def main():
    cfg = json.load(open(sys.argv[1]))
    out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(); jobs = []
    for nome, W, H in (('feed', 1080, 1350), ('story', 1080, 1920)):
        page = f"<!doctype html><html><head><meta charset='utf-8'><style>{fontes()}body{{margin:0}}</style></head><body>{montar(cfg, W, H)}</body></html>"
        p = os.path.join(tmp, nome + '.html'); open(p, 'w').write(page)
        jobs.append((p, os.path.join(tmp, nome + '.png'), H, os.path.join(out, nome + '.jpg')))
    js = os.path.join(tmp, 'shot.js')
    open(js, 'w').write("""
const { chromium } = require('playwright');
(async () => { const jobs = JSON.parse(process.argv[2]); const b = await chromium.launch();
  for (const [src, png, h] of jobs) { const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    await p.screenshot({ path: png }); }
  await b.close(); })();
""")
    subprocess.run(['node', js, json.dumps([j[:3] for j in jobs])], check=True)
    for _, png, _, jpg in jobs:
        Image.open(png).convert('RGB').save(jpg, quality=93); print(jpg)

if __name__ == '__main__':
    main()
