import os, base64
R=os.path.abspath('../../..'); F=R+'/ferramentas/fontes'; D=os.getcwd()
css=''
for w,st in ((700,'normal'),(900,'italic')): css+=f"@font-face{{font-family:BC;font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}"
for w in (500,700): css+=f"@font-face{{font-family:Inter;font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}"
ZAP='<svg viewBox="0 0 24 24" fill="#0c0c32"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
def html(W,H,aw,atop,bandtop,story):
    ah=int(aw*724/579); al=(W-aw)//2
    top=(f'<div style="position:absolute;top:60px;left:0;right:0;text-align:center"><img src="file://{R}/marca/logo.png" style="width:380px"><div style="font:700 30px BC;letter-spacing:6px;color:#ffd400;margin-top:6px">PARCEIRO MOURA FÁCIL EM CRATEÚS</div></div>' if story else '')
    return f"""<html><head><meta charset=utf-8><style>{css}*{{margin:0;padding:0}}body{{width:{W}px;height:{H}px;overflow:hidden;background:linear-gradient(180deg,#0c0c32,#16137a 60%,#0c0c32);position:relative;font-family:Inter;color:#fff}}</style></head><body>
{top}<img src="file://{D}/original.jpg" style="position:absolute;left:{al}px;top:{atop}px;width:{aw}px;height:{ah}px;border-radius:{24 if story else 0}px;box-shadow:0 20px 60px rgba(0,0,0,.5)">
<div style="position:absolute;left:0;right:0;top:{bandtop}px;bottom:0;display:flex;align-items:center;justify-content:{'center' if story else 'space-between'};gap:30px;padding:0 50px;{'flex-direction:column' if story else ''}">
{'' if story else f'<div><img src="file://{R}/marca/logo.png" style="width:300px;display:block"><div style="font:700 22px BC;letter-spacing:4px;color:#ffd400;margin-top:4px">PARCEIRO MOURA FÁCIL EM CRATEÚS</div></div>'}
<div style="background:#ffd400;color:#0c0c32;border-radius:20px;padding:14px 28px;display:flex;align-items:center;gap:16px"><div style="width:{60 if story else 50}px">{ZAP}</div><div><div style="font:700 {24 if story else 20}px BC;letter-spacing:3px">CHAMA NO ZAP DA LÍDER</div><div style="font:italic 900 {64 if story else 52}px/1 BC">(88) 9.8865-5130</div></div></div>
{'<div style="font:500 26px Inter;color:#b9bde0">Rua Deolino Barreto, 860 - Centro · Crateús/CE</div>' if story else ''}</div></body></html>"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,(W,H,aw,atop,bt,st) in {'feed':(1080,1350,914,0,1143,False),'story':(1080,1920,960,300,1500,True)}.items():
        open(n+'.html','w').write(html(W,H,aw,atop,bt,st)); pg=b.new_page(viewport={'width':W,'height':H}); pg.goto('file://'+D+'/'+n+'.html'); pg.wait_for_timeout(500); pg.screenshot(path=n+'.jpg',type='jpeg',quality=94)
    b.close()
