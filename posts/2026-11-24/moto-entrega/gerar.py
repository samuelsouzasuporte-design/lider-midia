import os
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
F = os.path.join(RAIZ,'ferramentas','fontes'); OUT=os.path.dirname(os.path.abspath(__file__))
logo='file://'+os.path.join(RAIZ,'marca','logo.png')
css=''
for w,st in ((700,'normal'),(800,'italic'),(900,'italic')):
    css+=f"@font-face{{font-family:'BC';font-weight:{w};font-style:{st};src:url('file://{F}/barlow-condensed-latin-{w}-{st}.woff2')}}\n"
for w in (500,600,700):
    css+=f"@font-face{{font-family:'Inter';font-weight:{w};src:url('file://{F}/inter-latin-{w}-normal.woff2')}}\n"
CHK='<svg viewBox="0 0 24 24" fill="none" stroke="#071233" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ZAP='<svg viewBox="0 0 24 24" fill="#071233"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.5c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
def page(W,H,foto,pos,fh,tag,t1,t2,sub,itens,s):
    li=''.join(f'<div class=it><div class=ck>{CHK}</div><span>{i}</span></div>' for i in itens)
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{css}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#071233;font-family:Inter;color:#fff;position:relative}}
.ph{{position:absolute;left:0;right:0;top:0;height:{fh}px;background:url('file://{RAIZ}/fotos/{foto}') {pos}/cover}}
.ph:after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,18,51,.55) 0%,rgba(7,18,51,0) 22%,rgba(7,18,51,0) 60%,#071233 100%)}}
.logo{{position:absolute;top:{40*s}px;left:{50*s}px;width:{300*s}px}}
.badge{{position:absolute;top:{50*s}px;right:{50*s}px;background:#ffd400;color:#071233;font:italic 800 {34*s}px BC;padding:{8*s}px {22*s}px;border-radius:{12*s}px;transform:rotate(3deg);box-shadow:0 8px 0 rgba(0,0,0,.25)}}
.tx{{position:absolute;left:{60*s}px;right:{60*s}px;top:{fh-120*s}px}}
.tag{{display:inline-block;background:#ffd400;color:#071233;font:700 {30*s}px BC;letter-spacing:{4*s}px;padding:{6*s}px {18*s}px;border-radius:{8*s}px}}
h1{{font:italic 900 {112*s}px/.9 BC;text-transform:uppercase;margin-top:{16*s}px}} h1 b{{color:#ffd400}}
.sub{{font:500 {32*s}px/1.35 Inter;color:#cfd6ea;margin-top:{18*s}px}}
.its{{margin-top:{26*s}px}}
.it{{display:flex;align-items:center;gap:{18*s}px;margin-top:{14*s}px;font:600 {34*s}px Inter}}
.ck{{flex:0 0 {50*s}px;height:{50*s}px;border-radius:50%;background:#ffd400;display:flex;align-items:center;justify-content:center}} .ck svg{{width:{30*s}px}}
.zap{{position:absolute;left:{60*s}px;right:{60*s}px;bottom:{70*s}px;background:#ffd400;color:#071233;border-radius:{24*s}px;padding:{18*s}px {30*s}px;display:flex;align-items:center;gap:{20*s}px}}
.zap svg{{width:{66*s}px}} .za{{font:700 {26*s}px BC;letter-spacing:{3*s}px}} .zb{{font:italic 900 {64*s}px/1 BC}}
.end{{position:absolute;left:0;right:0;bottom:{24*s}px;text-align:center;font:500 {22*s}px Inter;color:#9aa3bd}}
</style></head><body><div class=ph></div><img class=logo src="{logo}"><div class=badge>NOVIDADE!</div>
<div class=tx><span class=tag>{tag}</span><h1>{t1}<br><b>{t2}</b></h1><div class=sub>{sub}</div><div class=its>{li}</div></div>
<div class=zap>{ZAP}<div><div class=za>PEDE PELO ZAP</div><div class=zb>(88) 9.8865-5130</div></div></div>
<div class=end>Rua Deolino Barreto, 860 - Centro · Crateús/CE</div></body></html>"""

def feedpage():
    W,H=1080,1350
    li=''.join(f'<div class=it><div class=ck>{CHK}</div><span>{i}</span></div>' for i in itens)
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{css}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#071233;font-family:Inter;color:#fff;position:relative}}
.ph{{position:absolute;right:0;top:0;bottom:0;width:560px;background:url('file://{RAIZ}/fotos/entrega-moto-01-lateral.jpg') 40% 30%/cover}}
.ph:after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#071233 0%,rgba(7,18,51,0) 30%)}}
.bar{{position:absolute;left:0;top:0;width:14px;height:100%;background:#ffd400}}
.logo{{position:absolute;top:60px;left:60px;width:300px}}
.tx{{position:absolute;left:60px;width:560px;top:250px}}
.tag{{display:inline-block;background:#ffd400;color:#071233;font:700 28px BC;letter-spacing:4px;padding:6px 16px;border-radius:8px}}
h1{{font:italic 900 128px/.88 BC;text-transform:uppercase;margin-top:22px}} h1 b{{color:#ffd400;display:block}}
.sub{{font:500 30px/1.38 Inter;color:#cfd6ea;margin-top:24px;width:480px}}
.its{{margin-top:30px}}
.it{{display:flex;align-items:center;gap:16px;margin-top:16px;font:600 29px/1.2 Inter;width:520px}}
.ck{{flex:0 0 46px;height:46px;border-radius:50%;background:#ffd400;display:flex;align-items:center;justify-content:center}} .ck svg{{width:28px}}
.zap{{position:absolute;left:60px;right:60px;bottom:80px;background:#ffd400;color:#071233;border-radius:22px;padding:18px 30px;display:flex;align-items:center;gap:20px;box-shadow:0 10px 30px rgba(0,0,0,.4)}}
.zap svg{{width:60px}} .za{{font:700 24px BC;letter-spacing:3px}} .zb{{font:italic 900 60px/1 BC}}
.end{{position:absolute;left:60px;bottom:30px;font:500 22px Inter;color:#9aa3bd}}
</style></head><body><div class=ph></div><div class=bar></div><img class=logo src="{logo}">
<div class=tx><span class=tag>NOVIDADE NA LÍDER</span><h1>Pediu?<b>A gente<br>leva!</b></h1>
<div class=sub>A moto da Líder sai com ferramenta a bordo: a bateria chega e já sai instalada.</div><div class=its>{li}</div></div>
<div class=zap>{ZAP}<div><div class=za>PEDE PELO ZAP</div><div class=zb>(88) 9.8865-5130</div></div></div>
<div class=end>Rua Deolino Barreto, 860 - Centro · Crateús/CE</div></body></html>"""
itens=['Entrega e instalação grátis na bateria','Teste da bateria antes da troca','Moura em até 10x sem juros']
jobs={'story':(1080,1920,'entrega-moto-04-funcionario.jpg','center 30%',1080,'A LÍDER VAI ATÉ VOCÊ','Bateria','na porta!','Nossa moto de entrega já está rodando, com ferramenta a bordo pra instalar na hora.',itens,1),
      'feed':(1080,1350,'entrega-moto-01-lateral.jpg','center 38%',640,'NOVIDADE NA LÍDER','Pediu?','A gente leva!','Moto da Líder com ferramenta a bordo: a bateria chega e já sai instalada.',itens,0.82)}
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,a in jobs.items():
        h=os.path.join(OUT,n+'.html'); open(h,'w').write(feedpage() if n=='feed' else page(*a))
        pg=b.new_page(viewport={'width':a[0],'height':a[1]}); pg.goto('file://'+h); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT,n+'.jpg'),type='jpeg',quality=93)
    b.close()
print('ok')
