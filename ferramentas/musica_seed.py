"""Escolhe uma música NOVA para cada vídeo (pedido do dono, 09/11/2026: "sempre troque a música quando for vídeo em story").
Cada seed muda acordes, tom, batida (house, piseiro, half-time, xote eletrônico), timbre e arpejo.
Uso: python3 ferramentas/musica_seed.py [rotulo]  -> imprime uma seed nunca usada (com batida diferente da última) e registra em musicas_usadas.txt
"""
import os, sys, datetime
AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(os.path.dirname(AQUI), 'musicas_usadas.txt')
JA = [61, 67, 71, 47, 53, 11, 23, 17, 41, 29, 43]   # seeds usadas antes deste registro


def estilo(s): return (s // 5) % 4


def proxima(rotulo=''):
    usadas = list(JA)
    if os.path.exists(ARQ):
        for l in open(ARQ):
            try: usadas.append(int(l.split()[0]))
            except Exception: pass
    ult = usadas[-1] if usadas else None
    s = max(usadas + [100]) + 1
    while s in usadas or (ult is not None and estilo(s) == estilo(ult)):
        s += 1
    with open(ARQ, 'a') as f:
        f.write(f"{s} {datetime.date.today().isoformat()} {rotulo}\n")
    return s


if __name__ == '__main__':
    print(proxima(' '.join(sys.argv[1:])))
