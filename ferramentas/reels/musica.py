import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
import sys

SR = 44100
BPM = 124
BEAT = 60 / BPM
BAR = 4 * BEAT
NBARS = 16
TAIL = 4.6
DUR = NBARS * BAR + TAIL
N = int(DUR * SR)
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 7
rng = np.random.default_rng(SEED)

L = np.zeros(N); R = np.zeros(N)
side = np.ones(N)  # sidechain envelope

def t_(n): return np.arange(n) / SR
def idx(t): return int(t * SR)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)

def add(buf, x, t, g=1.0):
    i = idx(t)
    if i >= N: return
    x = x[:N - i]
    buf[i:i + len(x)] += x * g

def addst(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * np.sqrt(0.5 * (1 - pan)) * 1.414)
    add(R, x, t, g * np.sqrt(0.5 * (1 + pan)) * 1.414)

def addst2(xl, xr, t, g=1.0):
    add(L, xl, t, g); add(R, xr, t, g)

# ---------- instruments ----------
def kick():
    n = idx(0.45); tt = t_(n)
    f = 45 + 120 * np.exp(-tt * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-tt * 6.5)
    click = hp(rng.standard_normal(n), 2000) * np.exp(-tt * 300) * 0.4
    return np.tanh((x + click) * 1.6)

def clap():
    n = idx(0.35); tt = t_(n)
    nz = bp(rng.standard_normal(n), 900, 5000)
    env = np.zeros(n)
    for d in (0, 0.011, 0.022):
        s = idx(d); env[s:] += np.exp(-(tt[:n - s]) * 60)
    env += np.exp(-tt * 14) * 0.5
    return nz * env * 0.6

def hat(open_=False):
    n = idx(0.25 if open_ else 0.06); tt = t_(n)
    x = hp(rng.standard_normal(n), 7000, 4)
    return x * np.exp(-tt * (12 if open_ else 70)) * 0.35

def saw(freq, n, detune=0.0, phase=0.0):
    tt = t_(n)
    p = (tt * freq * (1 + detune) + phase) % 1.0
    return 2 * p - 1

def supersaw(freqs, n):
    xl = np.zeros(n); xr = np.zeros(n)
    dets = [-0.012, -0.006, 0, 0.006, 0.012]
    for f in freqs:
        for k, d in enumerate(dets):
            s = saw(f, n, d, rng.random())
            pan = (k - 2) / 2
            xl += s * (1 - pan) * 0.5; xr += s * (1 + pan) * 0.5
    return xl, xr

def pluck(freq, n):
    tt = t_(n)
    x = saw(freq, n) * 0.6 + saw(freq * 2, n, 0.003) * 0.25
    cut = 600 + 5000 * np.exp(-tt * 18)
    # time-varying lowpass approximation: blend of two filtered versions
    a = lp(x, 6000); b = lp(x, 700)
    w = (cut - 600) / 5000
    return (a * w + b * (1 - w)) * np.exp(-tt * 9)

def bass(freq, n):
    tt = t_(n)
    x = np.sin(2 * np.pi * freq * tt) + 0.35 * saw(freq, n)
    x = lp(x, 500)
    env = np.minimum(1, tt / 0.005) * np.minimum(1, (n / SR - tt) / 0.02)
    return np.tanh(x * 1.8) * env

def reverb(x, secs=2.2, wet=0.25):
    n = idx(secs); tt = t_(n)
    ir = rng.standard_normal(n) * np.exp(-tt * 3.2)
    ir = lp(ir, 6000)
    y = fftconvolve(x, ir)[:len(x)]
    y /= (np.max(np.abs(y)) + 1e-9)
    return y * wet * np.max(np.abs(x))

# ---------- arrangement ----------
# A minor: Am F C G   (roots MIDI)
PROGS = [
    [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])],   # Am F C G
    [(50, [50, 53, 57]), (46, [46, 50, 53]), (53, [53, 57, 60]), (48, [48, 52, 55])],   # Dm Bb F C
    [(52, [52, 55, 59]), (48, [48, 52, 55]), (55, [55, 59, 62]), (50, [50, 54, 57])],   # Em C G D
    [(57, [57, 60, 64]), (55, [55, 59, 62]), (53, [53, 57, 60]), (52, [52, 56, 59])],   # Am G F E
]
prog = PROGS[SEED % len(PROGS)]
# transposição leve por seed
_tr = [0, 2, -2, 3, -3][SEED % 5]
prog = [(r + _tr, [m + _tr for m in ch]) for r, ch in prog]
DROP = 2 * BAR  # drop after 2-bar intro

padL = np.zeros(N); padR = np.zeros(N); plk = np.zeros(N)

for bar in range(NBARS):
    t0 = bar * BAR
    root, ch = prog[bar % 4]
    intro = bar < 2
    breakdown = bar in (10, 11)
    # pads
    n = idx(BAR)
    xl, xr = supersaw([mtof(m) for m in ch], n)
    env = np.minimum(1, t_(n) / 0.08) * np.minimum(1, (BAR - t_(n)) / 0.05)
    cut = 900 if intro else (1400 if breakdown else 2600)
    padL[idx(t0):idx(t0) + n] += lp(xl, cut) * env
    padR[idx(t0):idx(t0) + n] += lp(xr, cut) * env
    # pluck arpeggio 16ths
    arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[2] + 12]
    for s in range(16):
        f = mtof(arp[s % 8])
        p = pluck(f, idx(BEAT * 0.5))
        g = 0.18 if not intro else 0.12
        add(plk, p, t0 + s * BEAT / 4, g)
    if intro:
        continue
    # drums
    for b in range(4):
        tb = t0 + b * BEAT
        if not breakdown:
            addst(kick(), tb, 0.9)
            s = idx(tb); e = min(N, s + idx(BEAT))
            ramp = np.minimum(1, t_(e - s) / (BEAT * 0.55)) ** 1.5
            side[s:e] = np.minimum(side[s:e], 0.25 + 0.75 * ramp)
        addst(hat(True), tb + BEAT / 2, 0.55, 0.2)
        if b in (1, 3):
            addst(clap(), tb, 0.8 if not breakdown else 0.5)
        for h in range(4):
            if h != 2:
                addst(hat(), tb + h * BEAT / 4, 0.4 if h else 0.25, -0.3)
    # bass: offbeat 8ths
    if not breakdown:
        for e8 in range(8):
            if e8 % 2 == 1:
                f = mtof(root - 12)
                addst(bass(f, idx(BEAT / 2 * 0.9)), t0 + e8 * BEAT / 2, 0.55)
            elif e8 in (2, 6):
                addst(bass(mtof(root - 12), idx(BEAT / 2 * 0.6)), t0 + e8 * BEAT / 2, 0.3)

# risers & impacts
def riser(dur):
    n = idx(dur); tt = t_(n)
    x = rng.standard_normal(n)
    lo = lp(x, 800); hi = hp(x, 2500)
    w = tt / dur
    y = lo * (1 - w) + hi * w
    return y * (w ** 2) * 0.5

def impact():
    n = idx(2.5); tt = t_(n)
    boom = np.sin(2 * np.pi * np.cumsum(30 + 60 * np.exp(-tt * 8)) / SR) * np.exp(-tt * 2.2)
    nz = lp(rng.standard_normal(n), 3000) * np.exp(-tt * 3) * 0.4
    return np.tanh((boom + nz) * 1.5)

for tdrop in (DROP, 12 * BAR):
    r = riser(BAR * 1.5 if tdrop == DROP else BAR)
    addst(r, tdrop - len(r) / SR, 0.7)
    addst(impact(), tdrop, 0.7)

# final hit + tail
END = NBARS * BAR
addst(impact(), END, 0.9)
n = idx(TAIL); xl, xr = supersaw([mtof(m) for m in [57, 60, 64, 69]], n)
env = np.exp(-t_(n) * 1.3)
addst2(lp(xl, 2000) * env * 0.12, lp(xr, 2000) * env * 0.12, END)
addst(kick(), END, 1.0)

# mix
padL *= 0.07 * side; padR *= 0.07 * side
plk_s = plk * side
plk_rv = reverb(plk_s, wet=0.5)
L += padL + plk_s * 0.9 + plk_rv * 0.6
R += padR + np.concatenate([np.zeros(idx(0.012)), plk_s[:-idx(0.012)]]) * 0.9 + plk_rv * 0.6
padrv = reverb(padL + padR, wet=0.3)
L += padrv; R += padrv

# fade-in intro slightly, master
fi = np.minimum(1, t_(N) / 0.5)
mix = np.stack([L, R], 1) * fi[:, None]
mix = hp(mix.T, 25).T
mix /= np.max(np.abs(mix))
mix = np.tanh(mix * 1.8) / np.tanh(1.8)
mix *= 0.93
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("dur", DUR, "drop", DROP, "bar", BAR)
