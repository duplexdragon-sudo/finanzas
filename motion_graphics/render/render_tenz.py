#!/usr/bin/env python3
"""EL REY VOLVIÓ: motion graphic rojo/negro, imágenes en gris, 60 s, sincronizado con HEAVENLY JUMPSTYLE (129 BPM).
Uso: python3 render_tenz.py salida.mp4 --audio cancion.mp3 [--fps 60] | --preview t1,t2,...
Clips opcionales (se ponen en gris automáticamente): ../tenz/clips/clip1.mp4 (17.6-23.7 s) y clip2.mp4 (51-58 s)
"""
import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance, ImageFont
import render as R
from render import (W, H, text_layer, paste, para, rrect, circle, scale_about, motion_blur_x, offset, add_grain, DUST,
                    prog, eo, eio, lerp, SERIF, SANS, canvas, _safe_comp, F)

HERE = os.path.dirname(os.path.abspath(__file__)); TZ = os.path.join(HERE, "..", "tenz")
DUR = 60.0
NAME = "TU NOMBRE"; USER = "@tu_usuario"
BLACK = (11, 11, 12); RED = (225, 6, 0); DRED = (122, 0, 0); WHITE = (242, 242, 242); GREY = (150, 150, 150)
ANTON = lambda s: F("anton-400-normal", s)
BEATS = np.load(os.path.join(TZ, "beats.npy")) if os.path.exists(os.path.join(TZ, "beats.npy")) else np.arange(1.46, 60, 60 / 129.2)

# ---------------- fondo: negro con luz de persiana ----------------
def bg_base():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 14 + 10 * np.exp(-(((xx - W * .5) / W) ** 2 + ((yy - H * .35) / H) ** 2) * 3)
    im = Image.fromarray(np.dstack([v, v * .97, v * .97]).astype(np.uint8)).convert("RGBA")
    blinds = Image.new("L", (W * 2, H * 2), 0); d = ImageDraw.Draw(blinds)
    for k in range(-10, 30):
        x = k * 120; d.polygon([(x, 0), (x + 55, 0), (x + 55 - 900, H * 2), (x - 900, H * 2)], fill=34)
    blinds = blinds.filter(ImageFilter.GaussianBlur(18)).crop((300, 0, 300 + W, H))
    light = Image.new("RGBA", (W, H), (255, 245, 240, 0)); light.putalpha(blinds)
    im.alpha_composite(light); return im
BG = bg_base()

def ghost(word, t):
    f = ANTON(330); l = text_layer(word, f, (255, 255, 255))
    a = l.getchannel("A").point(lambda v: int(v * .07)); l.putalpha(a)
    return l

def stars(n=3):
    im = Image.new("RGBA", (90, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(n):
        cx, cy, r = 14 + i * 28, 15, 10
        d.polygon([(cx, cy - r), (cx + 2.5, cy - 2.5), (cx + r, cy), (cx + 2.5, cy + 2.5), (cx, cy + r), (cx - 2.5, cy + 2.5), (cx - r, cy), (cx - 2.5, cy - 2.5)], fill=WHITE + (255,))
    return im
STARS = stars()

def spark_line(h=300):
    im = Image.new("RGBA", (40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((20, 30, 20, h + 30), fill=(230, 230, 230, 200), width=2)
    cx, cy, r = 20, 26, 18
    d.polygon([(cx, cy - r), (cx + 3, cy - 3), (cx + r * .6, cy), (cx + 3, cy + 3), (cx, cy + r), (cx - 3, cy + 3), (cx - r * .6, cy), (cx - 3, cy - 3)], fill=(255, 255, 255, 255))
    return im
SPARK = spark_line()

# ---------------- imágenes originales en gris ----------------
def ss(fn, size, k=2):
    big = fn((size[0] * k, size[1] * k), k); return big.resize(size, Image.LANCZOS)

def crown_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    base_y = h * .78; top = h * .18; pts = [(w * .08, base_y)]
    tips = [.08, .29, .5, .71, .92]
    for i, x in enumerate(tips):
        pts.append((w * x, top if i % 2 == 0 else top + h * .12))
        if i < 4: pts.append((w * (x + .105), h * .5))
    pts.append((w * .92, base_y))
    # degradado metálico vertical
    grad = Image.new("L", size); gd = ImageDraw.Draw(grad)
    for y in range(h): gd.line((0, y, w, y), fill=int(70 + 150 * (0.5 + 0.5 * math.cos((y / h) * 5.5))))
    mask = Image.new("L", size, 0); md = ImageDraw.Draw(mask); md.polygon(pts, fill=255)
    md.rounded_rectangle((w * .06, base_y - h * .02, w * .94, h * .95), int(12 * k), fill=255)
    metal = Image.merge("RGBA", (grad, grad, grad, mask)); im.alpha_composite(metal)
    d = ImageDraw.Draw(im)
    for i, x in enumerate(tips):
        y = top if i % 2 == 0 else top + h * .12; r = w * .035
        d.ellipse((w * x - r, y - r * 1.6, w * x + r, y + r * .4), fill=(225, 225, 225, 255))
    for j in range(5):
        cx = w * (.18 + j * .16); cy = h * .86; r = w * .03
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(60, 60, 60, 255), outline=(200, 200, 200, 255), width=int(2 * k))
    d.line((w * .06, base_y, w * .94, base_y), fill=(240, 240, 240, 255), width=int(3 * k))
    return im
CROWN = ss(crown_img, (420, 300))
CROWN_DOWN = CROWN.rotate(-78, expand=True, resample=Image.BICUBIC)

def stage_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0))
    cone = Image.new("L", size, 0); ImageDraw.Draw(cone).polygon([(w * .44, 0), (w * .56, 0), (w * .85, h * .82), (w * .15, h * .82)], fill=110)
    cone = cone.filter(ImageFilter.GaussianBlur(25 * k))
    im.alpha_composite(Image.merge("RGBA", (cone, cone, cone, cone)))
    fl = Image.new("L", size, 0); ImageDraw.Draw(fl).ellipse((w * .12, h * .74, w * .88, h * .9), fill=180)
    fl = fl.filter(ImageFilter.GaussianBlur(20 * k)); im.alpha_composite(Image.merge("RGBA", (fl, fl, fl, fl)))
    d = ImageDraw.Draw(im); rr = random.Random(5)
    for i in range(26):  # público en silueta
        x = rr.uniform(0, w); y = h * .93 + rr.uniform(-10, 25) * k; s = rr.uniform(22, 34) * k
        d.ellipse((x - s * .5, y - s * 1.6, x + s * .5, y - s * .6), fill=(8, 8, 8, 255)); d.rounded_rectangle((x - s, y - s * .7, x + s, y + s * 2), int(s * .6), fill=(8, 8, 8, 255))
    return im
STAGE = ss(stage_img, (700, 900))

def setup_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((w * .12, h * .1, w * .88, h * .52), int(14 * k), fill=(38, 38, 40, 255), outline=(120, 120, 125, 255), width=int(4 * k))  # monitor apagado
    d.polygon([(w * .2, h * .14), (w * .45, h * .14), (w * .25, h * .48), (w * .16, h * .48)], fill=(70, 70, 74, 255))  # reflejo
    d.rectangle((w * .47, h * .52, w * .53, h * .6), fill=(90, 90, 95, 255)); d.rectangle((w * .36, h * .6, w * .64, h * .62), fill=(90, 90, 95, 255))
    d.rectangle((w * .05, h * .62, w * .95, h * .65), fill=(120, 120, 125, 255))  # escritorio
    # silla vacía
    d.rounded_rectangle((w * .34, h * .55, w * .66, h * .86), int(30 * k), fill=(26, 26, 28, 255), outline=(110, 110, 115, 255), width=int(3 * k))
    d.rounded_rectangle((w * .3, h * .84, w * .7, h * .9), int(12 * k), fill=(60, 60, 64, 255))
    d.rectangle((w * .485, h * .9, w * .515, h * .97), fill=(70, 70, 74, 255)); d.line((w * .36, h * .99, w * .64, h * .99), fill=(90, 90, 95, 255), width=int(5 * k))
    return im
SETUP = ss(setup_img, (560, 620))

def phone_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(48 * k), fill=(30, 30, 32, 255), outline=(150, 150, 155, 255), width=int(5 * k))
    d.rounded_rectangle((w * .05, h * .03, w * .95, h * .97), int(38 * k), fill=(232, 232, 232, 255))
    d.rounded_rectangle((w * .38, h * .045, w * .62, h * .07), int(10 * k), fill=(30, 30, 32, 255))
    d.ellipse((w * .1, h * .14, w * .26, h * .14 + w * .16), fill=(110, 110, 110, 255))
    d.rounded_rectangle((w * .3, h * .15, w * .62, h * .17), int(5 * k), fill=(60, 60, 60, 255)); d.rounded_rectangle((w * .3, h * .185, w * .5, h * .2), int(5 * k), fill=(160, 160, 160, 255))
    f = SANS(800, int(120 * k)); d.text((w * .1, h * .32), "LFT", font=f, fill=(20, 20, 20, 255), anchor="lm")
    d.text((w * .1, h * .42), "21 oct 2026", font=SANS(400, int(26 * k)), fill=(120, 120, 120, 255), anchor="lm")
    for i, yy in enumerate([.55, .6, .65]): d.rounded_rectangle((w * .1, h * yy, w * (.9 - i * .15), h * yy + 10 * k), int(5 * k), fill=(200, 200, 200, 255))
    return im
PHONE = ss(phone_img, (330, 640))

def trophy_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0))
    grad = Image.new("L", size); gd = ImageDraw.Draw(grad)
    for x in range(w): gd.line((x, 0, x, h), fill=int(90 + 140 * (0.5 + 0.5 * math.cos((x / w) * 6.0 - .6))))
    m = Image.new("L", size, 0); md = ImageDraw.Draw(m)
    md.polygon([(w * .18, h * .05), (w * .82, h * .05), (w * .7, h * .42), (w * .56, h * .52), (w * .44, h * .52), (w * .3, h * .42)], fill=255)
    md.rectangle((w * .45, h * .5, w * .55, h * .72), fill=255); md.polygon([(w * .3, h * .72), (w * .7, h * .72), (w * .78, h * .82), (w * .22, h * .82)], fill=255)
    md.rectangle((w * .16, h * .82, w * .84, h * .96), fill=255)
    for side in (-1, 1):
        cx = w * (.5 + side * .36); md.arc((cx - w * .14, h * .08, cx + w * .14, h * .36), 0, 360, fill=255, width=int(10 * k))
    im.alpha_composite(Image.merge("RGBA", (grad, grad, grad, m))); return im
TROPHY = ss(trophy_img, (300, 420))

def player_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(18 * k), fill=(34, 34, 36, 255), outline=(130, 130, 135, 255), width=int(3 * k))
    d.ellipse((w * .3, h * .16, w * .7, h * .16 + w * .4), fill=(150, 150, 155, 255))
    d.pieslice((w * .1, h * .52, w * .9, h * 1.15), 180, 360, fill=(150, 150, 155, 255))
    return im
PLAYER = ss(player_img, (170, 230))

def stadium_img(size, k):
    w, h = size; im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for row in range(5):
        y = h * (.55 + row * .08); n = 14 + row * 3
        for i in range(n):
            x = w * (i + .5) / n; d.ellipse((x - 3 * k, y - 3 * k, x + 3 * k, y + 3 * k), fill=(200, 200, 200, 200))
    beams = Image.new("L", size, 0); bd = ImageDraw.Draw(beams)
    for i, x in enumerate([.15, .35, .65, .85]):
        bd.polygon([(w * x - 8 * k, h), (w * x + 8 * k, h), (w * (x + (i - 1.5) * .18) + 60 * k, 0), (w * (x + (i - 1.5) * .18) - 60 * k, 0)], fill=60)
    beams = beams.filter(ImageFilter.GaussianBlur(14 * k)); im.alpha_composite(Image.merge("RGBA", (beams, beams, beams, beams)))
    d = ImageDraw.Draw(im); d.rectangle((w * .25, h * .38, w * .75, h * .5), outline=(220, 220, 220, 255), width=int(3 * k))
    return im
STADIUM = ss(stadium_img, (720, 900))

def glow_red(im, radius=40, strength=1.0):
    pad = radius * 3; big = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0); big.paste(im.getchannel("A"), (pad, pad))
    a = big.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: min(255, int(v * 1.8 * strength)))
    out = Image.new("RGBA", big.size, RED + (0,)); out.putalpha(a); out.alpha_composite(im, (pad, pad))
    return out
CROWN_G = glow_red(CROWN, 45, .9); CROWN_DOWN_G = glow_red(CROWN_DOWN, 40, .5)

# ---------------- clips opcionales ----------------
_clips = {}
def clip_frame(name, t, fps=30):
    p = os.path.join(TZ, "clips", name)
    if not os.path.exists(p): return None
    if name not in _clips:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-t", "8", "-vf", f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        _clips[name] = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
    fr = _clips[name]; g = fr[min(len(fr) - 1, int(t * fps))]
    g = (g.astype(np.float32) * .8).astype(np.uint8)
    return Image.fromarray(np.dstack([g, g, g, np.full_like(g, 255)]), "RGBA")

# ---------------- texto letra por letra ----------------
def letters(dst, word, font, cx, y, t, t0, per=.035, dur=.22, fill=WHITE, blur=True):
    total = font.getlength(word); x0 = cx - total / 2
    for i, ch in enumerate(word):
        p = prog(t, t0 + i * per, t0 + i * per + dur)
        if p <= 0 or ch == " ": continue
        lx = x0 + font.getlength(word[:i]); l = text_layer(ch, font, fill)
        if blur and p < 1: l = l.filter(ImageFilter.GaussianBlur(5 * (1 - p)))
        paste(dst, l, lx - 2, y + 10 * (1 - eo(p)), eo(p), "lm")

def small(dst, s, t, t0, y, fill=(210, 210, 210)):
    p = eo(prog(t, t0, t0 + .3))
    if p > 0: paste(dst, text_layer(s, SERIF(400, 34, True), fill), 360, y + 8 * (1 - p), p)

def fit_font(word, maxw, start=96):
    s = start
    while SANS(800, s).getlength(word) > maxw and s > 30: s -= 4
    return SANS(800, s)

# ---------------- escenas ----------------
def base(t, gword, zoom=0.0):
    im = BG.copy(); g = ghost(gword, t)
    paste(im, g, 360 + math.sin(t * .4) * 20, 470)
    paste(im, STARS, 40, 60, .9, "lt")
    return im

def frame_scene(T):
    """Devuelve (imagen, tiempo de inicio de escena)."""
    if T < 3.3:
        t = T; im = base(t, "CAÍDA")
        paste(im, CROWN_DOWN_G, 360 + 20, 930 + 6 * math.sin(t * 2), eo(prog(t, .1, .9)))
        small(im, "después de la caída", t, .3, 470); letters(im, "DOS CAMINOS", fit_font("DOS CAMINOS", 600), 360, 560, t, .9)
        return im, 0
    if T < 6.5:
        t = T - 3.3; im = base(t, "FUERTE")
        up = eo(prog(t, 1.2, 3.0))
        c = CROWN_DOWN_G.rotate(up * 60, expand=True, resample=Image.BICUBIC)
        paste(im, c, 380, lerp(930, 880, up)); small(im, "quedarte en el suelo…", t, .1, 440)
        small(im, "o volver", t, 1.2, 490); letters(im, "MÁS FUERTE", fit_font("MÁS FUERTE", 600), 360, 580, t, 1.6, fill=RED)
        return im, 3.3
    if T < 9.3:
        t = T - 6.5; im = base(t, "ADIÓS")
        st = STAGE.resize((int(700 * (1 + .03 * t)), int(900 * (1 + .03 * t)))); paste(im, st, 360, 1300, .95, "mb")
        small(im, "septiembre 2024", t, .1, 300); letters(im, "SE RETIRÓ", fit_font("SE RETIRÓ", 600), 360, 390, t, .35)
        small(im, "muchos pensaron:", t, 1.6, 470, GREY); letters(im, "NUNCA MÁS", SANS(800, 52), 360, 530, t, 1.9, fill=GREY)
        paste(im, SETUP, 360, 1240, eo(prog(t, 1.5, 2.2)) * .0, "mb")
        return im, 6.5
    if T < 12.0:
        t = T - 9.3; im = base(t, "LFT")
        paste(im, PHONE, 360 + 0 * t, lerp(1500, 930, eo(prog(t, 0, .5))), 1)
        small(im, "21 de octubre · solo tres letras", t, .2, 300)
        b = [x - 9.3 for x in BEATS if 9.9 < x < 12.0][:3] or [.8, 1.3, 1.8]
        for i, ch in enumerate("LFT"):
            p = eo(prog(t, b[i], b[i] + .12)) if i < len(b) else 0
            if p > 0:
                l = text_layer(ch, ANTON(170), RED if i == 2 else WHITE); s = lerp(1.6, 1, p)
                l = l.resize((int(l.width * s), int(l.height * s))); paste(im, l, 220 + i * 140, 470, p)
        return im, 9.3
    if T < 13.0:  # bajón: tensión
        t = T - 12.0; im = canvas(BLACK + (255,))
        r = int(lerp(40, 700, eo(t)));
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((360 - r, 640 - r, 360 + r, 640 + r), outline=RED + (255,), width=60)
        im.alpha_composite(ring.filter(ImageFilter.GaussianBlur(30))); small(im, "hasta que…", t, .1, 640, WHITE)
        return im, 12.0
    if T < 17.6:
        t = T - 13.0; im = base(t, "T1")
        sc = 1 + .05 * t; c = CROWN_G.resize((int(CROWN_G.width * sc), int(CROWN_G.height * sc)))
        paste(im, c, 360, 900 + 6 * math.sin(t * 3))
        small(im, "12 · noviembre · 2026", t, .05, 330); letters(im, "ES OFICIAL", fit_font("ES OFICIAL", 620), 360, 430, t, .15, per=.03)
        small(im, "T1 lo anuncia", t, 1.5, 520, GREY)
        return im, 13.0
    if T < 23.7:
        t = T - 17.6; cf = clip_frame("clip1.mp4", t)
        im = base(t, "KING")
        if cf is not None: im.alpha_composite(Image.blend(cf, BG, .25))
        else:
            sc = 1.2 + .06 * t; c = CROWN_G.resize((int(CROWN_G.width * sc), int(CROWN_G.height * sc))); paste(im, c, 360, 1000)
        small(im, "the KING is back", t, .05, 330); letters(im, "TENZ", ANTON(220), 360, 470, t, .3, per=.06, fill=RED)
        small(im, "vuelve a competir", t, 1.6, 600)
        return im, 17.6
    if T < 24.5:
        t = T - 23.7; im = canvas(BLACK + (255,)); small(im, "y no vuelve cualquiera", t, .05, 640, WHITE); return im, 23.7
    if T < 30.0:
        t = T - 24.5; im = base(t, "MASTERS")
        small(im, "2 veces campeón de Masters", t, .05, 300)
        paste(im, TROPHY, 220, lerp(1400, 1000, eo(prog(t, .2, .7))), 1); paste(im, TROPHY, 500, lerp(1400, 1000, eo(prog(t, 2.8, 3.3))), 1)
        letters(im, "REYKJAVÍK 2021", fit_font("REYKJAVÍK 2021", 620, 80), 360, 420, t, .3, per=.025)
        letters(im, "MADRID 2024", fit_font("MADRID 2024", 620, 80), 360, 520, t, 2.8, per=.03, fill=RED)
        return im, 24.5
    if T < 36.5:
        t = T - 30.0; im = base(t, "ROSTER"); small(im, "su nuevo equipo", t, .05, 220)
        names = ["CRASHIES", "STAX", "BUZZ", "IZU", "TENZ"]
        bt = [x - 30 for x in BEATS if 30.4 < x < 36.5][::2][:5] or [.5, 1.4, 2.3, 3.2, 4.4]
        for i, n in enumerate(names):
            p = eo(prog(t, bt[i], bt[i] + .2)) if i < len(bt) else 0
            if p <= 0: continue
            y = 330 + i * 150; last = n == "TENZ"
            paste(im, PLAYER.resize((110, 149)), lerp(-100, 130, p), y + 40, p)
            paste(im, text_layer(n, ANTON(110 if last else 84), RED if last else WHITE), lerp(900, 210, p), y + 40, p, "lm")
            if last: ImageDraw.Draw(im).rectangle((210, y + 105, lerp(210, 640, p), y + 111), fill=RED + (255,))
        return im, 30.0
    if T < 42.0:
        t = T - 36.5; im = base(t, "2027"); paste(im, STADIUM, 360, 1290, .9, "mb")
        small(im, "debut esperado", t, .05, 300); letters(im, "DICIEMBRE", fit_font("DICIEMBRE", 600), 360, 390, t, .25)
        small(im, "Red Bull Home Ground", t, .9, 470, GREY)
        small(im, "y en enero · VCT Pacific", t, 2.8, 560); letters(im, "ENERO 2027", fit_font("ENERO 2027", 600), 360, 650, t, 3.1, fill=RED)
        return im, 36.5
    if T < 50.5:
        t = T - 42.0; im = base(t, "VOLVER")
        paste(im, STAGE, 360, 1300, .8, "mb")
        up = eo(prog(t, 2.5, 7.5)); c = CROWN_DOWN_G.rotate(up * 78, expand=True, resample=Image.BICUBIC)
        paste(im, c, 360, lerp(960, 880, up), .9)
        small(im, "dos años después…", t, .3, 340); small(im, "eligió el segundo camino", t, 3.5, 420, GREY)
        if t > 5.4:
            r = int(lerp(20, 760, eo(prog(t, 5.4, 8.4))))
            ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((360 - r, 640 - r, 360 + r, 640 + r), outline=(200, 200, 200, 160), width=50)
            im.alpha_composite(ring.filter(ImageFilter.GaussianBlur(25)))
        return im, 42.0
    t = T - 51.0 if T >= 51.0 else 0
    cf = clip_frame("clip2.mp4", t) if T >= 51 else None
    im = base(t, "KING")
    if cf is not None and T < 56.5: im.alpha_composite(Image.blend(cf, BG, .25))
    sc = 1 + .03 * t; c = CROWN_G.resize((int(CROWN_G.width * sc), int(CROWN_G.height * sc))); paste(im, c, 360, 930, 1 if cf is None or T >= 56.5 else .5)
    small(im, "el", t, .1, 300); letters(im, "REY", ANTON(200), 360, 410, t, .2, per=.07, fill=RED)
    letters(im, "VOLVIÓ", fit_font("VOLVIÓ", 600, 110), 360, 560, t, .7, per=.05)
    for i, (s, x, y, a) in enumerate([(NAME, 60, 1150, "lm"), (USER, 660, 1150, "rm"), ("Fuente: anuncio oficial de T1 · 12 nov 2026", 360, 1210, "mm")]):
        p = prog(t, 2 + i * .3, 2.5 + i * .3)
        if p > 0: paste(im, text_layer(s, SANS(400, 16), (180, 180, 180)), x, y, p, a)
    return im, 51.0

CUTS = [3.3, 6.5, 9.3, 12.0, 13.0, 17.6, 23.7, 24.5, 30.0, 36.5, 42.0, 50.5, 51.0]
DROPS = [(13.0, 24.0), (25.0, 30.0), (51.0, 58.5)]

def chroma(img, amt):
    if amt < 1: return img
    r, g, b, a = img.split(); r = ImageChops.offset(r, int(amt), 0); b = ImageChops.offset(b, -int(amt), 0)
    return Image.merge("RGBA", (r, g, b, a))

def frame(T):
    img, t0 = frame_scene(T)
    # golpe de zoom en cada corte y pulso en cada beat de los drops
    dc = min([T - c for c in CUTS if T >= c] or [9])
    s = 1 + .07 * (1 - eo(clamp01(dc / .25)))
    if any(a <= T < b for a, b in DROPS):
        db = min([T - b for b in BEATS if T >= b] or [9]); s += .018 * max(0, 1 - db / .18)
    img = scale_about(img, s, bg=BLACK + (255,))
    if dc < .07: img = chroma(img, 14 * (1 - dc / .07))
    if dc < .05: img = Image.blend(img, canvas((255, 40, 30, 255) if T > 12 else (255, 255, 255, 255)), .55 * (1 - dc / .05))
    if 50.5 <= T < 51.0:  # flash grande antes del drop final
        p = prog(T, 50.5, 51.0); img = Image.blend(img, canvas((255, 255, 255, 255)), .9 * (1 - p)) if p > .3 else canvas((255, 255, 255, 255))
    img.alpha_composite(DUST[int(T * 12) % len(DUST)])
    paste(img, SPARK, 660, 1060, .8)
    img = add_grain(img, .22, T); img.alpha_composite(R.VIG)
    if T > 58.6: img = Image.blend(img, canvas((0, 0, 0, 255)), prog(T, 58.6, 59.9))
    return img.convert("RGB")

def clamp01(x): return max(0.0, min(1.0, x))

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((W // 2, H // 2)) for t in ts]
        sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for i, x in enumerate(ims): sh.paste(x, (i * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview"); sys.exit()
    out = a[0]; fps = int(a[a.index("--fps") + 1]) if "--fps" in a else 60
    audio = a[a.index("--audio") + 1] if "--audio" in a else None
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if audio: cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-af", "afade=t=out:st=58.3:d=1.7", "-c:a", "aac", "-b:a", "256k", "-t", "60"]
    cmd += ["-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * fps)
    for i in range(n):
        p.stdin.write(frame(i / fps).tobytes())
        if i % 600 == 0: print(f"{i}/{n}", flush=True)
    p.stdin.close(); p.wait(); print("OK", out)
