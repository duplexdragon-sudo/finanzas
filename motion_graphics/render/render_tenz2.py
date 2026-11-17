#!/usr/bin/env python3
"""EL REY VOLVIÓ v2: sincronizado con la voz (Grabación 54) + HEAVENLY JUMPSTYLE.
Tiempos de video = tiempos de la voz - VOFF. Objetos con iluminación metálica, foto CC de TenZ en gris.
Fotos de jugadores opcionales en ../tenz/fotos/{tenz,crashies,stax,buzz,izu}.jpg (se ponen en gris solas).
"""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import render_tenz as T
from render_tenz import (W, H, BG, RED, WHITE, GREY, BLACK, ANTON, STARS, SPARK, text_layer, paste, scale_about, add_grain,
                         DUST, prog, eo, lerp, SERIF, SANS, canvas, letters, small, fit_font, ghost, chroma, clamp01, R)

HERE = os.path.dirname(os.path.abspath(__file__)); TZ = os.path.join(HERE, "..", "tenz"); FOT = os.path.join(TZ, "fotos")
VOFF = 1.5; DUR = 62.0
NAME = "DUPLEXDRAGON"; USER = "@DuplexDragon_"

# ---------------- objetos de mejor calidad: relieve + luz metálica + sombra ----------------
def metalize(img, bump=7, spec=0.75, amb=0.5):
    a = np.asarray(img).astype(np.float32); al = a[..., 3] / 255
    lum = a[..., :3].mean(-1) / 255
    h = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(bump))).astype(np.float32) / 255
    h = h * 1.0 + lum * .25
    gy, gx = np.gradient(h)
    nx, ny, nz = -gx * 9, -gy * 9, np.ones_like(h); nl = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    L = np.array([-.5, -.6, .62]); L /= np.linalg.norm(L)
    d = np.clip((nx * L[0] + ny * L[1] + nz * L[2]) / nl, 0, 1)
    hv = np.array([0, 0, 1.0]) + L; hv /= np.linalg.norm(hv)
    s = np.clip((nx * hv[0] + ny * hv[1] + nz * hv[2]) / nl, 0, 1) ** 40
    v = lum * (amb + .75 * d) + spec * s
    v = np.clip(v, 0, 1) * 255
    out = np.dstack([v, v, v, a[..., 3]]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")

def with_shadow(img, dy=24, blur=18, op=.75):
    pad = blur * 3; out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad + dy), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 255)); sh.putalpha(img.getchannel("A").point(lambda v: int(v * op)))
    big = Image.new("RGBA", out.size, (0, 0, 0, 0)); big.alpha_composite(sh, (pad, pad + dy))
    out.alpha_composite(big.filter(ImageFilter.GaussianBlur(blur))); out.alpha_composite(img, (pad, pad)); return out

def reflection(img, op=.22, h=.35):
    r = ImageOps.flip(img).crop((0, 0, img.width, int(img.height * h)))
    m = Image.linear_gradient("L").resize(r.size).point(lambda v: int((255 - v) * op))
    r.putalpha(Image.fromarray(np.minimum(np.asarray(r.getchannel("A")), np.asarray(m)))); return r

_CU = os.path.join(TZ, "corona_recorte.png")
if os.path.exists(_CU):  # corona que mandó el usuario
    CROWN = Image.open(_CU).convert("RGBA")
    CROWN = CROWN.resize((420, int(CROWN.height * 420 / CROWN.width)), Image.LANCZOS)
else:
    CROWN = metalize(T.ss(T.crown_img, (420, 300), 3), bump=6, spec=.9)
CROWN_G = T.glow_red(with_shadow(CROWN), 45, .7)
CROWN_DOWN = CROWN.rotate(-78, expand=True, resample=Image.BICUBIC); CROWN_DOWN_G = T.glow_red(with_shadow(CROWN_DOWN), 40, .45)
TROPHY = with_shadow(metalize(T.ss(T.trophy_img, (300, 420), 3), bump=8, spec=.95))
PHONE = with_shadow(T.ss(T.phone_img, (330, 640), 3), 30, 24)
SETUP = with_shadow(metalize(T.ss(T.setup_img, (560, 620), 3), bump=4, spec=.5, amb=.7))
STAGE = T.ss(T.stage_img, (700, 900), 3); STADIUM = T.ss(T.stadium_img, (720, 900), 3)

# ---------------- fotos en gris ----------------
def gray_photo(path, size, focus=(.5, .4), zoom=1.0, contrast=1.25):
    im = Image.open(path).convert("L"); im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    r = max(size[0] / im.width, size[1] / im.height) * zoom
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    cx, cy = im.width * focus[0], im.height * focus[1]
    l = int(np.clip(cx - size[0] / 2, 0, im.width - size[0])); t = int(np.clip(cy - size[1] / 2, 0, im.height - size[1]))
    im = im.crop((l, t, l + size[0], t + size[1])).filter(ImageFilter.UnsharpMask(2, 80, 2))
    return Image.merge("RGBA", (im, im, im, Image.new("L", size, 255)))

def fade_mask(img, top=.25, bottom=.35):
    w, h = img.size; m = np.ones((h, w), np.float32); y = np.arange(h)[:, None] / h
    m *= np.clip(y / top, 0, 1) if top else 1; m *= np.clip((1 - y) / bottom, 0, 1) if bottom else 1
    x = np.arange(w)[None, :] / w; m *= np.clip(np.minimum(x, 1 - x) / .24, 0, 1) ** 1.5
    img.putalpha(Image.fromarray((m * 255).astype(np.uint8))); return img

TENZ_CC = os.path.join(FOT, "tenz_sen2023.jpg")
def hero_cutout():
    """TenZ recortado (máscara de segmentación) en gris, con el mismo encuadre que antes."""
    g = ImageEnhance.Brightness(gray_photo(TENZ_CC, (720, 980), focus=(.5, .38), zoom=1.05)).enhance(.9)
    mp_ = os.path.join(TZ, "tenz_mask.png")
    if not os.path.exists(mp_): return fade_mask(g, top=.16, bottom=.3)
    m = Image.open(mp_).convert("L"); im0 = Image.open(TENZ_CC)
    r = max(720 / im0.width, 980 / im0.height) * 1.05
    m = m.resize((int(im0.width * r) + 1, int(im0.height * r) + 1), Image.LANCZOS)
    cx, cy = m.width * .5, m.height * .38
    l = int(np.clip(cx - 360, 0, m.width - 720)); t = int(np.clip(cy - 490, 0, m.height - 980)); m = m.crop((l, t, l + 720, t + 980))
    y = np.arange(980)[:, None] / 980; x = np.arange(720)[None, :] / 720
    fade = np.clip((1 - y) / .22, 0, 1) * np.clip(np.minimum(x, 1 - x) / .2, 0, 1)
    a = (np.asarray(m).astype(np.float32) * fade).astype(np.uint8); g.putalpha(Image.fromarray(a)); return g
HERO = hero_cutout() if os.path.exists(TENZ_CC) else None
_W = os.path.join(TZ, "alas_recorte.png")
WINGS = Image.open(_W).convert("RGBA") if os.path.exists(_W) else None
if WINGS is not None:
    _a = np.asarray(WINGS.getchannel("A")); cols = np.where(_a.max(0) > 30)[0]
    gaps = [x for x in range(WINGS.width // 3, 2 * WINGS.width // 3) if _a[:, x].max() < 30]
    mid = int(np.mean(gaps)) if gaps else WINGS.width // 2
    WING_L = WINGS.crop((0, 0, mid, WINGS.height)); WING_R = WINGS.crop((mid, 0, WINGS.width, WINGS.height))
# foco (x,y) de la cara en cada foto que mandó el usuario (relativo a la imagen)
FOCUS = {"tenz": (.42, .33), "crashies": (.42, .33), "stax": (.6, .38), "buzz": (.55, .31), "izu": (.51, .3), "sacy": (.4, .29)}
def player_card(key, size=(150, 200)):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = os.path.join(FOT, f"{key}.{ext}")
        if os.path.exists(p):
            ph = gray_photo(p, size, FOCUS.get(key, (.5, .4)), zoom=1.7)
            m = Image.new("L", size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), 16, fill=255)
            ph.putalpha(m); ImageDraw.Draw(ph).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), 16, outline=(200, 200, 200, 255), width=2)
            return ph
    return metalize(T.PLAYER.resize(size, Image.LANCZOS), bump=3, spec=.4, amb=.8)
_TR = os.path.join(FOT, "trofeo.jpg")
TROPHY_PHOTO = fade_mask(ImageEnhance.Brightness(gray_photo(_TR, (560, 820), focus=(.5, .45), zoom=1.0, contrast=1.35)).enhance(.95), top=.12, bottom=.25) if os.path.exists(_TR) else None
_TW = os.path.join(FOT, "tweet_lft.png")
def tweet_card(path=None, w=640):
    path = path or _TW
    if not os.path.exists(path): return None
    im = Image.open(path).convert("L"); im = ImageEnhance.Contrast(im).enhance(1.1)
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    im = Image.merge("RGBA", (im, im, im, Image.new("L", im.size, 255)))
    pad = 26; card = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255, 0))
    m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, card.width - 1, card.height - 1), 28, fill=255)
    base = Image.new("RGBA", card.size, (255, 255, 255, 255)); base.alpha_composite(im, (pad, pad)); base.putalpha(m)
    ImageDraw.Draw(base).rounded_rectangle((0, 0, card.width - 1, card.height - 1), 28, outline=RED + (255,), width=4)
    return with_shadow(base, 22, 20, .8)
TWEET = tweet_card()
TWEET_BACK = tweet_card(os.path.join(FOT, "tweet_back.png"), 500)
def _obj(name, h):
    p = os.path.join(TZ, name)
    if not os.path.exists(p): return None
    im = Image.open(p).convert("RGBA"); g = ImageOps.grayscale(im.convert("RGB")); g = ImageEnhance.Contrast(g).enhance(1.15)
    a = im.getchannel("A").filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.5))   # sin borde blanco
    im = Image.merge("RGBA", (g, g, g, a))
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
MASK = _obj("ficha.png", 400); KING = _obj("rey_ajedrez.png", 640)
CARDS = {k: player_card(k) for k in ["crashies", "stax", "buzz", "izu", "tenz", "sacy"]}


# ---------------- corona animada ----------------
CROWN_S = with_shadow(CROWN, 20, 14, .6)
def _rays(t, r=380, n=14):
    im = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(n):
        a = math.radians(k * 360 / n + t * 18); w = math.radians(5)
        d.polygon([(r, r), (r + r * math.cos(a - w), r + r * math.sin(a - w)), (r + r * math.cos(a + w), r + r * math.sin(a + w))], fill=RED + (48,))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r, 2 * r), fill=255)
    m = Image.fromarray((np.asarray(m.filter(ImageFilter.GaussianBlur(r * .45))) * 1.0).astype(np.uint8))
    im.putalpha(Image.fromarray(np.minimum(np.asarray(im.getchannel("A")), np.asarray(m))))
    return im.filter(ImageFilter.GaussianBlur(9))
RAYS = [_rays(i / 10) for i in range(0, 200)]
def crown_anim(T_, t, lying=0.0, scale=1.0, glow=.75, rays=True, sway=1.0, rot0=0.0):
    """lying: 1 = tirada en el suelo, 0 = de pie. Flota, gira en 3D, brillo que barre y rebote en cada beat."""
    db = min([T_ - b for b in BEATS if T_ >= b] or [9]); bounce = .05 * max(0, 1 - db / .2) * (1 - lying) * sway
    c = CROWN_S
    ang = math.sin(t * 1.6) * 28 * (1 - .7 * lying) * sway
    c, _ = R.rotate_y(c, ang)
    # brillo que barre la corona cada 1.6 s
    ph = (t % 1.6) / 1.6
    if ph < .45:
        sw = Image.new("L", c.size, 0); x = lerp(-c.width * .4, c.width * 1.3, ph / .45)
        ImageDraw.Draw(sw).polygon([(x, 0), (x + 40, 0), (x - c.height * .5 + 40, c.height), (x - c.height * .5, c.height)], fill=110)
        sw = sw.filter(ImageFilter.GaussianBlur(10)); sw = Image.fromarray(np.minimum(np.asarray(sw), np.asarray(c.getchannel("A"))))
        hl = Image.new("RGBA", c.size, (255, 255, 255, 0)); hl.putalpha(sw); c = c.copy(); c.alpha_composite(hl)
    rot = -78 * lying + rot0 + (math.sin(t * 1.1) * 5 * (1 - lying) + math.sin(t * 3) * 2 * lying) * max(sway, .25)
    c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = scale * (1 + bounce); c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.BICUBIC)
    c = T.glow_red(c, 40, glow)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if rays and lying < .5:
        rr = RAYS[int(T_ * 10) % len(RAYS)]; rs = rr.resize((int(rr.width * scale), int(rr.height * scale))); paste(out, rs, 360, 0, 1 - lying * 2)
    return c, out

def put_crown(im, T_, t, x, y, lying=0.0, scale=1.0, a=1.0, glow=.75, sway=1.0, rot0=0.0, rays_on=True, sparks=True):
    c, rays = crown_anim(T_, t, lying, scale, glow, rays_on, sway, rot0)
    fy = y + (math.sin(t * 2.2) * 14 * (1 - lying) + math.sin(t * 1.3) * 4) * sway
    if lying < .5 and rays_on:
        rl = rays; tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); paste(tmp, rl.crop((0, 0, W, H)), 0, 0, 1, "lt")
        paste(im, RAYS[int(T_ * 10) % len(RAYS)].resize((int(760 * scale), int(760 * scale))), x, fy, a * (1 - lying * 2))
    paste(im, c, x, fy, a)
    # chispas que suben
    for k in range(14 if sparks else 0):
        ph = ((t * .45 + k / 14) % 1)
        sx = x + math.sin(k * 7.3 + t) * 150 * scale; sy = fy + 120 - ph * 420
        r = 2 + (k % 3)
        ImageDraw.Draw(im).ellipse((sx - r, sy - r, sx + r, sy + r), fill=(255, 120 + (k * 9) % 120, 90, int(220 * (1 - ph) * a * (1 - lying * .6))))

# ---------------- clips y logos opcionales (archivos que suba el usuario) ----------------
CLIPDIR = os.path.join(TZ, "clips"); LOGODIR = os.path.join(TZ, "logos")
_clips = {}
def clip(name, t, fps=60, dark=.75):
    for ext in ("mp4", "mov", "webm", "mkv"):
        p = os.path.join(CLIPDIR, f"{name}.{ext}")
        if os.path.exists(p): break
    else: return None
    if name not in _clips:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-t", "8", "-vf", f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        _clips[name] = np.frombuffer(raw, np.uint8).reshape(-1, H, W) if raw else None
    fr = _clips[name]
    if fr is None or not len(fr): return None
    g = fr[min(len(fr) - 1, int(max(0, t) * fps))].astype(np.float32)
    g = np.clip((g - 128) * 1.25 + 128, 0, 255) * dark
    g = g.astype(np.uint8); return Image.fromarray(np.dstack([g, g, g, np.full_like(g, 255)]), "RGBA")
def logo(name, h):
    for ext in ("png", "webp", "jpg"):
        p = os.path.join(LOGODIR, f"{name}.{ext}")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA"); bb = im.getchannel("A").getbbox()
            if bb: im = im.crop(bb)
            return im.resize((max(1, int(im.width * h / im.height)), h), Image.LANCZOS)
    return None
LOGO_T1 = logo("t1", 46); LOGO_T1_BIG = logo("t1", 150); LOGO_VCT = logo("vct", 60); LOGO_MASTERS = logo("masters", 110)

HEAD = (282, 150); HEAD_TILT = 18.0   # base de la corona sobre el pelo (coords de HERO) e inclinación de la cabeza
HEADC = 308
def head_crown_pos(z, cy, cscale):
    bx = 360 + (HEAD[0] - HEADC) * z; by = cy + (HEAD[1] - 490) * z
    d = (CROWN.height / 2 - 10) * cscale; th = math.radians(HEAD_TILT)
    return bx - d * math.sin(th), by - d * math.cos(th)
USE_WINGS = False   # alas desactivadas a pedido
def draw_wings(im, T_, z, cy, p):
    if not USE_WINGS or WINGS is None or p <= 0: return
    ws = 1.72 * z * (.4 + .6 * p)                            # tamaño: de encima de la cabeza hasta los hombros
    flap = math.sin(T_ * 2.4) * 6 * p                        # aleteo lento
    topy = cy + (430 - 490) * z                              # bisagra en la espalda (a la altura del cuello/hombros)
    cx = 360                                                 # centradas en la cabeza (simétricas)
    for side, wimg in ((-1, WING_L), (1, WING_R)):
        w = wimg.resize((max(1, int(wimg.width * ws)), max(1, int(wimg.height * ws))), Image.LANCZOS)
        px = w.width if side < 0 else 0; py = int(w.height * .06)       # bisagra: borde interior de arriba
        big = Image.new("RGBA", (w.width * 2, w.height * 2), (0, 0, 0, 0)); big.alpha_composite(w, (w.width - px, w.height - py))
        big = big.rotate(-side * (flap + (1 - p) * 40) + side * 24, resample=Image.BICUBIC)   # abiertas 24°
        paste(im, big, cx + side * 150 * z, topy + (1 - p) * 120, p * .97)

def hero(im, T_, scene, a=.9, red=0.0, dy=40, z=None, wings=0.0):
    """TenZ recortado en gris (cara que vende el video), alas rojas detrás. Devuelve (z, centro_y)."""
    if HERO is None: return None
    z = z or (1.0 - .05 * eo(clamp01(T_ / 8.5))); h = HERO.resize((int(720 * z), int(980 * z)), Image.LANCZOS)
    cy = 1280 - h.height / 2 + 60 + dy
    draw_wings(im, T_, z, cy, wings)
    hx0 = 360 + (360 - HEADC) * z                            # TenZ centrado en el cuadro
    rim = Image.new("RGBA", h.size, RED + (0,)); rim.putalpha(h.getchannel("A").filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * (.35 + .4 * red))))
    paste(im, rim, hx0, cy); paste(im, h, hx0, cy, a)
    global LAST_HERO; LAST_HERO = (h, hx0, cy, a); return z, cy
LAST_HERO = None
def head_over(im, k=1.0):
    """Vuelve a pegar a TenZ encima: la corona queda detrás de su cabeza."""
    if LAST_HERO is None or k <= 0: return
    h, x, y, a = LAST_HERO; paste(im, h, x, y, a * k)
def crown_on_head(im, T_, t, hz, p=1.0, start=(150, 1180), a=1.0):
    """Corona en la cabeza de TenZ. p<1: viene volando desde 'start' (tirada) hasta la cabeza."""
    if hz is None: return
    z, cy = hz; cs = .92 * z; hx, hy = head_crown_pos(z, cy, cs)
    if p >= 1:
        put_crown(im, T_, t, hx, hy, scale=cs, a=a, glow=.12, sway=0.0, rot0=HEAD_TILT, rays_on=False, sparks=False)
        head_over(im); return
    x = lerp(start[0], hx, p); y = lerp(start[1], hy, p) - math.sin(math.pi * p) * 260
    put_crown(im, T_, t, x, y, lying=1 - p, scale=lerp(.6, cs, p), a=a, glow=lerp(.45, .12, p), sway=1 - p, rot0=HEAD_TILT * p, rays_on=False)
    head_over(im, clamp01((p - .8) / .2))   # al aterrizar pasa detrás de la cabeza

def base(t, gword):
    im = BG.copy(); paste(im, ghost(gword, t), 360 + math.sin(t * .4) * 20, 470); paste(im, STARS, 40, 60, .9, "lt"); return im

def grown(im, obj, x, y, t, rate=.03, a=1.0):
    s = 1 + rate * t; o = obj.resize((int(obj.width * s), int(obj.height * s)), Image.BICUBIC); paste(im, o, x, y, a)

# ---------------- línea de tiempo (segundos de video) ----------------
v = lambda raw: raw - VOFF
CUTS = [0, v(6.36), v(10.06), v(15.86), v(18.2), v(25.46), v(31.64), v(36.92), v(43.8), v(50.98), v(57.72), v(60.58)]
WORDS = dict(caminos=v(5.20), volver=v(7.84), fuerte=v(8.70), grandes=v(11.88), adios=v(14.32), jamas=v(17.2), octubre=v(18.2),
             letras=v(20.2), L=v(22.12), F=v(22.82), Tt=v(23.56), equipo=v(24.12), nov=v(25.46), t1=v(28.34), oficial=v(29.16),
             king=v(30.2), tyson=v(31.64), tenz=v(32.54), ngo=v(34.32), compite=v(35.48), cualq=v(36.92), campeon=v(38.76),
             reyk=v(40.4), y2021=v(41.70), madrid=v(42.88), equipo2=v(44.3), crashies=v(46.34), stax=v(47.34), buzz=v(48.36),
             izu=v(49.12), tenz2=v(50.02), debut=v(50.98), rbhg=v(52.40), dic=v(54.14), enero=v(55.12), pacific=v(56.2),
             anos=v(57.72), camino=v(58.92), rey=v(60.58), volvio=v(61.28))
Wd = WORDS

def frame_scene(T_):
    c = CUTS
    if T_ < c[1]:  # Después de la caída… dos caminos
        t = T_; im = base(t, "CAÍDA"); hero(im, T_, 0, .9)
        small(im, "después de la caída", t, .3, 120); small(im, "solo hay", t, v(3.72), 175, GREY)
        letters(im, "DOS CAMINOS", fit_font("DOS CAMINOS", 600), 360, 250, t, Wd["caminos"] - .1)
        return im
    if T_ < c[2]:  # quedarte en el suelo… o volver MÁS FUERTE → la corona vuela a su cabeza
        t = T_ - c[1]; im = base(t, "FUERTE"); hz = hero(im, T_, 1, .95, red=eo(prog(T_, Wd["fuerte"], Wd["fuerte"] + .5)), wings=eo(prog(T_, Wd["fuerte"] + .2, Wd["fuerte"] + 1.0)))
        drop = eo(prog(T_, Wd["fuerte"] - .1, Wd["fuerte"] + .4))
        if drop > 0 and hz is not None: crown_on_head(im, T_, T_, (hz[0], hz[1] - (1 - drop) * 700), a=drop)
        small(im, "quedarte en el suelo…", t, .05, 120); small(im, "o volver", T_, Wd["volver"], 175)
        letters(im, "MÁS FUERTE", fit_font("MÁS FUERTE", 600), 360, 250, T_, Wd["fuerte"], fill=RED)
        return im
    if T_ < c[3]:  # Septiembre 2024… dijo adiós
        t = T_ - c[2]; im = base(t, "ADIÓS"); grown(im, STAGE, 360, 1290 - 450, t, .02, .95)
        # TenZ bajo el foco; en "dijo adiós" se desvanece hacia arriba y deja el escenario vacío
        gone = eo(prog(T_, Wd["adios"], Wd["adios"] + 1.3))
        if gone < 1:
            tmp = canvas(); hero(tmp, T_, 2, 1.0, red=.25, z=.84 + .02 * t, dy=70 - 60 * gone)
            if gone > 0: tmp = tmp.filter(ImageFilter.GaussianBlur(6 * gone))
            paste(im, tmp, 360, 640, .9 * (1 - gone))
        small(im, "septiembre 2024", t, .05, 300); small(im, "uno de los más grandes de Valorant", T_, Wd["grandes"], 360, GREY)
        letters(im, "DIJO ADIÓS", fit_font("DIJO ADIÓS", 600), 360, 460, T_, Wd["adios"])
        return im
    if T_ < c[4]:  # muchos pensaron… jamás
        t = T_ - c[3]; im = base(t, "NUNCA")
        if MASK is not None:   # máscara que flota y se acerca en "jamás"
            pj = eo(prog(T_, Wd["jamas"] - .2, Wd["jamas"] + .3)); s_ = (.9 + .05 * t) * (1 + .12 * pj)
            m = MASK.resize((int(MASK.width * s_), int(MASK.height * s_)), Image.LANCZOS).rotate(math.sin(t * 1.4) * 6, expand=True, resample=Image.BICUBIC)
            paste(im, T.glow_red(m, 40, .35 + .5 * pj), 360, 930 + math.sin(t * 2) * 10, eo(prog(t, 0, .4)))
        else: grown(im, SETUP, 360, 940, t, .025)
        small(im, "muchos pensaron que no volvería", t, .05, 330); letters(im, "JAMÁS", ANTON(170), 360, 450, T_, Wd["jamas"] - .2, per=.05, fill=GREY)
        return im
    if T_ < c[5]:  # 21 de octubre… L F T… buscando equipo
        t = T_ - c[4]; im = base(t, "LFT")
        if TWEET is not None:
            p = eo(prog(t, 0, .5)); s_ = lerp(.85, 1.0, p) + .02 * math.sin(t * 2)
            tw = TWEET.resize((int(TWEET.width * s_), int(TWEET.height * s_)), Image.LANCZOS); paste(im, tw, 360, lerp(1300, 860, p), p)
        else: paste(im, PHONE, 360, lerp(1500, 960, eo(prog(t, 0, .6))), 1)
        small(im, "hasta que el 21 de octubre", t, .05, 260); small(im, "publicó solo tres letras", T_, Wd["letras"], 320, GREY)
        for i, (ch, k) in enumerate(zip("LFT", ["L", "F", "Tt"])):
            p = eo(prog(T_, Wd[k], Wd[k] + .12))
            if p > 0:
                l = text_layer(ch, ANTON(170), RED if i == 2 else WHITE); s = lerp(1.7, 1, p)
                paste(im, l.resize((int(l.width * s), int(l.height * s))), 220 + i * 140, 470, p)
        small(im, "looking for team · buscando equipo", T_, Wd["equipo"], 590)
        return im
    if T_ < c[6]:  # 12 nov 2026 · T1 lo hace oficial · the KING is back
        t = T_ - c[5]; im = base(t, "T1")
        if TWEET_BACK is not None:
            p = eo(prog(T_, Wd["oficial"] - .2, Wd["oficial"] + .4)); s_ = lerp(.88, 1.0, p)
            tw = TWEET_BACK.resize((int(TWEET_BACK.width * s_), int(TWEET_BACK.height * s_)), Image.LANCZOS)
            paste(im, tw, 360, lerp(1500, 1075, p) - 40 * clamp01((T_ - Wd["oficial"]) / 3), p)
        else: put_crown(im, T_, t, 360, 900, scale=1.0 + .05 * t)
        small(im, "12 · noviembre · 2026", t, .05, 280)
        if LOGO_T1_BIG is not None:
            p = eo(prog(T_, Wd["t1"], Wd["t1"] + .25))
            if p > 0: lg = LOGO_T1_BIG.resize((int(LOGO_T1_BIG.width * lerp(1.5, 1, p)), int(LOGO_T1_BIG.height * lerp(1.5, 1, p)))); paste(im, lg, 360, 415, p)
        else: letters(im, "T1", ANTON(200), 360, 400, T_, Wd["t1"], per=.08, fill=RED)
        letters(im, "LO HACE OFICIAL", fit_font("LO HACE OFICIAL", 620, 70), 360, 520, T_, Wd["oficial"], per=.025)
        small(im, "the KING is back", T_, Wd["king"], 600, GREY)
        return im
    if T_ < c[7]:  # Tyson TenZ Ngo vuelve a competir (foto)
        t = T_ - c[6]; im = BG.copy()
        cf = clip("clip_tenz", t)
        if cf is not None: im.alpha_composite(cf); hz = None
        else: hz = hero(im, T_, 6, 1.0, z=.95 - .03 * eo(prog(t, 0, 4)), wings=1.0)
        crown_on_head(im, T_, t, hz)
        paste(im, ghost("TENZ", t), 360, 300); paste(im, STARS, 40, 60, .9, "lt")
        small(im, "Tyson", T_, Wd["tyson"], 110); letters(im, "TENZ", ANTON(200), 360, 215, T_, Wd["tenz"], per=.06, fill=RED)
        small(im, "Ngo", T_, Wd["ngo"], 330); small(im, "vuelve a competir", T_, Wd["compite"], 1200, WHITE)
        return im
    if T_ < c[8]:  # no vuelve con cualquiera · 2 veces campeón · Reykjavík 2021 · Madrid 2024
        t = T_ - c[7]; im = base(t, "MASTERS"); cf = clip("clip_masters", t, dark=.45)
        if cf is not None: im.alpha_composite(Image.blend(cf, BG, .3))
        small(im, "y no vuelve con cualquiera", t, .05, 250); small(im, "dos veces campeón de Masters", T_, Wd["campeon"], 310, GREY)
        if TROPHY_PHOTO is not None:
            p = eo(prog(T_, Wd["campeon"] - .1, Wd["campeon"] + .6)); zz = 1.04 + .03 * (T_ - c[7])
            tp = TROPHY_PHOTO.resize((int(560 * zz), int(820 * zz)), Image.LANCZOS); paste(im, tp, 360, lerp(1380, 1010, p), p)
        else:
            paste(im, TROPHY, 220, lerp(1500, 990, eo(prog(T_, Wd["reyk"] - .2, Wd["reyk"] + .4))))
            paste(im, TROPHY, 500, lerp(1500, 990, eo(prog(T_, Wd["madrid"] - .2, Wd["madrid"] + .4))))
        if LOGO_MASTERS is not None: paste(im, LOGO_MASTERS, 360, 640, eo(prog(T_, Wd["campeon"], Wd["campeon"] + .4)))
        letters(im, "REYKJAVÍK 2021", fit_font("REYKJAVÍK 2021", 620, 80), 360, 420, T_, Wd["reyk"], per=.025)
        letters(im, "MADRID 2024", fit_font("MADRID 2024", 620, 80), 360, 530, T_, Wd["madrid"], per=.03, fill=RED)
        return im
    if T_ < c[9]:  # su nuevo equipo
        t = T_ - c[8]; im = base(t, "ROSTER"); small(im, "y su nuevo equipo", t, .05, 200)
        for i, (k, n) in enumerate([("crashies", "CRASHIES"), ("stax", "STAX"), ("buzz", "BUZZ"), ("izu", "IZU"), ("tenz", "TENZ")]):
            key = {"tenz": "tenz2"}.get(k, k); p = eo(prog(T_, Wd[key], Wd[key] + .22))
            if p <= 0: continue
            y = 330 + i * 165; last = k == "tenz"
            paste(im, CARDS[k].resize((120, 160)), lerp(-100, 125, p), y + 40, p)
            paste(im, text_layer(n, ANTON(112 if last else 86), RED if last else WHITE), lerp(900, 210, p), y + 40, p, "lm")
            if last: ImageDraw.Draw(im).rectangle((210, y + 108, lerp(210, 640, p), y + 114), fill=RED + (255,))
        p = eo(prog(T_, c[8] + .4, c[8] + .8))   # Sacy: entrenador (reportado)
        if p > 0:
            y = 330 + 5 * 165
            paste(im, CARDS["sacy"].resize((96, 128)), lerp(-100, 125, p), y + 30, p)
            paste(im, text_layer("SACY", ANTON(66), (200, 200, 200)), lerp(900, 200, p), y + 12, p, "lm")
            paste(im, text_layer("coach (reportado)", SERIF(400, 26, True), GREY), lerp(900, 200, p), y + 62, p, "lm")
        return im
    if T_ < c[10]:  # debut esperado
        t = T_ - c[9]; im = base(t, "2027")
        if KING is not None:   # rey de ajedrez que sube y se queda en el centro
            p = eo(prog(t, 0, .7)); s_ = .95 + .03 * t
            k = KING.resize((int(KING.width * s_), int(KING.height * s_)), Image.LANCZOS)
            paste(im, T.glow_red(k, 40, .45), 360, lerp(1700, 1020, p), p)
        small(im, "su debut esperado", t, .05, 260)
        letters(im, "RED BULL HOME GROUND", fit_font("RED BULL HOME GROUND", 640, 60), 360, 350, T_, Wd["rbhg"], per=.018)
        letters(im, "DICIEMBRE", fit_font("DICIEMBRE", 600), 360, 440, T_, Wd["dic"])
        small(im, "y en enero", T_, Wd["enero"], 540, GREY)
        letters(im, "VCT PACIFIC", fit_font("VCT PACIFIC", 600, 84), 360, 625, T_, Wd["pacific"], fill=RED)
        if LOGO_VCT is not None: paste(im, LOGO_VCT, 360, 720, eo(prog(T_, Wd["pacific"] + .3, Wd["pacific"] + .6)))
        return im
    if T_ < c[11]:  # dos años después… eligió el segundo camino
        t = T_ - c[10]; im = base(t, "VOLVER"); cf = clip("clip_camino", t, dark=.5)
        if cf is not None: im.alpha_composite(Image.blend(cf, BG, .25))
        else: paste(im, STAGE, 360, 1290 - 450, .8)
        up = eo(prog(T_, Wd["camino"] - .3, Wd["camino"] + 1.0)); put_crown(im, T_, T_, 360, lerp(960, 880, up), lying=1 - up, glow=lerp(.45, .8, up))
        small(im, "dos años después…", t, .05, 330); small(im, "eligió el segundo camino", T_, Wd["camino"], 400, WHITE)
        return im
    t = T_ - c[11]; im = base(t, "KING")
    cf = clip("clip_final", t, dark=.5)
    if cf is not None: im.alpha_composite(cf); hz = None
    else: hz = hero(im, T_, 11, 1.0, red=.8, z=.93 + .02 * t, wings=eo(prog(T_, Wd["rey"] - .3, Wd["rey"] + .4)))
    if hz is not None:
        drop = eo(prog(T_, Wd["rey"] - .15, Wd["rey"] + .35)); z_, cy_ = hz; hx, hy = head_crown_pos(z_, cy_, .85 * z_)
        crown_on_head(im, T_, t, (z_, cy_ - (1 - drop) * 700), a=drop)
    else: put_crown(im, T_, t, 360, 900, scale=1.05 + .03 * t, glow=.9)
    small(im, "el", t, .02, 90); letters(im, "REY", ANTON(170), 360, 185, T_, Wd["rey"], per=.07, fill=RED)
    letters(im, "VOLVIÓ", fit_font("VOLVIÓ", 600, 96), 360, 315, T_, Wd["volvio"], per=.05)
    cred = [(NAME, 60, 1130, "lm", 15), (USER, 660, 1130, "rm", 15), ("Fuente: anuncio oficial de T1 · 12 nov 2026", 360, 1180, "mm", 14),
            ("Foto TenZ: Billgatenguyen, CC BY 4.0, editada a B/N · Clips: créditos a sus autores", 360, 1205, "mm", 12)]
    for i, (s, x, y, a, sz) in enumerate(cred):
        p = prog(t, .8 + i * .2, 1.2 + i * .2)
        if p > 0: paste(im, text_layer(s, SANS(400, sz), (175, 175, 175)), x, y, p, a)
    return im

DROPS = [(v(25.46), v(36.9)), (v(50.98), 60.5)]
BEATS = T.BEATS + (-1.04)  # canción adelantada 1.04 s (su caída/regreso en 24-25 s cae en "12 de noviembre")

def frame(T_):
    img = frame_scene(T_)
    dc = min([T_ - x for x in CUTS[1:] if T_ >= x] or [9])
    s = 1 + .07 * (1 - eo(clamp01(dc / .25)))
    if any(a <= T_ < b for a, b in DROPS):
        db = min([T_ - b for b in BEATS if T_ >= b] or [9]); s += .016 * max(0, 1 - db / .18)
    img = scale_about(img, s, bg=BLACK + (255,))
    if dc < .07: img = chroma(img, 14 * (1 - dc / .07))
    if dc < .05: img = Image.blend(img, canvas((255, 40, 30, 255)), .5 * (1 - dc / .05))
    if CUTS[5] <= T_ < CUTS[5] + .12 or CUTS[11] <= T_ < CUTS[11] + .12:  # flashes blancos en los momentos clave
        img = Image.blend(img, canvas((255, 255, 255, 255)), .85 * (1 - prog(T_, CUTS[5] if T_ < 50 else CUTS[11], (CUTS[5] if T_ < 50 else CUTS[11]) + .12)))
    img.alpha_composite(DUST[int(T_ * 12) % len(DUST)]); paste(img, SPARK, 660, 1060, .8)
    if LOGO_T1 is not None and T_ >= Wd["t1"]: paste(img, LOGO_T1, 670, 75, .9 * eo(prog(T_, Wd["t1"], Wd["t1"] + .4)), "rm")
    img = add_grain(img, .2, T_); img.alpha_composite(R.VIG)
    if T_ > 61.0: img = Image.blend(img, canvas((0, 0, 0, 255)), prog(T_, 61.0, 61.95))
    return img.convert("RGB")

def build_audio(voice, song, out):
    # voz desde 1.5 s; canción desde 1.04 s, bajo la voz con sidechain; fade final
    f = (f"[0:a]atrim=start={VOFF},asetpts=PTS-STARTPTS,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
         f"loudnorm=I=-16:TP=-1.5,aresample=48000,apad=whole_dur={DUR},asplit=2[v][vk];"
         f"[1:a]atrim=start=1.04,asetpts=PTS-STARTPTS,volume=0.55,aresample=48000[m];"
         f"[m][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
         f"[v][md]amix=inputs=2:normalize=0:duration=longest,atrim=0:{DUR},afade=t=out:st={DUR-1.8}:d=1.8,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", song, "-filter_complex", f, "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--portada" in a:
        im = BG.copy(); hz = hero(im, 8.0, 0, 1.0, red=1.0, z=.95, wings=1.0); paste(im, STARS, 40, 60, .9, "lt")
        crown_on_head(im, 30.0, 3.0, hz)
        small(im, "dos años después…", 9, 0, 80, WHITE)
        paste(im, text_layer("EL REY", ANTON(150), RED), 360, 180); paste(im, text_layer("VOLVIÓ", fit_font("VOLVIÓ", 600, 92), WHITE), 360, 300)
        im = add_grain(im, .15, 1); im.alpha_composite(R.VIG); im.convert("RGB").resize((1080, 1920), Image.LANCZOS).save(os.path.join(HERE, "portada_tenz.jpg"), quality=95)
        print("portada"); sys.exit()
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((W // 2, H // 2)) for t in ts]; sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for i, x in enumerate(ims): sh.paste(x, (i * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview"); sys.exit()
    out = a[0]; fps = int(a[a.index("--fps") + 1]) if "--fps" in a else 60
    voice = a[a.index("--voz") + 1]; song = a[a.index("--cancion") + 1]
    mix = os.path.join(TZ, "mezcla.wav"); build_audio(voice, song, mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * fps)
    for i in range(n):
        p.stdin.write(frame(i / fps).tobytes())
        if i % 600 == 0: print(f"{i}/{n}", flush=True)
    p.stdin.close(); p.wait(); print("OK", out)
