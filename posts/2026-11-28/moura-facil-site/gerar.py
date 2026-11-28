import os
R=os.path.abspath('../../..'); F=R+'/ferramentas/fontes'; D=os.getcwd()
bat=f"file://{R}/canva/moura-sem-fundo.png"; logo=f"file://{R}/marca/logo.png"
css=''
for w,st in ((700,'normal'),(800,'italic'),(900,'italic')): css+=f"@font-face{{font-family:BC;font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}"
for w in (500,600,700): css+=f"@font-face{{font-family:Inter;font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}"
ZAP='<svg viewBox="0 0 24 24" fill="#071233"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
LOCK='<svg viewBox="0 0 24 24" fill="#1aa34a"><path d="M6 10V8a6 6 0 1 1 12 0v2h1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V11a1 1 0 0 1 1-1h1zm2 0h8V8a4 4 0 1 0-8 0v2z"/></svg>'
def page(W,H,s,story):
    return f"""<html><head><meta charset=utf-8><style>{css}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;color:#fff;font-family:Inter;
background:radial-gradient(circle at 75% 30%,#1f3fa8 0,#0b1d5c 40%,#050d2b 80%)}}
.rays{{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 80% 28%,rgba(255,212,0,.07) 0 6deg,transparent 6deg 18deg)}}
.top{{position:absolute;left:{60*s}px;right:{60*s}px;top:{60*s}px;display:flex;justify-content:space-between;align-items:center}}
.top img{{height:{110*s}px}}
.chip{{background:#ffd400;color:#071233;font:700 {30*s}px BC;letter-spacing:{3*s}px;padding:{8*s}px {20*s}px;border-radius:{40*s}px}}
.bat{{position:absolute;right:{-30*s}px;top:{(230 if story else 165)*s}px;width:{(560 if story else 400)*s}px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.55))}}
.glow{{position:absolute;right:{40*s}px;top:{(330 if story else 260)*s}px;width:{420*s}px;height:{420*s}px;border-radius:50%;background:radial-gradient(#ffd40066,transparent 65%)}}
.h{{position:absolute;left:{60*s}px;top:{(250 if story else 175)*s}px;width:{560*s}px}}
.h small{{display:block;font:700 {34*s}px BC;letter-spacing:{4*s}px;color:#ffd400}}
.h h1{{font:italic 900 {(128 if story else 96)*s}px/.88 BC;text-transform:uppercase;margin-top:{10*s}px;text-shadow:0 6px 24px rgba(0,0,0,.5)}}
.h h1 b{{color:#ffd400}}
.h p{{font:600 {30*s}px/1.3 Inter;color:#d3d9ec;margin-top:{18*s}px}}
.url{{position:absolute;left:{40*s}px;right:{40*s}px;top:{(840 if story else 560)*s}px;background:#fff;border-radius:{30*s}px;padding:{26*s}px {28*s}px {30*s}px;
 box-shadow:0 0 0 {8*s}px #ffd400,0 30px 60px rgba(0,0,0,.6);color:#071233}}
.bar{{display:flex;align-items:center;gap:{12*s}px;font:600 {24*s}px Inter;color:#5a6280}}
.bar i{{width:{18*s}px;height:{18*s}px;border-radius:50%;display:inline-block}}
.bar svg{{width:{26*s}px;margin-left:{14*s}px}}
.u1{{font:italic 900 {(232 if story else 200)*s}px/.88 BC;letter-spacing:-1px;color:#071233;margin-top:{10*s}px;white-space:nowrap}}
.u2{{font:italic 900 {(158 if story else 146)*s}px/.95 BC;color:#e3122b;white-space:nowrap}}
.u2 span{{color:#071233}}
.hand{{position:absolute;right:{40*s}px;bottom:{-46*s}px;font-size:{90*s}px;transform:rotate(-20deg)}}
.pills{{position:absolute;left:{40*s}px;right:{40*s}px;top:{(1400 if story else 1015)*s}px;display:flex;gap:{16*s}px}}
.pill{{flex:1;background:rgba(255,255,255,.08);border:2px solid rgba(255,212,0,.6);border-radius:{22*s}px;padding:{18*s}px;text-align:center}}
.pill b{{display:block;font:italic 900 {54*s}px/1 BC;color:#ffd400}}
.pill span{{font:600 {22*s}px/1.25 Inter;color:#e6e9f5}}
.bf{{position:absolute;left:{40*s}px;right:{40*s}px;top:{1590*s}px;background:#0a0a0a;border:3px solid #e3122b;border-radius:{20*s}px;padding:{18*s}px {24*s}px;text-align:center;box-shadow:0 0 30px #e3122b88}}
.bf b{{font:italic 900 {44*s}px BC;color:#fff}} .bf b span{{color:#ffd400}}
.bf small{{display:block;font:500 {20*s}px Inter;color:#aab2cc;margin-top:{4*s}px}}
.zap{{position:absolute;left:{40*s}px;right:{40*s}px;bottom:{50*s}px;display:flex;align-items:center;justify-content:space-between}}
.zb{{background:#ffd400;color:#071233;border-radius:{18*s}px;padding:{12*s}px {22*s}px;display:flex;align-items:center;gap:{14*s}px}} .zb svg{{width:{50*s}px}}
.end{{font:500 {22*s}px/1.35 Inter;color:#aab2cc;text-align:right}}
{'' if story else '.sp{display:none}.pill{padding:10px}.pill b{font-size:44px}.pill span{font-size:19px}'}</style></head><body><div class=rays></div>
<div class=top><img src="{logo}"><div class=chip>DELIVERY OFICIAL MOURA</div></div>
<div class=glow></div><img class=bat src="{bat}">
<div class=h><small>MOURA FÁCIL</small><h1>Bateria Moura<br><b>pelo site!</b></h1><p class=sp>Escolhe, pede e recebe a bateria do seu carro.</p></div>
<div class=url><div class=bar><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>{LOCK}<span>Acesse agora</span></div>
<div class=u1>mourafacil</div><div class=u2><span>.</span>moura.com.br</div><div class=hand>👆</div></div>
<div class=pills><div class=pill><b>10X</b><span>sem juros<br>na Moura</span></div><div class=pill><b>ENTREGA</b><span>e instalação<br>grátis</span></div><div class=pill><b>LÍDER</b><span>revenda Moura<br>em Crateús</span></div></div>
{'<div class=bf><b>BLACK NOVEMBER MOURA: <span>R$100 EM VALE BÔNUS</span></b><small>Na compra da bateria pelo site · consulte o regulamento em mourafacil.moura.com.br</small></div>' if story else ''}
<div class=zap><div class=zb>{ZAP}<div><div style="font:700 {20*s}px BC;letter-spacing:3px">OU CHAMA NO ZAP</div><div style="font:italic 900 {48*s}px/1 BC">(88) 9.8865-5130</div></div></div>
<div class=end>Líder Baterias e Pneus<br>Rua Deolino Barreto, 860 · Crateús/CE</div></div></body></html>"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,(W,H,s,st) in {'story':(1080,1920,1,True),'feed':(1080,1350,1,False)}.items():
        open(n+'.html','w').write(page(W,H,s,st)); pg=b.new_page(viewport={'width':W,'height':H}); pg.goto('file://'+D+'/'+n+'.html'); pg.wait_for_timeout(600); pg.screenshot(path=n+'.jpg',type='jpeg',quality=93)
    b.close()
