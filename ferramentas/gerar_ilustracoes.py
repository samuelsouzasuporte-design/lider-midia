"""Gera ilustrações próprias (sem marcas de terceiros) para usar como 'foto' quando as fotos reais
estiverem repetindo. Saída: fotos/ilustracoes/*.jpg (1600x2133)."""
import os, subprocess, json, tempfile, math, random
from PIL import Image
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
OUT = os.path.join(RAIZ, 'fotos', 'ilustracoes'); os.makedirs(OUT, exist_ok=True)
W, H = 1600, 2133
random.seed(7)

def bg(c1, c2):
    return f'<defs><radialGradient id="g" cx="50%" cy="40%" r="80%"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>' \
           '<linearGradient id="y" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFD84D"/><stop offset="1" stop-color="#FF8A00"/></linearGradient>' \
           '<filter id="b"><feGaussianBlur stdDeviation="40"/></filter><filter id="s"><feGaussianBlur stdDeviation="8"/></filter></defs>' \
           f'<rect width="{W}" height="{H}" fill="url(#g)"/>'

def pneu(cx, cy, r, sidew=0.62):
    # pneu de frente, banda de rodagem com sulcos
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#121316"/>'
    for i in range(48):
        a = i * 2 * math.pi / 48
        x1, y1 = cx + r * 0.86 * math.cos(a), cy + r * 0.86 * math.sin(a)
        x2, y2 = cx + r * 0.99 * math.cos(a + .05), cy + r * 0.99 * math.sin(a + .05)
        s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#2C2F36" stroke-width="{r*0.05:.0f}" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.84}" fill="#1B1D22" stroke="#2E3138" stroke-width="6"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*sidew}" fill="#2A2D33"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*sidew*0.92}" fill="url(#rim)"/>'
    for i in range(5):
        a = i * 2 * math.pi / 5 - math.pi / 2
        s += f'<path d="M{cx} {cy} L{cx + r*sidew*0.85*math.cos(a-0.22):.0f} {cy + r*sidew*0.85*math.sin(a-0.22):.0f} L{cx + r*sidew*0.85*math.cos(a+0.22):.0f} {cy + r*sidew*0.85*math.sin(a+0.22):.0f}Z" fill="#9AA0A8" opacity=".9"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.12}" fill="#C9CED4"/>'
    return s
RIM = '<defs><radialGradient id="rim"><stop offset="0" stop-color="#5A5F67"/><stop offset="1" stop-color="#2F3238"/></radialGradient></defs>'

def bateria(x, y, w, h):
    d = h * 0.25
    s = f'<polygon points="{x+w},{y} {x+w+d},{y-d*0.7} {x+w+d},{y+h-d*0.7} {x+w},{y+h}" fill="#0E0F12"/>'
    s += f'<polygon points="{x},{y} {x+d},{y-d*0.7} {x+w+d},{y-d*0.7} {x+w},{y}" fill="#3A3E46"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1D1F24"/>'
    s += f'<rect x="{x}" y="{y+h*0.28}" width="{w}" height="{h*0.42}" fill="url(#y)"/>'
    s += f'<path d="M{x+w*0.52} {y+h*0.31} L{x+w*0.4} {y+h*0.52} L{x+w*0.5} {y+h*0.52} L{x+w*0.44} {y+h*0.68} L{x+w*0.62} {y+h*0.45} L{x+w*0.52} {y+h*0.45} L{x+w*0.58} {y+h*0.31}Z" fill="#111"/>'
    for tx, c, sg in ((x + w * 0.18, '#D7263D', '+'), (x + w * 0.74, '#2B2E35', '−')):
        s += f'<rect x="{tx}" y="{y-d*0.7-40}" width="{w*0.1}" height="50" rx="8" fill="#C9CED4"/>'
        s += f'<circle cx="{tx+w*0.05}" cy="{y-d*0.7-90}" r="34" fill="{c}"/><text x="{tx+w*0.05}" y="{y-d*0.7-74}" font-family="Arial Black" font-size="46" fill="#fff" text-anchor="middle">{sg}</text>'
    return s

def raios(n=7):
    s = ''
    for _ in range(n):
        x = random.randint(100, W - 100); y = random.randint(150, H - 300); pts = [(x, y)]
        for k in range(7): x += random.randint(-70, 70); y += random.randint(60, 120); pts.append((x, y))
        p = ' '.join(f'{a},{b}' for a, b in pts)
        s += f'<polyline points="{p}" fill="none" stroke="#CFE6FF" stroke-width="4" opacity=".55" filter="url(#s)"/><polyline points="{p}" fill="none" stroke="#FFFFFF" stroke-width="2" opacity=".8"/>'
    return s


def trator_cena():
    # trator genérico (sem marca), visto de lado, no campo ao entardecer — para posts de linha pesada/agro
    sky = ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1640"/><stop offset=".55" stop-color="#23306B"/>'
           '<stop offset=".72" stop-color="#C2562A"/><stop offset=".8" stop-color="#F29A3A"/><stop offset="1" stop-color="#1A1206"/></linearGradient>'
           '<linearGradient id="y" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFD84D"/><stop offset="1" stop-color="#FF8A00"/></linearGradient>'
           '<linearGradient id="corpo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A4D8F"/><stop offset="1" stop-color="#16214A"/></linearGradient>'
           '<filter id="b"><feGaussianBlur stdDeviation="40"/></filter><filter id="s"><feGaussianBlur stdDeviation="8"/></filter></defs>')
    s = sky + f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<rect y="1700" width="{W}" height="{H-1700}" fill="#120D07"/>'
    for i in range(14):
        y = 1720 + i * 32
        s += f'<path d="M0 {y} Q 800 {y-30+i*3} {W} {y}" stroke="#2A1E10" stroke-width="{6+i}" fill="none"/>'
    s += '<ellipse cx="820" cy="1880" rx="720" ry="70" fill="#000" opacity=".75" filter="url(#b)"/>'
    def roda(cx, cy, r):
        t = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0C0D10"/>'
        for i in range(22):
            a = i * 2 * math.pi / 22
            x1, y1 = cx + r * .9 * math.cos(a), cy + r * .9 * math.sin(a)
            x2, y2 = cx + r * 1.02 * math.cos(a + .12), cy + r * 1.02 * math.sin(a + .12)
            t += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#23252B" stroke-width="{r*.12:.0f}" stroke-linecap="round"/>'
        t += f'<circle cx="{cx}" cy="{cy}" r="{r*.55}" fill="#E0A21F"/><circle cx="{cx}" cy="{cy}" r="{r*.42}" fill="#B07A10"/><circle cx="{cx}" cy="{cy}" r="{r*.14}" fill="#2A2A2A"/>'
        for i in range(8):
            a = i * 2 * math.pi / 8
            t += f'<circle cx="{cx + r*.3*math.cos(a):.0f}" cy="{cy + r*.3*math.sin(a):.0f}" r="{r*.035:.0f}" fill="#3A2A08"/>'
        return t
    # chassi e capô
    s += '<rect x="700" y="1330" width="640" height="210" rx="28" fill="url(#corpo)"/>'
    s += '<rect x="700" y="1330" width="640" height="26" rx="12" fill="#5B70B8" opacity=".8"/>'
    for i in range(6):
        s += f'<rect x="{1180+i*24}" y="1380" width="10" height="120" rx="4" fill="#0E1330"/>'
    s += '<rect x="1320" y="1360" width="60" height="150" rx="14" fill="#1B2550"/><circle cx="1360" cy="1395" r="20" fill="#FFE9A8"/>'
    # escapamento
    s += '<rect x="1040" y="1120" width="34" height="220" rx="12" fill="#2B2F38"/><rect x="1032" y="1100" width="50" height="40" rx="10" fill="#3A3F4A"/>'
    # cabine
    s += '<path d="M420 1360 L470 920 L860 920 L900 1360Z" fill="#0F1736"/>'
    s += '<path d="M470 960 L500 960 L520 1330 L460 1330Z" fill="#26346E"/><path d="M820 960 L850 960 L880 1330 L830 1330Z" fill="#26346E"/>'
    s += '<path d="M505 965 L815 965 L845 1320 L520 1320Z" fill="#7FA2D6" opacity=".35"/>'
    s += '<rect x="430" y="880" width="470" height="60" rx="18" fill="url(#corpo)"/>'
    s += '<rect x="390" y="1330" width="360" height="120" rx="20" fill="url(#corpo)"/>'
    s += roda(600, 1560, 330) + roda(1210, 1665, 195)
    # luz de fim de tarde no contorno
    s += '<path d="M430 880 L900 880" stroke="#FFB15A" stroke-width="6" opacity=".7"/><path d="M700 1330 L1340 1330" stroke="#FFB15A" stroke-width="5" opacity=".6"/>'
    # bateria em destaque no chão
    s += '<circle cx="330" cy="1830" r="260" fill="url(#y)" opacity=".18" filter="url(#b)"/>'
    s += bateria(130, 1720, 380, 260)
    return s

arts = {
  'ilustracao-pneu-carro': bg('#2A3A6A', '#070B18') + RIM + f'<ellipse cx="800" cy="1950" rx="700" ry="90" fill="#000" opacity=".7" filter="url(#b)"/>' + pneu(800, 1200, 640) + raios(4),
  'ilustracao-pneus-pilha': bg('#3A2A70', '#0A0618') + RIM + ''.join(pneu(420 + 760 * (i % 2), 700 + 620 * (i // 2), 380) for i in range(4)),
  'ilustracao-bateria-carro': bg('#1B3F9E', '#050A1E') + '<ellipse cx="800" cy="1600" rx="650" ry="80" fill="#000" opacity=".7" filter="url(#b)"/>' + bateria(330, 900, 860, 640) + raios(6),
  'ilustracao-energia': bg('#4A2A10', '#080402') + '<circle cx="800" cy="1000" r="520" fill="url(#y)" opacity=".25" filter="url(#b)"/>' +
      '<path d="M920 300 L500 1150 L780 1150 L640 1850 L1120 900 L840 900 L1000 300Z" fill="url(#y)"/>' + raios(9),
  'ilustracao-regiao': bg('#123B3A', '#030A0A') + ''.join(f'<path d="M{random.randint(0,W)} {random.randint(0,H)} Q {random.randint(0,W)} {random.randint(0,H)} {random.randint(0,W)} {random.randint(0,H)}" stroke="#2F6F6A" stroke-width="{random.choice([8,14,22])}" fill="none" opacity=".7"/>' for _ in range(14)) +
      '<path d="M800 1500 C 560 1150 470 980 470 820 A 330 330 0 1 1 1130 820 C 1130 980 1040 1150 800 1500Z" fill="url(#y)"/><circle cx="800" cy="820" r="140" fill="#0A1A1A"/>',
  'ilustracao-trator': trator_cena(),
}
if os.environ.get('SO'):
    arts = {k: v for k, v in arts.items() if k in os.environ['SO'].split(',')}
tmp = tempfile.mkdtemp(); jobs = []
for nome, body in arts.items():
    p = f'{tmp}/{nome}.html'
    open(p, 'w').write(f'<!doctype html><html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg></body></html>')
    jobs.append((p, f'{tmp}/{nome}.png', os.path.join(OUT, nome + '.jpg')))
js = f'{tmp}/s.js'; open(js, 'w').write("""const { chromium } = require('playwright');
(async () => { const j = JSON.parse(process.argv[2]); const b = await chromium.launch();
for (const [s, o] of j) { const p = await b.newPage({ viewport: { width: 1600, height: 2133 } }); await p.goto('file://' + s); await p.screenshot({ path: o }); } await b.close(); })();""")
subprocess.run(['node', js, json.dumps([j[:2] for j in jobs])], check=True)
for _, png, jpg in jobs:
    Image.open(png).convert('RGB').save(jpg, quality=93); print(jpg)
