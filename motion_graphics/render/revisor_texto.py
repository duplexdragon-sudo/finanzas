#!/usr/bin/env python3
"""Revisor de texto: recorre el video cuadro a cuadro y avisa si un TEXTO se pisa con otro texto, una cara o un logo.
Uso: python3 revisor_texto.py render_c9 [fps=6]   → lista de choques + revisor_texto.jpg con los cuadros marcados en rojo."""
import sys, importlib, itertools, os
import numpy as np
from PIL import Image, ImageDraw

mod = sys.argv[1].replace(".py", ""); FPS_R = float(sys.argv[2]) if len(sys.argv) > 2 else 6
R = importlib.import_module(mod); W, H = R.W, R.H

REC = None; CTX = []; CID = [0]
_orig = Image.Image.alpha_composite
def _ac(self, im, dest=(0, 0), source=(0, 0)):
    _orig(self, im, dest, source)
    if REC is None or self.size != (W, H) or not CTX: return
    a = np.asarray(im.getchannel("A")) > 90
    if source != (0, 0): a = a[source[1]:, source[0]:]
    x, y = dest; h, w = a.shape
    big = np.zeros((H, W), bool); x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0: return
    big[y0:y1, x0:x1] = a[y0 - y:y1 - y, x0 - x:x1 - x]
    n = big.sum()
    if n < 1500 or n > W * H * .45: return                       # partículas y fondos no cuentan
    kind, cid, lab = CTX[-1]
    if kind == "I":                                              # en fotos y logos sólo cuenta la parte de arriba (cara); el pecho puede llevar el nombre
        ys = np.nonzero(big.any(1))[0]; big[int(ys[0] + (ys[-1] - ys[0]) * .72):] = False
    REC.append((kind, cid, lab, big))
Image.Image.alpha_composite = _ac

def ctx(kind, lab):
    CID[0] += 1; CTX.append((kind, CID[0], lab))
def wrap_text(fn, name):
    def f(*a, **k):
        lab = next((x for x in a if isinstance(x, str)), name); ctx("T", lab)
        try: return fn(*a, **k)
        finally: CTX.pop()
    return f
def mark(fn):
    def f(*a, **k):
        r = fn(*a, **k)
        try: r._txt = next((x for x in a if isinstance(x, str)), fn.__name__)
        except Exception: pass
        return r
    return f
def wrap_place(fn):
    def f(im, img, *a, **k):
        lab = getattr(img, "_txt", None)
        if getattr(img, "_clip", False): ctx("K", "clip de jugada")             # los clips cuentan completos (no solo la cara)
        else: ctx("T" if lab else "I", lab or "imagen")
        try: return fn(im, img, *a, **k)
        finally: CTX.pop()
    return f
for n in ("word", "slam", "ribbon", "stamp", "counter"):
    if hasattr(R, n): setattr(R, n, wrap_text(getattr(R, n), n))
for n in ("nchip", "chipx", "text_layer"):
    if hasattr(R, n): setattr(R, n, mark(getattr(R, n)))
for n in ("pop", "paste"):
    if hasattr(R, n): setattr(R, n, wrap_place(getattr(R, n)))
if hasattr(R, "vcard"):
    def _vc(fn):
        def f(*a, **k):
            r = fn(*a, **k)
            if r: r[0]._clip = True
            return r
        return f
    R.vcard = _vc(R.vcard)
if hasattr(R, "c9orb"): R.c9orb = (lambda fn: lambda *a, **k: (ctx("I", "logo"), fn(*a, **k), CTX.pop())[1])(R.c9orb)

def check(T):
    global REC
    REC = []; name = [n for n in R.ORDER if T >= R.SEG[n]][-1]
    ctx("B", "escena"); im = R.scene(name, T); CTX.pop(); recs = REC; REC = None
    hits = []
    for (k1, c1, l1, m1), (k2, c2, l2, m2) in itertools.combinations(recs, 2):
        if c1 == c2 or "B" in (k1, k2) or (k1 != "T" and k2 != "T"): continue
        ov = (m1 & m2).sum()
        if ov > 250: hits.append((l1, l2, int(ov), m1 & m2))
    return name, im, hits

if __name__ == "__main__":
    bad = []; n = int(R.DUR * FPS_R)
    for i in range(n):
        T = i / FPS_R; name, im, hits = check(T)
        if hits:
            for l1, l2, ov, _ in hits: print(f"{T:6.2f}s {name}: «{l1}» choca con «{l2}» ({ov} px)")
            d = ImageDraw.Draw(im)
            for *_, m in hits:
                ys, xs = np.nonzero(m); d.rectangle((xs.min() - 6, ys.min() - 6, xs.max() + 6, ys.max() + 6), outline=(255, 0, 0, 255), width=6)
            bad.append(im.convert("RGB").resize((W // 3, H // 3)))
    print("CHOQUES:", len(bad), "cuadros de", n)
    if bad:
        bad = bad[:24]; sh = Image.new("RGB", (W // 3 * min(8, len(bad)), H // 3 * ((len(bad) + 7) // 8)), "white")
        for k, x in enumerate(bad): sh.paste(x, ((k % 8) * W // 3, (k // 8) * H // 3))
        sh.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "revisor_texto.jpg"), quality=85)
