#!/usr/bin/env python3
"""Recreación del edit 'I'M ARTIST' (estilo motion-poster azul). 720x1280, 30 fps, 18.75 s.
Uso: python3 render.py [salida.mp4] [--audio guia.mp4] [--preview t1,t2,...]
Imágenes en ./images (opcionales, si faltan se usa un placeholder):
  a1_statue.png  a2_stage.png  a3_dancer.png  a4_singer.png  a5_drummer.png  a6_leaf.png
  (a3-a5 con fondo verde #00FF00 o PNG transparente)
"""
import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
IMG = os.path.join(HERE, "images")
W, H, FPS, DUR = 720, 1280, 30, 18.75

# ---------------- textos (cámbialos por los tuyos) ----------------
NAME = "TU NOMBRE"; USER = "@tu_usuario"; DATE = "13 NOV 2026"; MONTH = "Nov 2026"
TXT = dict(
    p1="Greatness is built quietly—through focus, discipline, and relentless commitment. When a person gives their best, their work naturally stands out and motivates",
    quote="True impact comes from consistent effort. When someone works with vision and dedication, their actions inspire many and create a powerful ripple of positive change.",
    caps="GREAT WORK SPEAKS BEFORE THE WORLD DOES. WHEN DEDICATION MEETS SKILL, IT INSPIRES PEOPLE, MOVES CROWDS, AND CREATES LASTING IMPACT. EVERY EFFORT, EVERY STEP, EVERY IDEA BUILDS A MOMENT WHERE EXCELLENCE STANDS AT THE CENTER.",
    p3="An artist transforms emotions into expression, turning imagination into reality. Their creativity inspires minds, connects hearts, and leaves a timeless impact through every stroke, note, or performance.",
    comment="Such a satisfying edit, everything feels balanced, clean, and very well thought out.",
)

NAVY = (28, 45, 62); BLACKB = (12, 23, 35); MID = (29, 58, 86); ACC = (31, 79, 128)
LAV = (232, 232, 244); WHITE = (255, 255, 255)

_fc = {}
def F(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONTS, name + ".ttf"), size)
    return _fc[k]
SERIF = lambda w, s, it=False: F(f"playfair-display-{w}-{'italic' if it else 'normal'}", s)
SANS = lambda w, s: F(f"poppins-{w}-normal", s)

# ---------------- easing ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def lerp(a, b, x): return a + (b - a) * x

# ---------------- helpers ----------------
def canvas(color=(0, 0, 0, 0)): return Image.new("RGBA", (W, H), color)

def text_layer(s, font, fill=WHITE, alpha=255):
    bb = font.getbbox(s); asc, desc = font.getmetrics()
    im = Image.new("RGBA", (bb[2] - bb[0] + 4, asc + desc + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - bb[0], 2), s, font=font, fill=fill + (alpha,))
    return im

def paste(dst, src, x, y, alpha=1.0, anchor="mm"):
    if alpha <= 0: return
    if alpha < 1:
        a = src.getchannel("A").point(lambda v: int(v * alpha)); src = src.copy(); src.putalpha(a)
    w, h = src.size
    ox = {"l": 0, "m": w / 2, "r": w}[anchor[0]]; oy = {"t": 0, "m": h / 2, "b": h}[anchor[1]]
    dst.alpha_composite(src, (int(round(x - ox)), int(round(y - oy)))) if 0 else _safe_comp(dst, src, int(round(x - ox)), int(round(y - oy)))

def _safe_comp(dst, src, x, y):
    # alpha_composite que tolera coordenadas fuera del lienzo
    sx0, sy0 = max(0, -x), max(0, -y)
    dx0, dy0 = max(0, x), max(0, y)
    w = min(src.width - sx0, dst.width - dx0); h = min(src.height - sy0, dst.height - dy0)
    if w <= 0 or h <= 0: return
    dst.alpha_composite(src.crop((sx0, sy0, sx0 + w, sy0 + h)), (dx0, dy0))

def word_reveal(dst, words, font, cx, y, starts, fill=WHITE, dur=0.22, t=0, gap=None, offs=None):
    """Palabras que aparecen una a una (fade + sube 18 px), centradas en cx."""
    gap = gap if gap is not None else font.size * 0.28
    lays = [text_layer(w, font, fill) for w in words]
    total = sum(l.width for l in lays) + gap * (len(lays) - 1)
    x = cx - total / 2
    for i, l in enumerate(lays):
        p = eo(prog(t, starts[i], starts[i] + dur))
        dy = (offs[i] if offs else 0)
        if p > 0: paste(dst, l, x, y + dy + 18 * (1 - p), p, "lm")
        x += l.width + gap

def typed(s, t, a, cps=60):
    n = int(max(0, (t - a)) * cps); return s[:n]

def wrap(s, font, maxw):
    lines, cur = [], ""
    for w in s.split():
        tst = (cur + " " + w).strip()
        if font.getlength(tst) > maxw and cur: lines.append(cur); cur = w
        else: cur = tst
    if cur: lines.append(cur)
    return lines

def para(dst, s, font, cx, y, maxw, fill, alpha=1.0, lh=1.35):
    for i, ln in enumerate(wrap(s, font, maxw)):
        paste(dst, text_layer(ln, font, fill), cx, y + i * font.size * lh, alpha, "mt")

def rrect(size, r, fill, outline=None, width=0):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=fill, outline=outline, width=width)
    return im

def circle(r, color, blur=0):
    pad = int(blur * 3)
    im = Image.new("RGBA", (2 * r + 2 * pad, 2 * r + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((pad, pad, pad + 2 * r, pad + 2 * r), fill=color)
    return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im

def dashed_rect(d, box, color, dash=8, gap=6, width=2):
    x0, y0, x1, y1 = box
    for (ax, ay, bx, by) in [(x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)]:
        L = math.hypot(bx - ax, by - ay); n = int(L // (dash + gap)) + 1
        for i in range(n):
            s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
            d.line((ax + (bx - ax) * s, ay + (by - ay) * s, ax + (bx - ax) * e, ay + (by - ay) * e), fill=color, width=width)

def scale_about(img, s, cx=W / 2, cy=H / 2, bg=(0, 0, 0, 0)):
    if abs(s - 1) < 1e-4: return img
    nw, nh = int(W * s), int(H * s)
    sm = img.resize((nw, nh), Image.BILINEAR)
    out = Image.new("RGBA", (W, H), bg)
    _safe_comp(out, sm, int(cx - cx * s), int(cy - cy * s))
    return out

def _shift(a, d, axis):
    d = int(d)
    if d == 0: return a
    idx = np.clip(np.arange(a.shape[axis]) - d, 0, a.shape[axis] - 1)
    return np.take(a, idx, axis=axis)

def motion_blur_x(img, px, n=6):
    if abs(px) < 2: return img
    acc = np.zeros((img.height, img.width, 4), np.float32); a = np.asarray(img, np.float32)
    for i in range(n):
        acc += _shift(a, px * (i / (n - 1) - .5), 1)
    return Image.fromarray((acc / n).astype(np.uint8), "RGBA")

def motion_blur_y(img, px, n=6):
    if abs(px) < 2: return img
    acc = np.zeros((img.height, img.width, 4), np.float32); a = np.asarray(img, np.float32)
    for i in range(n):
        acc += _shift(a, px * (i / (n - 1) - .5), 0)
    return Image.fromarray((acc / n).astype(np.uint8), "RGBA")

def offset(img, dx, dy, bg=(0, 0, 0, 0)):
    out = Image.new("RGBA", (W, H), bg); _safe_comp(out, img, int(dx), int(dy)); return out

def persp_coeffs(src, dst):
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(m, float); B = np.array([p for pt in src for p in pt], float)
    return np.linalg.solve(A, B).tolist()

def rotate_y(img, deg, f=1100):
    """Gira una capa en 3D sobre el eje Y (perspectiva)."""
    if abs(deg) < .3: return img, (0, 0)
    w, h = img.size; th = math.radians(deg); pts = []
    for (x, y) in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        xr, z = x * math.cos(th), x * math.sin(th)
        k = f / (f + z); pts.append((xr * k, y * k))
    minx = min(p[0] for p in pts); miny = min(p[1] for p in pts)
    maxx = max(p[0] for p in pts); maxy = max(p[1] for p in pts)
    dst = [(p[0] - minx, p[1] - miny) for p in pts]
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    out = img.transform((int(maxx - minx) + 1, int(maxy - miny) + 1), Image.PERSPECTIVE, persp_coeffs(src, dst), Image.BICUBIC)
    return out, ((minx + maxx) / 2, (miny + maxy) / 2)

# ---------------- imágenes ----------------
def load(name, size, kind):
    p = os.path.join(IMG, name + ".png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGBA")
        if kind == "cut":  # quitar fondo verde
            a = np.asarray(im).astype(np.int16)
            g = (a[..., 1] - np.maximum(a[..., 0], a[..., 2]))
            alpha = np.clip(255 - (g - 40) * 4, 0, 255).astype(np.uint8)
            alpha = np.minimum(alpha, a[..., 3].astype(np.uint8))
            a2 = a.copy(); a2[..., 1] = np.minimum(a[..., 1], np.maximum(a[..., 0], a[..., 2]) + 10)  # despill
            im = Image.fromarray(np.dstack([a2[..., :3].astype(np.uint8), alpha]), "RGBA")
            bb = im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
            if bb: im = im.crop(bb)
        im.thumbnail(size, Image.LANCZOS) if kind == "cut" else None
        if kind != "cut": im = fit_cover(im, size)
        return im
    # placeholder
    im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    light = kind == "light"
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), 28, fill=(200, 205, 222, 255) if light else (40, 70, 105, 200),
                        outline=NAVY + (255,) if light else (150, 180, 215, 255), width=3)
    lab = name.split("_", 1)[1].upper()
    f = SANS(700, 30)
    d.text((size[0] / 2, size[1] / 2), "IMAGEN\n" + lab, font=f, fill=NAVY if light else WHITE, anchor="mm", align="center")
    return im

def fit_cover(im, size):
    r = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    l = (im.width - size[0]) // 2; t = (im.height - size[1]) // 2
    return im.crop((l, t, l + size[0], t + size[1]))

STATUE = load("a1_statue", (400, 430), "light")
STAGE = load("a2_stage", (392, 300), "dark")
ARTISTS = [load("a3_dancer", (470, 600), "cut"), load("a4_singer", (440, 600), "cut"), load("a5_drummer", (520, 560), "cut")]
LEAF = None
if os.path.exists(os.path.join(IMG, "a6_leaf.png")):
    lf = Image.open(os.path.join(IMG, "a6_leaf.png")).convert("L").resize((420, 420))
    LEAF = Image.new("RGBA", lf.size, NAVY + (0,)); LEAF.putalpha(ImageChops.invert(lf).point(lambda v: 255 if v > 90 else 0))
else:  # hoja de palma vectorial
    LEAF = Image.new("RGBA", (420, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(LEAF)
    cx, cy = 210, 330
    for k in range(9):
        ang = math.radians(-160 + k * 17.5); L = 190 + 30 * math.sin(k)
        tip = (cx + L * math.cos(ang), cy + L * math.sin(ang))
        n = (-math.sin(ang) * 16, math.cos(ang) * 16)
        mid = (cx + L * .5 * math.cos(ang), cy + L * .5 * math.sin(ang))
        d.polygon([(cx, cy), (mid[0] + n[0], mid[1] + n[1]), tip, (mid[0] - n[0], mid[1] - n[1])], fill=NAVY + (255,))
    d.line((cx, cy, cx + 10, 415), fill=NAVY + (255,), width=8)

def leaf(color, blur, scale=1.0, rot=0):
    l = LEAF.resize((int(420 * scale), int(420 * scale)))
    if color != NAVY:
        c = Image.new("RGBA", l.size, color + (255,)); c.putalpha(l.getchannel("A")); l = c
    l = l.rotate(rot, expand=True, resample=Image.BICUBIC)
    return l.filter(ImageFilter.GaussianBlur(blur)) if blur else l

LEAF_LIGHT = [leaf(NAVY, 10, 0.9), leaf(NAVY, 6, 0.7)]
LEAF_BLUE = leaf(ACC, 14, 1.1)

# ---------------- granos / polvo ----------------
rng = np.random.default_rng(7)
GRAIN = [Image.fromarray(np.clip(rng.normal(128, 38, (H // 2, W // 2)), 0, 255).astype(np.uint8)).resize((W, H)) for _ in range(6)]
DUST = []
for k in range(6):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(k)
    for _ in range(160):
        x, y, s = r.randrange(W), r.randrange(H), r.choice([1, 1, 1, 2, 2, 3])
        d.ellipse((x, y, x + s, y + s), fill=(255, 255, 255, r.randrange(60, 200)))
    for _ in range(6):
        x, y = r.randrange(W), r.randrange(H)
        d.line((x, y, x + r.randrange(-30, 30), y + r.randrange(10, 60)), fill=(255, 255, 255, 90), width=1)
    DUST.append(im)

def add_grain(img, amount, t):
    g = GRAIN[int(t * FPS) % len(GRAIN)]
    rgb = img.convert("RGB")
    over = Image.merge("RGB", (g, g, g))
    blended = ImageChops.overlay(rgb, over)
    return Image.blend(rgb, blended, amount).convert("RGBA")

# ================= ESCENA 1: póster claro =================
def bg_light():
    a = np.zeros((H, W, 3), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .45) / H) ** 2)
    for i, c in enumerate(LAV): a[..., i] = c + 14 * (1 - np.clip(r * 1.6, 0, 1)) - 8 * np.clip(r - .4, 0, 1)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    # cuadrícula con desvanecido radial
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
    for x in range(80, 650, 22): gd.line((x, 360, x, 940), fill=(170, 178, 200, 255), width=1)
    for y in range(360, 950, 22): gd.line((80, y, 640, y), fill=(170, 178, 200, 255), width=1)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).ellipse((40, 330, 680, 980), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(70))
    grid.putalpha(ImageChops.multiply(grid.getchannel("A"), mask))
    im.alpha_composite(grid)
    return im
BG1 = bg_light()

def barcode():
    im = Image.new("RGBA", (130, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(3); x = 4
    while x < 120:
        w = r.choice([1, 1, 2, 3]); d.rectangle((x, 22, x + w - 1, 46), fill=NAVY + (255,)); x += w + r.choice([1, 2])
    d.text((65, 10), DATE, font=SANS(400, 13), fill=NAVY, anchor="mm")
    d.text((65, 54), "5 012345 678900", font=SANS(400, 9), fill=NAVY, anchor="mm")
    return im
BARCODE = barcode()

def cursor_img():
    im = Image.new("RGBA", (44, 44), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon([(2, 2), (40, 16), (22, 22), (16, 40)], fill=NAVY + (255,))
    return im
CURSOR = cursor_img()

def scene1(t):
    im = BG1.copy()
    # línea curva que se dibuja
    d = ImageDraw.Draw(im)
    p = eo(prog(t, 0.2, 1.6)); pts = []
    for i in range(int(60 * p) + 1):
        u = i / 60; pts.append((-40 + 820 * u, 260 - 300 * math.sin(u * 1.2) + 40 * u))
    if len(pts) > 1: d.line(pts, fill=NAVY + (255,), width=2)
    pts2 = [(-40 + 820 * (i / 60), 1080 + 120 * math.sin(i / 60 * 2.4)) for i in range(int(60 * eo(prog(t, 0.8, 2.2))) + 1)]
    if len(pts2) > 1: d.line(pts2, fill=NAVY + (255,), width=2)
    paste(im, BARCODE, 640, 70, 1, "rm")
    paste(im, text_layer(NAME, SANS(400, 15), NAVY), 70, 1190, prog(t, .3, .6), "lm")
    # estatua: pixelada/borrosa -> nítida
    ps = eo(prog(t, 0.35, 0.95))
    if ps > 0:
        st = STATUE
        if ps < 1:
            k = max(1, int(28 * (1 - ps)))
            st = st.resize((max(1, st.width // k), max(1, st.height // k)), Image.NEAREST).resize(st.size, Image.NEAREST)
            st = st.filter(ImageFilter.GaussianBlur(6 * (1 - ps)))
        paste(im, st, 360, 680, ps)
    # título tipeado con recuadro punteado
    box = (150, 290, 570, 450)
    if t > 0.05:
        dashed_rect(ImageDraw.Draw(im), box, NAVY + (255,), 6, 4, 2)
        paste(im, text_layer(typed("ak", t, .05, 20), SERIF(800, 34), NAVY), 170, 318, 1, "lm")
        s = typed("ARTIST", t, .15, 14)
        if s: paste(im, text_layer(s, SERIF(900, 88), NAVY), 168, 382, 1, "lm")
        if t > .6: paste(im, text_layer("ko", SERIF(800, 34), NAVY), 555, 428, 1, "rm")
    word_reveal(im, ["Paise", "ke", "alwa"], SERIF(500, 58), 360, 945, [1.25, 1.42, 1.58], NAVY, t=t)
    pp = eo(prog(t, 1.95, 2.2))
    if pp > 0:
        pill = rrect((360, 46), 4, NAVY + (255,))
        ImageDraw.Draw(pill).text((180, 23), "KYA CHAIYE HOTA HAI ?", font=SERIF(500, 24, True), fill=WHITE, anchor="mm")
        pw = int(360 * pp); paste(im, pill.crop((0, 0, max(1, pw), 46)), 180, 1012, 1, "lm")
    s = typed(TXT["p1"], t, 0.9, 110)
    if s: para(im, s, SANS(400, 17), 360, 1068, 560, NAVY)
    # cursor
    path = [(0, (430, 150)), (.6, (520, 360)), (1.2, (470, 900)), (1.9, (520, 1060)), (2.6, (560, 1080))]
    for (t0, p0), (t1, p1) in zip(path, path[1:]):
        if t0 <= t <= t1:
            e = eio(prog(t, t0, t1)); paste(im, CURSOR, lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e), 1, "lt")
    if t > path[-1][0]: paste(im, CURSOR, *path[-1][1], 1, "lt")
    # hojas desenfocadas que se mecen
    sw = math.sin(t * 2.2) * 8
    paste(im, LEAF_LIGHT[0].rotate(150 + sw, expand=True), -150, -170, .9, "lt")
    paste(im, LEAF_LIGHT[1].rotate(-30 - sw, expand=True), W + 130, H + 110, .9, "rb")
    return scale_about(im, 1 + 0.03 * t / 2.6, bg=LAV + (255,))

# ================= ESCENA 2: tarjeta Instagram 3D =================
def make_card():
    cw, ch = 430, 500
    c = rrect((cw, ch), 18, (250, 250, 252, 255)); d = ImageDraw.Draw(c)
    d.ellipse((18, 14, 46, 42), fill=(214, 41, 118))
    d.ellipse((23, 19, 41, 37), fill=WHITE); d.ellipse((27, 23, 37, 33), fill=(214, 41, 118))
    d.text((56, 28), USER.strip("@") + " ·", font=SANS(500, 15), fill=(30, 30, 30), anchor="lm")
    d.text((56 + SANS(500, 15).getlength(USER.strip("@") + " · "), 28), "Follow", font=SANS(600, 15), fill=(0, 149, 246), anchor="lm")
    d.text((cw - 22, 28), "⋮", font=SANS(700, 18), fill=(40, 40, 40), anchor="mm")
    c.alpha_composite(STAGE, (19, 52))
    y = 52 + 300 + 26
    d.text((22, y), "♥", font=F("../fonts/poppins-400-normal", 1) if 0 else SANS(700, 26), fill=(237, 73, 86), anchor="lm") if 0 else d.ellipse((22, y - 11, 44, y + 11), fill=(237, 73, 86))
    d.ellipse((58, y - 11, 80, y + 11), outline=(30, 30, 30), width=2)
    d.polygon([(96, y - 10), (118, y - 2), (100, y + 10)], outline=(30, 30, 30))
    d.rectangle((cw - 36, y - 11, cw - 22, y + 11), fill=(30, 30, 30))
    d.text((22, y + 34), "2.018 Likes", font=SANS(500, 16), fill=(30, 30, 30), anchor="lm")
    d.text((22, y + 64), "Viral Reel edit", font=SANS(500, 16), fill=(30, 30, 30), anchor="lm")
    d.text((160, y + 64), "#edit #reels", font=SANS(500, 16), fill=(0, 149, 246), anchor="lm")
    # grosor (canto) para efecto 3D
    full = Image.new("RGBA", (cw + 14, ch + 14), (0, 0, 0, 0))
    full.alpha_composite(rrect((cw, ch), 18, (175, 178, 186, 255)), (12, 12))
    full.alpha_composite(c, (0, 0))
    return full
CARD = make_card()

def bg_dark_orbs():
    im = canvas(BLACKB[:2] + (BLACKB[2],) + (255,)); im = canvas((5, 9, 15, 255))
    paste(im, circle(170, ACC + (255,), 2), 70, 150)
    paste(im, circle(140, ACC + (255,), 30), 760, 40)
    paste(im, circle(230, ACC + (230,), 45), 640, 1240)
    paste(im, circle(150, MID + (255,), 40), 60, 1050)
    d = ImageDraw.Draw(im); d.arc((-330, 1060, 130, 1520), 280, 360, fill=(220, 225, 235, 255), width=3)
    return im
BG2 = bg_dark_orbs()

def corner_frame(d, box, col, L=34, w=2):
    x0, y0, x1, y1 = box
    d.line((x0, y0, x0 + L, y0), fill=col, width=w); d.line((x0, y0, x0, y0 + L), fill=col, width=w)
    d.line((x1, y1, x1 - L, y1), fill=col, width=w); d.line((x1, y1, x1, y1 - L), fill=col, width=w)

def scene2(t):  # t local desde 2.8
    im = BG2.copy(); d = ImageDraw.Draw(im)
    qa = prog(t, .1, .5)
    corner_frame(d, (80, 70, 640, 190), (150, 160, 180, int(255 * qa)))
    s = typed(TXT["quote"], t, .15, 120)
    if s: para(im, s, SANS(400, 18), 360, 88, 520, (225, 228, 235))
    # tarjeta: entra desde abajo-derecha girando en 3D
    e = eo(prog(t, 0.0, 0.7))
    ang = lerp(48, 6, e) + math.sin(t * 1.6) * 3
    card = CARD.rotate(lerp(-14, 0, e), expand=True, resample=Image.BICUBIC)
    card, _ = rotate_y(card, ang)
    fl = math.sin(t * 2) * 6
    paste(im, card, lerp(620, 360, e), lerp(1150, 545, e) + fl)
    word_reveal(im, ["OFCOURSE", "USKE"], SERIF(500, 38, True), 360, 1010, [0.6, 0.85], WHITE, t=t)
    pb = eo(prog(t, 1.15, 1.4))
    if pb > 0: dashed_rect(ImageDraw.Draw(im), (110, 1040, 610, 1114), (230, 232, 240, int(255 * pb)), 9, 6, 2)
    word_reveal(im, ["KAAM", "KI", "TARIF"], SERIF(900, 50), 360, 1077, [1.2, 1.4, 1.6], WHITE, t=t)
    s = typed(TXT["caps"], t, 1.0, 160)
    if s: para(im, s, SANS(400, 12), 360, 1135, 470, (210, 214, 224))
    return im

# ================= ESCENA 3: artistas =================
def bg_spot():
    im = canvas((4, 10, 18, 255))
    paste(im, circle(330, ACC + (255,), 90), 360, 590)
    paste(im, circle(180, (60, 110, 170, 255), 70), 360, 560)
    d = ImageDraw.Draw(im); d.arc((380, -260, 900, 260), 100, 200, fill=ACC + (255,), width=26)
    return im.filter(ImageFilter.GaussianBlur(4))
BG3 = bg_spot()
BUBBLES = [(random.Random(i).randrange(40, 680), random.Random(i + 50).randrange(150, 1200), random.Random(i + 9).randrange(14, 46)) for i in range(9)]
LABELS = ["NACHNE WALA", "GAANE WALA", "BAJANE WALA"]

def pill_label(txt):
    f = SANS(800, 40); w = int(f.getlength(txt)) + 70
    p = rrect((w, 74), 37, NAVY + (255,), (235, 238, 245, 255), 3)
    ImageDraw.Draw(p).text((w / 2, 38), txt, font=f, fill=WHITE, anchor="mm")
    return p

def scene3(t):  # t local desde 5.5
    im = BG3.copy()
    for i, (x, y, r) in enumerate(BUBBLES):
        yy = (y - t * (18 + i * 3)) % 1300 - 10
        paste(im, circle(r, ACC + (255,), 0 if i % 3 else 6), x + math.sin(t + i) * 8, yy, .9)
    word_reveal(im, ["Fhir", "chahe", "wo"], SERIF(900, 36), 360, 210, [0.05, 0.2, 0.35], WHITE, t=t)
    cuts = [0.0, 1.2, 2.3]; idx = 0 if t < cuts[1] else (1 if t < cuts[2] else 2)
    lt = t - cuts[idx]
    # entrada lateral con blur
    e = eo(prog(lt, 0, .3)) if idx > 0 else 1.0
    nxt_out = (idx < 2 and t > cuts[idx + 1] - .25)
    ox = (1 - e) * 560
    if nxt_out: ox = -eo(prog(t, cuts[idx + 1] - .25, cuts[idx + 1])) * 560
    art = ARTISTS[idx]; sc = 1 + .04 * lt
    a2 = art.resize((int(art.width * sc), int(art.height * sc)), Image.BILINEAR)
    layer = canvas(); paste(layer, a2, 360 + ox, 900, 1, "mb")
    pl = pill_label(LABELS[idx]); paste(layer, pl, 360 + ox * .7, 972)
    if abs(ox) > 3: layer = motion_blur_x(layer, ox * .12)
    im.alpha_composite(layer)
    para(im, TXT["p3"], SANS(400, 17), 360, 1030, 600, (220, 225, 235), prog(t, .3, .6))
    return scale_about(im, 1 + .025 * t, bg=(4, 10, 18, 255))

# ================= ESCENA 4: panel de vidrio =================
def bg_grad():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    k = np.clip((xx / W * .35 + yy / H * .9) - .25, 0, 1) ** 1.4
    a = np.zeros((H, W, 3), np.float32)
    for i, (c0, c1) in enumerate(zip((2, 4, 8), (28, 72, 120))): a[..., i] = c0 + (c1 - c0) * k
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    paste(im, LEAF_BLUE.rotate(140, expand=True), 600, 60, .9)
    paste(im, LEAF_BLUE.rotate(-20, expand=True), 40, 1250, .6)
    return im
BG4 = bg_grad()
PANEL = (60, 380, 660, 790)

def comment_card(name="Nisha", user="@nishren"):
    c = rrect((520, 120), 30, (222, 224, 230, 245)); d = ImageDraw.Draw(c)
    d.ellipse((22, 18, 58, 54), fill=(150, 110, 90)); d.ellipse((30, 22, 50, 42), fill=(205, 165, 140))
    d.text((70, 26), name, font=SANS(600, 17), fill=(20, 20, 25), anchor="lm")
    d.text((70, 46), user, font=SANS(400, 12), fill=(90, 90, 100), anchor="lm")
    lines = wrap(TXT["comment"], SANS(400, 15), 440); y = 74
    for i, ln in enumerate(lines[:2]):
        x = 70 if i == 0 else 60
        if i == 0:
            hl = "Such a satisfying edit,"; d.text((x, y), hl, font=SANS(400, 15), fill=(40, 90, 230), anchor="lm")
            d.text((x + SANS(400, 15).getlength(hl + " "), y), ln[len(hl):].strip(), font=SANS(400, 15), fill=(25, 25, 30), anchor="lm")
        else: d.text((x, y), ln, font=SANS(400, 15), fill=(25, 25, 30), anchor="lm")
        y += 21
    return c
CCARD = comment_card()

def glass(base, box, t):
    x0, y0, x1, y1 = box
    reg = base.crop(box).filter(ImageFilter.GaussianBlur(22))
    reg = ImageEnhance.Brightness(reg).enhance(1.18)
    tint = Image.new("RGBA", reg.size, (255, 255, 255, 14)); reg.alpha_composite(tint)
    # brillo esquina superior izquierda
    hl = circle(170, (140, 190, 240, 70), 60); _safe_comp(reg, hl, -180, -200)
    m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), 34, fill=255)
    base.paste(reg, (x0, y0), m)
    ImageDraw.Draw(base).rounded_rectangle(box, 34, outline=(200, 215, 235, 120), width=2)

def scene4(t):  # t local desde 9.1
    im = BG4.copy()
    if t < 1.2: para(im, TXT["p3"], SANS(400, 17), 360, 330, 600, (220, 226, 236), 1 - prog(t, .6, 1.1))
    a = eo(prog(t, 0, .4))
    layer = im.copy(); glass(layer, PANEL, t)
    # barrido de luz
    sp = prog(t, .1, .6)
    if 0 < sp < 1:
        sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sweep)
        x = lerp(-200, 900, sp); sd.polygon([(x, 380), (x + 90, 380), (x - 60, 790), (x - 150, 790)], fill=(255, 255, 255, 50))
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(PANEL, 34, fill=255)
        sweep.putalpha(ImageChops.multiply(sweep.getchannel("A"), m)); layer.alpha_composite(sweep.filter(ImageFilter.GaussianBlur(8)))
    im = Image.blend(im, layer, a)
    # tarjetas que caen y se barajan
    for k, st in enumerate([0.55, 0.65, 0.75, 0.85]):
        e = eo(prog(t, st, st + .45))
        if e <= 0: continue
        settle = k == 3
        dx = 0 if settle else (k - 1.5) * 10 * (1 - prog(t, 1.3, 1.6))
        y = lerp(300, 600, e) + (0 if settle else -k * 8 * (1 - prog(t, 1.3, 1.6)))
        al = 1 if settle else (1 - prog(t, 1.3, 1.6)) * .85
        paste(im, CCARD, 360 + dx, y, al)
    word_reveal(im, ["Par", "Main", "Hun", "Kon"], SANS(400, 34), 360, 470, [2.3, 2.55, 2.8, 3.05], WHITE, t=t, offs=[0, -4, 4, 22])
    return im

# ================= ESCENA 5: I'M / ARTIST =================
def bg_end():
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32); k = np.clip((yy / H - .45) / .55, 0, 1) ** 1.6
    a = np.zeros((H, W, 3), np.float32)
    for i, (c0, c1) in enumerate(zip((3, 5, 9), (26, 62, 104))): a[..., i] = c0 + (c1 - c0) * k
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    paste(im, circle(260, (30, 70, 115, 255), 120), 600, 120, .8)
    return im
BG5 = bg_end()

def scene5a(t):  # desde 13.3
    im = BG5.copy(); im.alpha_composite(DUST[int(t * 12) % 6])
    s = lerp(3.2, 1.0, eo(prog(t, 0, 1.5)))
    f = SANS(800, int(120 * s)); l = text_layer("I’M", f)
    if t < .3: l = l.filter(ImageFilter.GaussianBlur(10 * (1 - t / .3)))
    paste(im, l, 360, 640)
    return im

CORNERS = [(NAME, 70, 140, "lm"), ("VFX ARTIST", 650, 140, "rm"), (USER.upper(), 70, 1080, "lm"), ("EDITS", 650, 1080, "rm")]
def scene5b(t):  # desde 15.0
    im = BG5.copy(); im.alpha_composite(DUST[int(t * 12) % 6])
    e = eo(prog(t, 0, .35)); ox = (1 - e) * 600
    layer = canvas()
    paste(layer, text_layer("ARTIST", SANS(800, 118)), 360 + ox, 650)
    paste(layer, text_layer("Made with after effect", SERIF(400, 24)), 650 + ox, 575, prog(t, .3, .6), "rm")
    if ox > 3: layer = motion_blur_x(layer, ox * .15)
    im.alpha_composite(layer)
    for i, (s, x, y, a) in enumerate(CORNERS):
        tx = typed(s, t, .4 + i * .15, 30)
        if tx: paste(im, text_layer(tx, SERIF(400, 22, True), (225, 228, 236)), x, y, 1, a)
    return im

# ================= bordes verticales =================
def edge_text():
    im = canvas()
    for items, x in [((NAME.lower(), USER, MONTH), 30), (("Made by after effect", USER), 690)]:
        y = 240
        for s in items:
            l = text_layer(s, SANS(400, 14), (200, 205, 215)).rotate(90, expand=True)
            paste(im, l, x, y + l.height / 2, 1, "mm"); y += l.height + 70
    return im
EDGE = edge_text()

# ================= línea de tiempo =================
def frame(T):
    if T < 2.5: img = scene1(T)
    elif T < 2.9:  # push hacia arriba
        e = eio(prog(T, 2.5, 2.9))
        a = offset(scene1(T), 0, -H * e, LAV + (255,)); b = offset(scene2(T - 2.8 + .1 * 0), 0, H * (1 - e))
        a = offset(scene1(T), 0, 0, LAV + (255,)); top = int(H * (1 - e))
        img = canvas((5, 9, 15, 255)); img.alpha_composite(b)
        if top > 0: img.paste(scene1(T).crop((0, int(H * e), W, H)), (0, 0))
        img = motion_blur_y(img, 28 * math.sin(math.pi * e), 12)
    elif T < 5.25: img = scene2(T - 2.8)
    elif T < 5.65:
        e = eio(prog(T, 5.25, 5.65))
        a = offset(scene2(T - 2.8), -W * e, 0); b = offset(scene3(T - 5.5), W * (1 - e), 0)
        img = canvas((4, 10, 18, 255)); img.alpha_composite(a); img.alpha_composite(b)
        img = motion_blur_x(img, 40 * math.sin(math.pi * e), 12)
    elif T < 8.95: img = scene3(T - 5.5)
    elif T < 9.35:
        e = eio(prog(T, 8.95, 9.35))
        a = offset(scale_about(scene3(T - 5.5), 1 + .3 * e), 0, -H * e); b = offset(scene4(T - 9.1), 0, H * (1 - e))
        img = canvas((4, 10, 18, 255)); img.alpha_composite(b); img.alpha_composite(a)
        img = motion_blur_y(img, 30 * math.sin(math.pi * e), 12)
    elif T < 12.85: img = scene4(T - 9.1)
    elif T < 13.3:
        e = eio(prog(T, 12.85, 13.25))
        s4 = scene4(T - 9.1).filter(ImageFilter.GaussianBlur(10 * e))
        s4 = ImageEnhance.Color(s4).enhance(1 - .8 * e)
        img = scale_about(s4, 1 - .3 * e, bg=(10, 12, 16, 255))
        img = Image.blend(img, add_grain(img, 1, T), .5 * e)
        if 13.17 <= T < 13.27: img = canvas((250, 250, 252, 255))  # FLASH blanco
    elif T < 14.75: img = scene5a(T - 13.3)
    elif T < 15.1:
        e = eio(prog(T, 14.75, 15.1))
        a = offset(scene5a(T - 13.3), -W * e, 0)
        img = BG5.copy(); img.alpha_composite(a); img = motion_blur_x(img, 70 * math.sin(math.pi * e))
        if T >= 15.0: img = scene5b(T - 15.0)
    else: img = scene5b(T - 15.0)
    # capas globales
    if T > 2.8: img.alpha_composite(EDGE)
    amt = .10 if T < 2.6 else (.18 if T < 13.3 else .32)
    img = add_grain(img, amt, T)
    vig = VIG; img.alpha_composite(vig)
    if T > 17.4: img = Image.blend(img, canvas((0, 0, 0, 255)), prog(T, 17.4, 18.7) * .9)
    return img.convert("RGB")

def vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a = (np.clip(r - .75, 0, 1) * 150).astype(np.uint8)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); im.putalpha(Image.fromarray(a)); return im
VIG = vignette()

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--preview" in args:
        ts = [float(x) for x in args[args.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((W // 2, H // 2)) for t in ts]
        sheet = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for i, x in enumerate(ims): sheet.paste(x, (i * W // 2, 0))
        sheet.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview.jpg"); sys.exit()
    out = args[0] if args and not args[0].startswith("--") else os.path.join(HERE, "artist_edit.mp4")
    audio = args[args.index("--audio") + 1] if "--audio" in args else None
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 60 == 0: print(f"{i}/{n}", flush=True)
    p.stdin.close(); p.wait(); print("OK", out)
