#!/usr/bin/env python3
"""Recreación (original) del estilo 'motion design editorial': blanco ↔ morado, serif italic, objetos con pop.
Voz: ../motion/voz/lXX.wav (ElevenLabs). Uso: python3 render_motion.py salida.mp4 | --preview t1,t2"""
import os, sys, math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from render import text_layer, paste, prog, eo, eio, lerp, SERIF, SANS, F, canvas, _safe_comp, scale_about

HERE = os.path.dirname(os.path.abspath(__file__)); MO = os.path.join(HERE, "..", "motion"); TZ = os.path.join(HERE, "..", "tenz")
W, H, FPS = 720, 1280, 30
PUR = (115, 16, 165); LIL = (166, 97, 196); LILL = (228, 205, 238); WHITE = (255, 255, 255); CREAM = (241, 235, 227); INK = (17, 17, 17)
ANTON = lambda s: F("anton-400-normal", s)
IT = lambda w, s: SERIF(w, s, True)

# ---------------- tiempos desde la voz ----------------
DUR_L = []
for i in range(11):
    w = wave.open(os.path.join(MO, "voz", f"l{i:02d}.wav")); DUR_L.append(w.getnframes() / w.getframerate())
GAP = .32; LS = []; t = .35
for d in DUR_L: LS.append(t); t += d + GAP
TOTAL = t + .9
CUT = [0.0] + [s - .12 for s in LS[1:]]

def clamp01(x): return max(0., min(1., x))
def ease_back(x, s=1.7):
    x = clamp01(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2
def pop(dst, img, x, y, t, t0, dur=.35, a=1.0, anchor="mm"):
    p = prog(t, t0, t0 + dur)
    if p <= 0: return
    s = max(.01, ease_back(p)); im = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BICUBIC)
    paste(dst, im, x, y, a * clamp01(p * 2.5), anchor)
def word(dst, s, font, x, y, t, t0, color=INK, anchor="mm", dur=.28):
    p = eo(prog(t, t0, t0 + dur))
    if p <= 0: return
    l = text_layer(s, font, color)
    if p < 1: l = l.filter(ImageFilter.GaussianBlur(4 * (1 - p)))
    paste(dst, l, x, y + 22 * (1 - p), p, anchor)
def shadow(img, dy=18, blur=16, op=.35):
    pad = blur * 3; out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad + dy), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (40, 0, 60, 255)); sh.putalpha(img.getchannel("A").point(lambda v: int(v * op)))
    tmp = Image.new("RGBA", out.size, (0, 0, 0, 0)); tmp.alpha_composite(sh, (pad, pad + dy))
    out.alpha_composite(tmp.filter(ImageFilter.GaussianBlur(blur))); out.alpha_composite(img, (pad, pad)); return out
def ss(fn, size, k=2):
    return fn((size[0] * k, size[1] * k), k).resize(size, Image.LANCZOS)

# ---------------- fondos ----------------
def grid(img, col, step=48):
    d = ImageDraw.Draw(img)
    for x in range(0, W, step): d.line((x, 0, x, H), fill=col)
    for y in range(0, H, step): d.line((0, y, W, y), fill=col)
def burst(r, n=7, col=WHITE):
    im = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rr = random.Random(n)
    for k in range(n):
        a = math.radians(-120 + k * 22 + rr.uniform(-6, 6)); L = r * rr.uniform(.6, 1.0); w = math.radians(rr.uniform(4, 7))
        d.polygon([(r, r), (r + L * math.cos(a - w), r + L * math.sin(a - w)), (r + L * 1.1 * math.cos(a), r + L * 1.1 * math.sin(a)), (r + L * math.cos(a + w), r + L * math.sin(a + w))], fill=col + (255,))
    return im
BURST = burst(260)
def bg_white(ghost=None):
    im = canvas(WHITE + (255,)); grid(im, (238, 236, 242, 255))
    if ghost:
        g = text_layer(ghost, IT(900, 240), (225, 222, 230)); paste(im, g, 360, 700)
    return im
def bg_purple():
    im = canvas(PUR + (255,)); grid(im, (128, 34, 178, 255), 56)
    paste(im, BURST.rotate(200, expand=True), W + 190, -150, 1, "rt"); paste(im, BURST.rotate(20, expand=True), -190, H + 150, 1, "lb")
    return im
def bg_cream(): im = canvas(CREAM + (255,)); return im
BGW = {}; BGP = bg_purple(); BGC = bg_cream()
def bgw(g):
    if g not in BGW: BGW[g] = bg_white(g)
    return BGW[g].copy()

# ---------------- objetos originales ----------------
def bulb_img(size, k, lit=0.0):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy, r = w / 2, h * .38, w * .36
    glass = Image.new("L", size, 0); ImageDraw.Draw(glass).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    ImageDraw.Draw(glass).polygon([(cx - r * .55, cy + r * .7), (cx + r * .55, cy + r * .7), (cx + r * .38, h * .78), (cx - r * .38, h * .78)], fill=255)
    yy, xx = np.mgrid[0:h, 0:w]; dist = np.sqrt((xx - cx + r * .3) ** 2 + (yy - cy + r * .3) ** 2) / (r * 1.6)
    base = np.array([235, 232, 240]) * (1 - lit) + np.array([255, 214, 245]) * lit
    col = np.clip(base[None, None, :] * (1.05 - .35 * dist[..., None]), 0, 255).astype(np.uint8)
    g = Image.fromarray(col).convert("RGBA"); g.putalpha(glass.point(lambda v: int(v * .92))); im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    fc = (120, 60, 160, 255) if lit < .5 else (255, 120, 220, 255)
    d.line([(cx - r * .3, cy + r * .6), (cx - r * .25, cy - r * .05), (cx - r * .1, cy + r * .15), (cx, cy - r * .1), (cx + r * .1, cy + r * .15), (cx + r * .25, cy - r * .05), (cx + r * .3, cy + r * .6)], fill=fc, width=int(4 * k))
    for i in range(4):
        y = h * .78 + i * h * .045; d.rounded_rectangle((cx - r * .42, y, cx + r * .42, y + h * .04), int(6 * k), fill=(150 - i * 12, 150 - i * 12, 160 - i * 12, 255))
    d.ellipse((cx - r * .2, h * .95 - h * .03, cx + r * .2, h * .95 + h * .01), fill=(60, 60, 70, 255))
    d.ellipse((cx - r * .55, cy - r * .6, cx - r * .25, cy - r * .2), fill=(255, 255, 255, 170))   # brillo
    return im
BULB = shadow(ss(bulb_img, (260, 380))); BULB_LIT = shadow(ss(lambda s, k: bulb_img(s, k, 1.0), (260, 380)))

def tile(i, size=(230, 230)):
    w, h = size; cols = [(20, 20, 24), CREAM, PUR, LILL]; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=cols[i] + (255,)); c = WHITE if i in (0, 2) else PUR
    if i == 0: d.ellipse((w * .3, h * .3, w * .7, h * .7), outline=c + (255,), width=14)
    if i == 1: d.polygon([(w * .5, h * .25), (w * .75, h * .72), (w * .25, h * .72)], fill=c + (255,))
    if i == 2:
        for j in range(3): d.arc((w * .2, h * (.25 + j * .15), w * .8, h * (.55 + j * .15)), 200, 340, fill=c + (255,), width=12)
    if i == 3: d.text((w / 2, h / 2), "DD", font=ANTON(110), fill=c + (255,), anchor="mm")
    return shadow(im, 10, 10, .3)
TILES = [tile(i) for i in range(4)]

def die_img(size, k, face=5):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = w * .5; cx, cy = w / 2, h / 2
    top = [(cx, cy - s * .9), (cx + s * .85, cy - s * .45), (cx, cy), (cx - s * .85, cy - s * .45)]
    left = [(cx - s * .85, cy - s * .45), (cx, cy), (cx, cy + s * .95), (cx - s * .85, cy + s * .5)]
    right = [(cx, cy), (cx + s * .85, cy - s * .45), (cx + s * .85, cy + s * .5), (cx, cy + s * .95)]
    d.polygon(top, fill=(255, 255, 255, 255)); d.polygon(left, fill=(226, 220, 236, 255)); d.polygon(right, fill=(200, 190, 215, 255))
    for poly in (top, left, right): d.line(poly + [poly[0]], fill=(170, 160, 190, 255), width=int(2 * k))
    def dots(poly, pts):
        a, b, c_, dd = [np.array(p) for p in poly]
        for u, v in pts:
            p = a + (b - a) * u + (dd - a) * v; r = s * .07; d.ellipse((p[0] - r, p[1] - r * .7, p[0] + r, p[1] + r * .7), fill=PUR + (255,))
    dots(top, [(.5, .5)] if face == 1 else [(.25, .25), (.75, .75), (.5, .5), (.25, .75), (.75, .25)])
    dots(left, [(.3, .3), (.7, .7)]); dots(right, [(.25, .25), (.5, .5), (.75, .75)])
    return im
DIE = shadow(ss(die_img, (220, 220)), 14, 12, .45)

def eye_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy, r = w / 2, h / 2, w * .48; dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    shade = np.clip(1.0 - .45 * np.sqrt(((xx - cx + r * .35) ** 2 + (yy - cy + r * .35) ** 2)) / (r * 1.6), .45, 1)
    rgb = np.dstack([245 * shade, 242 * shade, 248 * shade])
    # venitas sutiles
    a = (dd < 1).astype(np.float32); out = np.dstack([rgb, a * 255]).astype(np.uint8); im = Image.fromarray(out, "RGBA")
    d = ImageDraw.Draw(im); ri = r * .45
    ir = Image.new("RGBA", size, (0, 0, 0, 0)); irr = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / ri
    ang = np.arctan2(yy - cy, xx - cx); strands = .75 + .25 * np.sin(ang * 40)
    colr = np.clip(np.dstack([60 + 90 * irr * strands, 10 + 30 * irr, 120 + 100 * irr * strands]), 0, 255)
    ia = ((irr < 1) * 255).astype(np.uint8); ir = Image.fromarray(np.dstack([colr, ia]).astype(np.uint8), "RGBA"); im.alpha_composite(ir)
    d = ImageDraw.Draw(im); rp = ri * .42; d.ellipse((cx - rp, cy - rp, cx + rp, cy + rp), fill=(8, 6, 12, 255))
    d.ellipse((cx - ri * .55, cy - ri * .6, cx - ri * .2, cy - ri * .25), fill=(255, 255, 255, 220))
    ring = Image.new("L", size, 0); ImageDraw.Draw(ring).ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=255, width=int(5 * k))
    im.alpha_composite(Image.merge("RGBA", (Image.new("L", size, 30), Image.new("L", size, 0), Image.new("L", size, 50), ring)))
    return im
EYE = shadow(ss(eye_img, (420, 420)), 18, 18, .35)

def tv_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for x0, x1 in ((.22, .3), (.7, .78)): d.polygon([(w * x0, h * .72), (w * x1, h * .72), (w * (x1 + (-.06 if x0 < .5 else .06)), h), (w * (x0 + (-.06 if x0 < .5 else .06)), h)], fill=(120, 74, 40, 255))
    d.rectangle((w * .2, h * .74, w * .8, h * .77), fill=(140, 90, 50, 255))
    d.rounded_rectangle((0, 0, w - 1, h * .74), int(36 * k), fill=(190, 30, 40, 255))
    d.rounded_rectangle((w * .03, h * .02, w * .97, h * .7), int(30 * k), fill=(214, 46, 56, 255))
    d.rounded_rectangle((w * .07, h * .07, w * .72, h * .64), int(30 * k), fill=(30, 26, 32, 255))
    d.rounded_rectangle((w * .76, h * .07, w * .93, h * .64), int(14 * k), fill=(225, 212, 196, 255))
    for i, y in enumerate((.16, .3)): d.ellipse((w * .79, h * y, w * .9, h * y + w * .11), fill=(60, 60, 64, 255))
    for y in range(int(h * .45), int(h * .6), int(8 * k)): d.line((w * .79, y, w * .9, y), fill=(140, 130, 120, 255), width=int(2 * k))
    return im
TV = ss(tv_img, (460, 470)); SCREEN = (int(460 * .07), int(470 * .07), int(460 * .72), int(470 * .64))
def tv_screen(i, t):
    sw, sh = SCREEN[2] - SCREEN[0], SCREEN[3] - SCREEN[1]; s = Image.new("RGBA", (sw, sh), (0, 0, 0, 255)); d = ImageDraw.Draw(s)
    cols = [PUR, (255, 110, 150), (30, 160, 200), (250, 190, 60)]; d.rectangle((0, 0, sw, sh), fill=cols[i % 4] + (255,))
    cx, cy = sw / 2, sh / 2 + math.sin(t * 6) * 6
    if i % 4 == 0:   # corazón
        d.ellipse((cx - 60, cy - 50, cx, cy + 10), fill=WHITE + (255,)); d.ellipse((cx, cy - 50, cx + 60, cy + 10), fill=WHITE + (255,)); d.polygon([(cx - 58, cy - 8), (cx + 58, cy - 8), (cx, cy + 60)], fill=WHITE + (255,))
    elif i % 4 == 1: d.polygon([(cx - 35, cy - 50), (cx - 35, cy + 50), (cx + 55, cy)], fill=WHITE + (255,))   # play
    elif i % 4 == 2:
        for j in range(5): d.arc((cx - 90 + j * 10, cy - 40, cx + 90 - j * 10, cy + 40), 180, 360, fill=WHITE + (255,), width=6)
    else:
        pts = [(cx + 70 * math.cos(math.radians(a)) * (1 if k % 2 == 0 else .42), cy + 70 * math.sin(math.radians(a)) * (1 if k % 2 == 0 else .42)) for k, a in enumerate(range(-90, 270, 36))]
        d.polygon(pts, fill=WHITE + (255,))
    for y in range(0, sh, 4): d.line((0, y, sw, y), fill=(0, 0, 0, 40))
    m = Image.new("L", (sw, sh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh - 1), 28, fill=255); s.putalpha(m); return s

def chart_card(t, p):
    w, h = 330, 560; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(10, 8, 30, 255))
    for i in range(9): x = i * w / 8; d.line((x, h * .35, w / 2 + (x - w / 2) * 2.2, h), fill=(70, 40, 140, 255), width=1)
    for j in range(7): y = h * .35 + (j / 6) ** 1.6 * h * .65; d.line((0, y, w, y), fill=(70, 40, 140, 255), width=1)
    pts = [(.05, .75), (.22, .62), (.38, .66), (.55, .52), (.72, .55), (.86, .38), (.96, .2)]
    n = p * (len(pts) - 1); vis = [pts[i] for i in range(int(n) + 1)]
    if int(n) < len(pts) - 1:
        a, b = pts[int(n)], pts[int(n) + 1]; f = n - int(n); vis.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    P = [(x * w, y * h) for x, y in vis]
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    if len(P) > 1: gd.line(P, fill=(60, 200, 255, 255), width=14)
    for x, y in P[:-1]: gd.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(120, 230, 255, 255))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9))); d = ImageDraw.Draw(im)
    if len(P) > 1: d.line(P, fill=(210, 245, 255, 255), width=4)
    for x, y in P[:-1]: d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=WHITE + (255,))
    return shadow(im, 22, 22, .5)

def diamond_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    top = h * .32; L, R = w * .04, w * .96
    crown = [(w * .25, h * .08), (w * .75, h * .08), (R, top), (L, top)]
    d.polygon(crown, fill=(220, 226, 236, 255))
    xs = [L, w * .25, w * .5, w * .75, R]; tones = [(240, 244, 250), (180, 190, 210), (250, 252, 255), (160, 172, 196)]
    for i in range(4):
        d.polygon([(xs[i], top), (xs[i + 1], top), (w * .5, h * .97)], fill=tones[i] + (255,))
    for x in (w * .25, w * .5, w * .75): d.line((x, h * .08 if x != w * .5 else h * .08, w * .5, h * .97), fill=(150, 160, 185, 255), width=int(2 * k))
    d.line((L, top, R, top), fill=(150, 160, 185, 255), width=int(2 * k))
    for (x0, x1) in ((w * .25, w * .38), (w * .62, w * .75)): d.polygon([(x0, h * .08), (x1, top), ((x0 + x1) / 2 - w * .1, top)], fill=(255, 255, 255, 200))
    return im
DIAMOND = ss(diamond_img, (220, 170))
def column_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    gold = lambda f: (int(200 * f), int(170 * f), int(120 * f), 255)
    d.rectangle((w * .05, 0, w * .95, h * .07), fill=gold(1.0))
    for cx in (w * .14, w * .86): d.ellipse((cx - w * .1, h * .02, cx + w * .1, h * .1), fill=gold(.9), outline=gold(.7), width=int(3 * k))
    d.rectangle((w * .15, h * .07, w * .85, h * .1), fill=gold(.85))
    shaft = np.zeros((h, w, 4), np.uint8); x0, x1 = int(w * .18), int(w * .82)
    for x in range(x0, x1):
        u = (x - x0) / (x1 - x0); f = .75 + .25 * math.cos((u - .35) * math.pi) + .08 * math.sin(u * math.pi * 18)
        shaft[int(h * .1):int(h * .93), x] = gold(f)
    im.alpha_composite(Image.fromarray(shaft, "RGBA")); d = ImageDraw.Draw(im)
    d.rectangle((w * .1, h * .93, w * .9, h), fill=gold(.8))
    return im
COLUMN = ss(column_img, (230, 620))
def king():
    p = os.path.join(TZ, "rey_ajedrez.png")
    if not os.path.exists(p): return None
    im = Image.open(p).convert("RGBA"); g = ImageEnhance.Contrast(ImageOps.grayscale(im.convert("RGB"))).enhance(1.1)
    g = ImageEnhance.Brightness(g).enhance(1.35)
    im = Image.merge("RGBA", (g, g, g, im.getchannel("A"))); return shadow(im.resize((int(im.width * 620 / im.height), 620), Image.LANCZOS), 20, 20, .45)
KING = king()

OBJ = os.path.join(MO, "objetos")
def uobj(name, h, sh=True):
    p = os.path.join(OBJ, name)
    if not os.path.exists(p): return None
    im = Image.open(p).convert("RGBA"); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    return shadow(im, 18, 18, .3) if sh else im
U_BRAIN = uobj("21_cerebro.png", 330); U_EYE = uobj("20_ojo.png", 420); U_KING = uobj("17_rey_ajedrez.png", 640)
U_CROWN = uobj("18_corona.png", 250); U_HOUR = uobj("19_reloj_arena.png", 420)
U_DIAM = uobj("24_diamante.png", 190, sh=False); U_COL = uobj("25_columna.png", 700, sh=False)
if U_DIAM is not None: DIAMOND = U_DIAM
if U_COL is not None: COLUMN = U_COL
if U_EYE is not None: EYE = U_EYE
if U_KING is not None: KING = U_KING

def cursor():
    im = Image.new("RGBA", (60, 60), (0, 0, 0, 0)); ImageDraw.Draw(im).polygon([(4, 4), (52, 24), (30, 30), (24, 54)], fill=PUR + (255,), outline=WHITE + (255,)); return im
CURSOR = cursor()

def orbits(dst, cx, cy, t, a):
    lay = canvas(); d = ImageDraw.Draw(lay)
    for rx, ry, sp in ((250, 250, .8), (205, 205, -1.1)):
        for k in range(0, 360, 8):
            if k % 16: continue
            a0 = math.radians(k); d.arc((cx - rx, cy - ry, cx + rx, cy + ry), k, k + 5, fill=(20, 20, 24, 255), width=3)
        ang = t * sp * 2; d.ellipse((cx + rx * math.cos(ang) - 14, cy + ry * math.sin(ang) - 14, cx + rx * math.cos(ang) + 14, cy + ry * math.sin(ang) + 14), fill=(20, 20, 24, 255))
        ang2 = ang + 2.6; d.ellipse((cx + rx * math.cos(ang2) - 9, cy + ry * math.sin(ang2) - 9, cx + rx * math.cos(ang2) + 9, cy + ry * math.sin(ang2) + 9), fill=(20, 20, 24, 255))
    paste(dst, lay, 0, 0, a, "lt")

# ---------------- escenas ----------------
def scene(i, T):
    t = T - CUT[i]; L = LS[i] - CUT[i]
    if i == 0:
        im = bgw(None); orbits(im, 360, 700, T, eo(prog(t, .2, .8)))
        pop(im, U_BRAIN if U_BRAIN is not None else BULB, 360, 700, t, .1, .45)
        rib = Image.new("RGBA", (620, 90), PUR + (255,)); ImageDraw.Draw(rib).text((310, 47), "¿ALGUNA VEZ TE PREGUNTASTE?", font=ANTON(50), fill=WHITE, anchor="mm")
        p = eo(prog(t, L, L + .35)); paste(im, rib.crop((0, 0, max(1, int(620 * p)), 90)), 50, 380, 1, "lm")
        return im
    if i == 1:
        im = BGP.copy(); s = lerp(1.9, 1.0, eo(prog(t, 0, .7)))
        for k, (dx, dy) in enumerate(((-128, -128), (128, -128), (-128, 128), (128, 128))):
            tl = TILES[k].resize((int(TILES[k].width * s), int(TILES[k].height * s))); paste(im, tl, 360 + dx * s, 690 + dy * s)
        lab = Image.new("RGBA", (380, 70), WHITE + (255,)); ImageDraw.Draw(lab).text((190, 36), "ALGUNAS MARCAS", font=ANTON(48), fill=PUR, anchor="mm")
        pop(im, lab, 360, 1060, t, L + .3, .3)
        return im
    if i == 2:
        im = bgw("mente"); b = (U_BRAIN if U_BRAIN is not None else (BULB_LIT if t > L + .5 else BULB))
        if t > L + .5:
            gl = Image.new("RGBA", (700, 700), (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((150, 150, 550, 550), fill=(255, 120, 230, 120)); paste(im, gl.filter(ImageFilter.GaussianBlur(70)), 360, 790)
        pop(im, b, 360, 820, t, .0, .45)
        word(im, "se quedan en", IT(600, 52), 360, 380, t, L, PUR); word(im, "tu mente?", IT(900, 92), 360, 470, t, L + .45, INK)
        return im
    if i == 3:
        im = BGP.copy(); word(im, "no es", IT(500, 60), 360, 380, t, L, WHITE); word(im, "Casualidad", IT(900, 110), 360, 490, t, L + .25, LILL)
        for k, (x, d0) in enumerate(((270, .0), (470, .12))):
            p = prog(t, d0, d0 + .8); y = lerp(-200, 900, eo(p)) - abs(math.sin(p * math.pi * 2.2)) * 120 * (1 - p)
            r = DIE.rotate((1 - eo(p)) * 400 * (1 if k else -1), expand=True, resample=Image.BICUBIC); paste(im, r, x, y, clamp01(p * 4))
        return im
    if i == 4:
        im = bgw("motion"); ex = lerp(900, 560, eo(prog(t, 0, .6))); e = EYE.rotate(-(1 - eo(prog(t, 0, .6))) * 200, resample=Image.BICUBIC)
        paste(im, e.resize((int(e.width * 1.25), int(e.height * 1.25))), ex, 760)
        word(im, "Motion", IT(900, 110), 270, 560, t, L - .05, PUR); word(im, "Design", IT(400, 96), 270, 670, t, L + .3, INK)
        cp = eo(prog(t, L + .3, L + .8)); paste(im, CURSOR, lerp(560, 300, cp), lerp(1000, 610, cp), clamp01(cp * 3), "lt")
        if L + .8 < t < L + 1.0: ImageDraw.Draw(im).ellipse((280, 590, 320, 630), outline=PUR + (255,), width=4)
        return im
    if i == 5:
        im = BGC.copy(); tvl = TV.copy(); idx = int(max(0, t - .2) / .45)
        tvl.alpha_composite(tv_screen(idx, t), (SCREEN[0], SCREEN[1])); pop(im, shadow(tvl, 26, 20, .35), 360, 900, t, 0, .45)
        word(im, "Emoción", IT(900, 104), 360, 330, t, L + .5, PUR); word(im, "a tu", IT(400, 50), 300, 430, t, L + .8, INK); word(im, "Historia", IT(900, 96), 410, 510, t, L + 1.1, INK)
        return im
    if i == 6:
        im = BGP.copy(); ws = [("Texto", IT(400, 56), 220, 330, WHITE), ("animado", IT(900, 104), 380, 420, WHITE), ("atrapa", IT(900, 92), 300, 650, WHITE),
                               ("miradas", IT(900, 104), 420, 760, WHITE), ("al instante", IT(400, 48), 470, 850, LILL)]
        for k, (s_, f, x, y, c) in enumerate(ws): word(im, s_, f, x, y, t, L + k * DUR_L[6] / 5.5, c)
        ep = eo(prog(t, L + .3, L + 1.0)); e = EYE.rotate((1 - ep) * 300, resample=Image.BICUBIC).resize((230, 230)); paste(im, e, lerp(360, 560, ep), lerp(1500, 1030, ep))
        return im
    if i == 7:
        im = bgw(None); word(im, "Metáforas", IT(900, 92), 360, 250, t, L - .05, PUR); word(im, "visuales", IT(400, 70), 360, 340, t, L + .35, INK)
        p = prog(t, L + .2, L + DUR_L[7]); card = chart_card(t, eo(p)); pop(im, card, 360, 760, t, .05, .45)
        word(im, "vuelven simple lo complicado", IT(400, 34), 360, 1120, t, L + DUR_L[7] * .55, INK)
        return im
    if i == 8:
        im = bgw(None); ImageDraw.Draw(im).rectangle((0, 900, W, H), fill=PUR + (255,))
        word(im, "esto no es", IT(500, 60), 360, 300, t, L, INK); word(im, "Decoración", IT(900, 104), 360, 400, t, L + .35, PUR)
        cy = lerp(1600, 980, eo(prog(t, 0, .6))); paste(im, COLUMN, 360, cy)
        dy = lerp(-200, 560, eo(prog(t, .2, .8))) + math.sin(t * 3) * 10; paste(im, shadow(DIAMOND, 30, 18, .3), 360, dy)
        return im
    if i == 9:
        im = BGP.copy(); word(im, "es", IT(500, 64), 200, 300, t, L, WHITE); word(im, "Movimiento", IT(900, 104), 340, 400, t, L + .15, WHITE)
        word(im, "estratégico.", IT(900, 96), 340, 500, t, L + .55, LILL)
        if KING is not None:
            p = eo(prog(t, .05, .75)); k = KING.rotate((1 - p) * 25, expand=True, resample=Image.BICUBIC); paste(im, k, lerp(620, 470, p), lerp(1700, 1010, p))
        return im
    im = bgw(None)
    if U_CROWN is not None: pop(im, U_CROWN, 360, 330 + math.sin(t * 2) * 8, t, L - .2, .45)
    word(im, "Duplex", IT(900, 120), 360, 520, t, L - .05, PUR); word(im, "Dragon", IT(900, 120), 360, 650, t, L + .2, PUR)
    word(im, "movámonos juntos", IT(400, 46), 360, 770, t, L + .9, INK); word(im, "@DuplexDragon_", SANS(400, 22), 360, 1180, t, L + 1.2, (120, 110, 130))
    return im

def frame(T):
    i = max(k for k in range(len(CUT)) if T >= CUT[k]); img = scene(i, T)
    dc = T - CUT[i]
    if i > 0 and dc < .12:   # flash de transición + golpe de escala
        col = WHITE if i in (3, 6, 9, 1) else LILL
        img = Image.blend(img, canvas(col + (255,)), .85 * (1 - dc / .12))
    if i > 0: img = scale_about(img, 1 + .05 * (1 - eo(clamp01(dc / .3))), bg=(255, 255, 255, 255))
    if T > TOTAL - .5: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, TOTAL - .5, TOTAL))
    return img.convert("RGB")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((W // 2, H // 2)) for t in ts]; sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for k, x in enumerate(ims): sh.paste(x, (k * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview", [round(c, 2) for c in CUT], round(TOTAL, 2)); sys.exit()
    out = a[0]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(TOTAL * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(TOTAL, 2))
