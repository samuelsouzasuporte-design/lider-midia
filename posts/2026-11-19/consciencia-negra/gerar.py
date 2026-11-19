import os, sys, asyncio
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
F = os.path.join(RAIZ, 'ferramentas', 'fontes')
OUT = os.path.dirname(os.path.abspath(__file__))
foto = 'file://' + os.path.join(RAIZ, 'fotos', 'loja-fachada-04.jpg')
logo = 'file://' + os.path.join(RAIZ, 'marca', 'logo.png')
css_f = ''
for w, st in ((600,'normal'),(700,'normal'),(700,'italic'),(800,'italic'),(900,'italic')):
    css_f += f"@font-face{{font-family:'BC';font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}\n"
for w in (500,600,700):
    css_f += f"@font-face{{font-family:'Inter';font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}\n"
HTML = f"""<!doctype html><html><head><meta charset=utf-8><style>{css_f}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:#070b1c;font-family:Inter;color:#fff;position:relative}}
.bg{{position:absolute;inset:0;background:url('{foto}') center 40%/cover;filter:saturate(.7) brightness(.55)}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,11,28,.55) 0%,rgba(7,11,28,.35) 18%,rgba(7,11,28,.88) 40%,#070b1c 62%)}}
.gold{{position:absolute;left:0;right:0;top:0;height:12px;background:linear-gradient(90deg,#ffd400,#f5a400)}}
.logo{{position:absolute;top:110px;left:0;right:0;text-align:center}} .logo img{{width:430px}}
.tag{{position:absolute;top:440px;left:0;right:0;text-align:center}}
.tag span{{display:inline-block;border:3px solid #ffd400;color:#ffd400;font:700 44px BC;letter-spacing:6px;padding:10px 34px;border-radius:60px}}
h1{{position:absolute;top:535px;left:40px;right:40px;text-align:center;font:italic 900 118px/0.9 BC;text-transform:uppercase}}
h1 b{{color:#ffd400}}
.frase{{position:absolute;top:880px;left:110px;right:110px;text-align:center;font:500 38px/1.35 Inter;color:#d6dbea}}
.card{{position:absolute;top:1040px;left:70px;right:70px;background:rgba(255,255,255,.06);border:2px solid rgba(255,212,0,.55);border-radius:34px;padding:36px 50px}}
.card h2{{font:700 40px BC;letter-spacing:5px;color:#ffd400;text-align:center;margin-bottom:30px}}
.row{{display:flex;align-items:center;gap:30px;padding:24px 0}}
.row+.row{{border-top:2px solid rgba(255,255,255,.12)}}
.ic{{flex:0 0 108px;height:108px;border-radius:50%;background:#ffd400;display:flex;align-items:center;justify-content:center}}
.ic svg{{width:58px;height:58px}}
.t1{{font:italic 800 70px/1 BC;text-transform:uppercase}}
.t2{{font:500 34px Inter;color:#c9cfe0;margin-top:6px}}
.zap{{position:absolute;top:1580px;left:70px;right:70px;background:#ffd400;color:#070b1c;border-radius:30px;padding:26px 40px;display:flex;align-items:center;gap:26px}}
.zap svg{{width:80px;height:80px}}
.zap .a{{font:700 32px BC;letter-spacing:3px}} .zap .b{{font:italic 900 78px/1 BC}}
.end{{position:absolute;top:1800px;left:0;right:0;text-align:center;font:500 30px Inter;color:#aeb5c9}}
</style></head><body><div class=bg></div><div class=sh></div><div class=gold></div>
<div class=logo><img src="{logo}"></div>
<div class=tag><span>20 DE NOVEMBRO</span></div>
<h1>Dia da<br><b>Consciência<br>Negra</b></h1>
<div class=frase>Um dia para lembrar, respeitar e valorizar a história e a força do povo negro.</div>
<div class=card><h2>NOSSO HORÁRIO NO FERIADO</h2>
 <div class=row><div class=ic><svg viewBox="0 0 24 24" fill="none" stroke="#070b1c" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
  <div><div class=t1>Das 07h às 12h</div><div class=t2>Loja aberta na parte da manhã</div></div></div>
 <div class=row><div class=ic><svg viewBox="0 0 24 24" fill="#070b1c"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg></div>
  <div><div class=t1>À tarde: plantão</div><div class=t2>Atendimento on-line pelo WhatsApp</div></div></div>
</div>
<div class=zap><svg viewBox="0 0 24 24" fill="#070b1c"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>
 <div><div class=a>CHAMA NO ZAP</div><div class=b>(88) 9.8865-5130</div></div></div>
<div class=end>Rua Deolino Barreto, 860 - Centro · Crateús/CE</div>
</body></html>"""
from playwright.sync_api import sync_playwright
open(os.path.join(OUT,'story.html'),'w').write(HTML)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+os.path.join(OUT,'story.html')); pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(OUT,'story.jpg'), type='jpeg', quality=93); b.close()
print('ok')
