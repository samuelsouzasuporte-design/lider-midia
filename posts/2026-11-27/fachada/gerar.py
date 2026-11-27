import os
R=os.path.abspath('../../..'); F=R+'/ferramentas/fontes'; D=os.getcwd()
foto=f"file://{R}/fotos/loja-fachada-05-moto-entrega.jpg"
css=''
for w,st in ((700,'normal'),(800,'italic'),(900,'italic')): css+=f"@font-face{{font-family:BC;font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}"
for w in (500,600): css+=f"@font-face{{font-family:Inter;font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}"
ZAP='<svg viewBox="0 0 24 24" fill="#071233"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
def page(W,H,ph,crop_top,s,extra):
    return f"""<html><head><meta charset=utf-8><style>{css}*{{margin:0;padding:0}}body{{width:{W}px;height:{H}px;overflow:hidden;background:#071233;position:relative;color:#fff;font-family:Inter}}
.ph{{position:absolute;left:0;top:0;width:{W}px;height:{ph}px;background:url('{foto}') 50% {crop_top}/cover}}
.ph:after{{content:'';position:absolute;left:0;right:0;bottom:0;height:{int(ph*.35)}px;background:linear-gradient(180deg,rgba(7,18,51,0),#071233)}}
.pn{{position:absolute;left:{60*s}px;right:{60*s}px;top:{ph-(70 if s<1 else 140)*s}px}}
.tag{{display:inline-block;background:#ffd400;color:#071233;font:700 {28*s}px BC;letter-spacing:{4*s}px;padding:{6*s}px {16*s}px;border-radius:{8*s}px}}
h1{{font:italic 900 {100*s}px/.9 BC;text-transform:uppercase;margin-top:{14*s}px;text-shadow:0 4px 20px rgba(0,0,0,.4)}} h1 b{{color:#ffd400}}
.sub{{font:500 {31*s}px/1.35 Inter;color:#d3d9ec;margin-top:{14*s}px}}
.zap{{position:absolute;left:{60*s}px;right:{60*s}px;bottom:{70*s}px;display:flex;align-items:center;justify-content:space-between;gap:20px}}
.zb{{background:#ffd400;color:#071233;border-radius:{18*s}px;padding:{12*s}px {24*s}px;display:flex;align-items:center;gap:{14*s}px}} .zb svg{{width:{52*s}px}}
.end{{font:500 {24*s}px/1.35 Inter;color:#aab2cc;text-align:right}}
.black{{position:absolute;left:50%;transform:translateX(-50%) rotate(-2deg);top:60px;background:#0a0a0a;border:3px solid #E3122B;box-shadow:0 0 24px #E3122Baa;border-radius:16px;padding:12px 26px;font:italic 900 40px BC;white-space:nowrap}} .black span{{color:#ffd400}}
</style></head><body><div class=ph></div>{extra}
<div class=pn><span class=tag>CENTRO DE CRATEÚS</span><h1>Bateria e pneu<br><b>num só lugar!</b></h1>
<div class=sub>E se você não puder vir, a moto da Líder leva a bateria e instala onde você estiver.</div></div>
<div class=zap><div class=zb>{ZAP}<div><div style="font:700 {20*s}px BC;letter-spacing:3px">CHAMA NO ZAP</div><div style="font:italic 900 {50*s}px/1 BC">(88) 9.8865-5130</div></div></div>
<div class=end>Rua Deolino Barreto, 860<br>Centro · Crateús/CE</div></div></body></html>"""
blk='<div class=black>🔥 ÚLTIMO DIA DA BLACK: <span>10X NO PREÇO DE À VISTA</span></div>'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,(W,H,ph,ct,s,ex) in {'feed':(1080,1350,1010,'52%',0.82,'<style>.sub{display:none}.zap{bottom:36px!important}</style>'),'story':(1080,1920,1440,'0%',1,blk)}.items():
        open(n+'.html','w').write(page(W,H,ph,ct,s,ex)); pg=b.new_page(viewport={'width':W,'height':H}); pg.goto('file://'+D+'/'+n+'.html'); pg.wait_for_timeout(500); pg.screenshot(path=n+'.jpg',type='jpeg',quality=93)
    b.close()
