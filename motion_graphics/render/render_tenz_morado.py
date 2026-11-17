#!/usr/bin/env python3
"""EL REY VOLVIÓ — versión morada editorial (estética/ritmo del video de Motion Design) con la voz y timings del video de TenZ.
Uso: python3 render_tenz_morado.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import render_motion as M
from render_motion import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, word, pop, shadow, grid, BURST, clamp01, CURSOR, orbits)
from render import text_layer, paste, prog, eo, lerp, SANS, canvas, scale_about
import render_tenz2 as T2
_word = word
def word(dst, s_, f, x, y, *a, **k): return _word(dst, s_, f, x, y + (70 if y < 700 else 0), *a, **k)

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, "..")
OBJ = os.path.join(S, "motion", "objetos"); TZ = os.path.join(S, "tenz"); FOT = os.path.join(TZ, "fotos"); X = os.path.join(S, "tz2")
FPS = 30; DUR = 62.0; C = T2.CUTS; Wd = T2.Wd

# ---------------- duotono morado ----------------
STOPS = [(0, (40, 22, 56)), (.45, (137, 83, 171)), (.68, (176, 120, 240)), (1, (244, 238, 252))]
def _lut(ch):
    out = []
    for v in range(256):
        x = v / 255
        for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
            if a <= x <= b: f = (x - a) / (b - a); out.append(int(ca[ch] + (cb[ch] - ca[ch]) * f)); break
    return out
LUT = [_lut(i) for i in range(3)]
def duo(img, contrast=1.15):
    a = img.getchannel("A") if img.mode == "RGBA" else None
    g = ImageEnhance.Contrast(ImageOps.autocontrast(img.convert("L"), cutoff=1)).enhance(contrast)
    out = Image.merge("RGB", [g.point(LUT[i]) for i in range(3)]).convert("RGBA")
    if a is not None: out.putalpha(a)
    return out
def tint(img, col):
    o = Image.new("RGBA", img.size, col + (255,)); o.putalpha(img.getchannel("A")); return o

def obj(name, h=None, w=None):
    im = Image.open(os.path.join(OBJ, name + ".png")).convert("RGBA")
    s = h / im.height if h else w / im.width
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)

def fade_bottom(im, frac=.25):
    a = np.asarray(im.getchannel("A")).astype(np.float32); h = a.shape[0]; y = np.arange(h)[:, None] / h
    a *= np.clip((1 - y) / frac, 0, 1); im = im.copy(); im.putalpha(Image.fromarray(a.astype(np.uint8))); return im

# ---------------- recursos ----------------
def tenz_cc():
    im = Image.open(os.path.join(FOT, "tenz_sen2023.jpg")).convert("RGB"); m = Image.open(os.path.join(TZ, "tenz_mask.png")).convert("L")
    o = im.convert("RGBA"); o.putalpha(m); o = o.crop(m.point(lambda v: 255 if v > 30 else 0).getbbox())
    o = duo(o); o = fade_bottom(o, .22); return o.resize((560, int(o.height * 560 / o.width)), Image.LANCZOS)
TZ_CC = tenz_cc()
TZ_T1 = fade_bottom(duo(Image.open(os.path.join(X, "tenz_t1.png")).convert("RGBA")), .25)
TZ_T1 = TZ_T1.resize((600, int(TZ_T1.height * 600 / TZ_T1.width)), Image.LANCZOS)
def head_top(im):
    a = np.asarray(im.getchannel("A")) > 120; rows = np.where(a.any(1))[0]; y = rows.min()
    xs = np.where(a[y + 25])[0]; return (xs.min() + xs.max()) / 2, y
HT_CC = head_top(TZ_CC); HT_T1 = head_top(TZ_T1)

CROWN = obj("18_corona_espinas", w=270); CHAIN = obj("31_cadena_rota", w=700); HOUR = obj("19_reloj_arena", 470); MON = obj("28_monitor", 430)
KING = obj("17_rey_ajedrez", 640); COL = obj("25_columna", 640); MEDAL = obj("29_medalla", 330); DIAM = obj("24_diamante", 160)
WINGS = obj("35_alas", 480); COMPASS = obj("32_brujula", 330); EYE = obj("20_ojo", 230); BOLT = obj("30_rayo", 300)
SCOPE = obj("43_mira", w=520); HEADSET = obj("27_audifonos", 300)
VLOGO = Image.open(os.path.join(X, "valorant_logo.png")).convert("RGBA")
T1 = Image.open(os.path.join(TZ, "logos", "t1.png")).convert("RGBA")
T1_W = tint(T1.resize((300, int(T1.height * 300 / T1.width)), Image.LANCZOS), WHITE)
T1_SMALL_P = tint(T1.resize((70, int(T1.height * 70 / T1.width)), Image.LANCZOS), PUR)
T1_SMALL_W = tint(T1.resize((70, int(T1.height * 70 / T1.width)), Image.LANCZOS), WHITE)
HAB = {}
for f in sorted(os.listdir(os.path.join(X, "hab"))):
    im = Image.open(os.path.join(X, "hab", f)).convert("RGBA"); im = im.resize((70, 70), Image.LANCZOS); HAB[f[:-4]] = im
JETT = [HAB[k] for k in sorted(HAB) if k.startswith("jett")][:4]
MIX = [HAB[k] for k in ("jett_2", "chamber_3", "yoru_2", "raze_3", "neon_3", "omen_3") if k in HAB]


ORB = [HAB[k] for k in ("jett_0", "jett_1", "jett_2", "jett_3", "chamber_3", "yoru_3", "raze_3", "neon_3") if k in HAB]
def tenz_orbit(im, T, t, x, ybottom, w, t_orb, crown_t0=None, a=1.0, icons=None):
    """Foto de TenZ con las habilidades girando a su alrededor como un anillo 3D."""
    icons = icons or ORB; ph = TZ_T1.resize((w, int(TZ_T1.height * w / TZ_T1.width)), Image.LANCZOS)
    s = 1 + .015 * t; p2 = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)
    cy_ph = ybottom - p2.height / 2; hx = x - p2.width / 2 + HT_T1[0] * w / TZ_T1.width * s
    ox, oy = hx, cy_ph - p2.height * .08; R = p2.width * .62; ap = clamp01(t_orb * 2.5)
    pts = []
    for k, ic in enumerate(icons):
        ang = t_orb * 1.3 + k * 2 * math.pi / len(icons)
        z = math.sin(ang); sc = .75 + .35 * (z + 1) / 2
        i2 = tint(ic, PUR if z > 0 else LIL); i2 = i2.resize((int(80 * sc), int(80 * sc)), Image.LANCZOS)
        pts.append((z, i2, ox + R * math.cos(ang), oy + R * .28 * z + 40 * math.cos(ang * .5)))
    if ap > 0:
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((ox - R, oy - R * .28, ox + R, oy + R * .28), outline=PUR + (90,), width=3)
        paste(im, ring, 0, 0, ap * a, "lt")
        for z, i2, px, py in pts:
            if z <= 0: paste(im, i2, px, py, ap * a * .7)          # por detrás
    paste(im, p2, x, cy_ph, a); xy = (x, cy_ph, p2.width, p2.height)
    if crown_t0 is not None: crown_over(im, T, t, xy, (HT_T1[0] * w / TZ_T1.width * s, HT_T1[1] * w / TZ_T1.width * s), crown_t0, a)
    if ap > 0:
        for z, i2, px, py in pts:
            if z > 0: paste(im, i2, px, py, ap * a)                # por delante
    return xy

def card(img, w, r=26, border=None):
    im = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255); im.putalpha(m)
    if border: ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, outline=border + (255,), width=4)
    return shadow(im, 20, 18, .35)
TW_LFT = card(duo(Image.open(os.path.join(FOT, "tweet_lft.png")).convert("RGBA"), 1.0), 620)
PIN_LFT = None
TW_BACK = card(duo(Image.open(os.path.join(FOT, "tweet_back.png")).convert("RGBA"), 1.0), 430)

def face(key, size=(130, 160)):
    for ext in ("png", "jpg", "webp"):
        p = os.path.join(FOT, f"{key}.{ext}")
        if os.path.exists(p): break
    fx, fy = T2.FOCUS.get(key, (.5, .4)); im = Image.open(p).convert("RGB")
    r = max(size[0] / im.width, size[1] / im.height) * 1.8; im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    l = int(np.clip(im.width * fx - size[0] / 2, 0, im.width - size[0])); t = int(np.clip(im.height * fy - size[1] / 2, 0, im.height - size[1]))
    im = duo(im.crop((l, t, l + size[0], t + size[1])).convert("RGBA"))
    m = Image.new("L", size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), 20, fill=255); im.putalpha(m)
    return shadow(im, 10, 10, .3)
FACES = {k: face(k) for k in ("crashies", "stax", "buzz", "izu", "tenz", "sacy")}

# ---------------- fondos ----------------
_bg = {}
def bg(kind, ghost=None):
    key = (kind, ghost)
    if key not in _bg:
        if kind == "w": im = canvas(WHITE + (255,)); grid(im, (238, 236, 242, 255)); im.alpha_composite(WINDOW); gc = (226, 222, 232)
        else:
            im = canvas(PUR + (255,)); grid(im, (128, 34, 178, 255), 56); gc = (134, 44, 186)
            b2 = BURST.resize((380, 380)); paste(im, b2.rotate(200, expand=True), W + 170, -170, 1, "rt"); paste(im, b2.rotate(20, expand=True), -170, H + 170, 1, "lb")
        if ghost: paste(im, text_layer(ghost, IT(900, 230), gc), 360, 640)
        _bg[key] = im
    return _bg[key].copy()

def orbit_icons(im, cx, cy, r, icons, t, a=1.0, col=None):
    for k, ic in enumerate(icons):
        ang = t * .8 + k * 2 * math.pi / len(icons)
        i2 = tint(ic, col) if col else ic
        paste(im, i2, cx + r * math.cos(ang), cy + r * .45 * math.sin(ang), a * clamp01((t - k * .12) * 3))

def crown_over(im, T, t, photo_xy, ht, t0, a=1.0):
    """Corona que cae y flota sobre la cabeza (estilo diamante sobre columna)."""
    px, py, pw, ph = photo_xy
    hx = px - pw / 2 + ht[0]; hy = py - ph / 2 + ht[1]
    p = eo(prog(T, t0, t0 + .5))
    if p <= 0: return
    y = lerp(-200, hy - 70, p) + math.sin(T * 2.6) * 8
    paste(im, CROWN, hx, y, p * a)

def photo(im, ph, x, ybottom, t, a=1.0, zoom=.02):
    s = 1 + zoom * t; p2 = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)
    paste(im, p2, x, ybottom - p2.height / 2, a); return (x, ybottom - p2.height / 2, p2.width, p2.height), s

# ================= efectos nuevos (referencia "collage") =================
def _window():
    """Sombra de ventana (luz que entra por una ventana con marco en cruz) para fondos blancos."""
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    for x in (120, 380):
        d.rectangle((x, 0, x + 60, H), fill=255)          # montantes verticales
    d.rectangle((0, 520, W, 570), fill=255)                # travesaño
    for k in range(6): d.line((k * 160 - 200, H, k * 160 + 300, 0), fill=170, width=26)   # hojas/rama diagonal
    m = m.filter(ImageFilter.GaussianBlur(28))
    sh = Image.new("RGBA", (W, H), (60, 40, 80, 0)); sh.putalpha(m.point(lambda v: int(v * .08))); return sh
WINDOW = _window()

def ribbons(im, t, a=1.0):
    """Dos cintas moradas que se cruzan (como las rojas de la referencia)."""
    lay = canvas(); d = ImageDraw.Draw(lay); p = eo(clamp01(t * 1.5))
    for k, (y0, y1) in enumerate(((330, 640), (700, 360))):
        pts = [(x, lerp(y0, y1, x / W) + 50 * math.sin(x / 140 + k)) for x in range(-20, int(W * p) + 20, 12)]
        if len(pts) > 1: d.line(pts, fill=(130, 40, 190, 210), width=22)
    paste(im, lay, 0, 0, a, "lt")

def pin_card(card_img, rot=-4):
    """Tarjeta como polaroid: borde papel, chinche y clip."""
    pad = 18; c = Image.new("RGBA", (card_img.width + 2 * pad, card_img.height + 2 * pad + 40), (248, 244, 236, 255))
    c.alpha_composite(card_img, (pad, pad)); d = ImageDraw.Draw(c)
    cx = c.width // 2; d.ellipse((cx - 16, -4, cx + 16, 28), fill=PUR + (255,)); d.ellipse((cx - 7, 4, cx + 3, 14), fill=(220, 180, 255, 255))
    d.rounded_rectangle((26, c.height - 60, 46, c.height + 10), 10, outline=(150, 150, 160, 255), width=4)
    return shadow(c.rotate(rot, expand=True, resample=Image.BICUBIC), 18, 16, .3)

def note_card():
    n = obj("44_nota", w=680); tw = TW_LFT.resize((590, int(TW_LFT.height * 590 / TW_LFT.width)), Image.LANCZOS).rotate(-3, expand=True, resample=Image.BICUBIC)
    n = n.copy(); n.alpha_composite(tw, (int(n.width * .54 - tw.width / 2), int(n.height * .55 - tw.height / 2))); return n
PIN_LFT = note_card()

def brackets(im, t, col=INK, a=1.0):
    p = eo(clamp01(t * 3)); L = 46; m = lerp(70, 34, p); d = ImageDraw.Draw(im)
    c = col + (int(255 * a * p),)
    for (x, y, sx, sy) in ((m, m + 40, 1, 1), (W - m, m + 40, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        d.line((x, y, x + sx * L, y), fill=c, width=5); d.line((x, y, x, y + sy * L), fill=c, width=5)

def ghost_tenz(im, t, a=.13):
    g = TZ_T1.resize((700, int(TZ_T1.height * 700 / TZ_T1.width))).filter(ImageFilter.GaussianBlur(3))
    paste(im, g, 360 + math.sin(t * .6) * 15, 690, a)

FLY = None
def fly_through(img, T):
    """Objetos que cruzan volando con desenfoque de movimiento en ciertos cortes."""
    global FLY
    if FLY is None: FLY = [obj("42_bala", 380).rotate(-70, expand=True), obj("41_rifle", w=620), obj("40_revolver", w=460)]
    for k, cut in enumerate((C[3], C[5], C[9])):
        p = prog(T, cut - .28, cut + .22)
        if 0 < p < 1:
            o = FLY[k]; x = lerp(-300, W + 300, p); y = 640 + (k - 1) * 120 + math.sin(p * 3) * 80
            lay = canvas(); paste(lay, o, x, y); lay = M.motion_blur_x(lay, 120) if hasattr(M, "motion_blur_x") else lay
            from render import motion_blur_x as mbx
            img.alpha_composite(mbx(lay, 60, 8))
    return img

def puzzle_tile(im, T, t0, ch, x, y, size=300, col=PUR):
    """Letra gigante que se arma con 4 piezas que entran deslizándose."""
    tile = Image.new("RGBA", (size, size), col + (255,)); d = ImageDraw.Draw(tile)
    d.text((size / 2, size / 2 + 8), ch, font=ANTON(int(size * .9)), fill=WHITE, anchor="mm")
    h = size // 2
    for k, (qx, qy, dx, dy) in enumerate(((0, 0, -1, -1), (h, 0, 1, -1), (0, h, -1, 1), (h, h, 1, 1))):
        p = eo(prog(T, t0 + k * .07, t0 + k * .07 + .35))
        if p <= 0: continue
        piece = tile.crop((qx, qy, qx + h, qy + h))
        paste(im, piece, x - h + qx + h / 2 + dx * 260 * (1 - p), y - h + qy + h / 2 + dy * 260 * (1 - p), p)
    if T > t0 + .6:   # costuras del rompecabezas
        dd = ImageDraw.Draw(im); dd.line((x - h, y, x + h, y), fill=(255, 255, 255, 120), width=3); dd.line((x, y - h, x, y + h), fill=(255, 255, 255, 120), width=3)

def neg_flash(img, T):
    for tk in (Wd["t1"], Wd["rey"]):
        if 0 <= T - tk < 2 / FPS:
            g = ImageOps.invert(img.convert("RGB")).convert("L")
            return Image.merge("RGB", (g.point(lambda v: int(v * .35)), g.point(lambda v: int(v * .95)), g)).convert("RGBA")
    return img

# ---------------- escenas ----------------
def scene(i, T):
    t = T - C[i]
    if i == 0:   # Después de la caída… dos caminos
        im = bg("w")
        rib = Image.new("RGBA", (620, 90), PUR + (255,)); ImageDraw.Draw(rib).text((310, 47), "DESPUÉS DE LA CAÍDA", font=ANTON(56), fill=WHITE, anchor="mm")
        p = eo(prog(t, .15, .5)); paste(im, rib.crop((0, 0, max(1, int(620 * p)), 90)), 50, 200, 1, "lm")
        if T < Wd["caminos"] - .05:
            tenz_orbit(im, T, t, 360, 1300, 560, max(0, t - .4), a=eo(prog(t, .1, .6)))
        else:
            tt = T - Wd["caminos"]; pop(im, COMPASS, 360, 760, tt, 0, .4)
            word(im, "solo hay", IT(400, 52), 360, 360, tt, 0, INK); word(im, "dos caminos", IT(900, 100), 360, 460, tt, .2, PUR)
        return im
    if i == 1:   # quedarte en el suelo / o volver más fuerte
        im = bg("p", "fuerte"); ghost_tenz(im, t, .16)
        word(im, "quedarte en el suelo…", IT(400, 46), 360, 250, t, .05, WHITE)
        sp = eo(prog(T, Wd["fuerte"] - .05, Wd["fuerte"] + .35)) * 70
        L = CHAIN.crop((0, 0, CHAIN.width // 2, CHAIN.height)); R = CHAIN.crop((CHAIN.width // 2, 0, CHAIN.width, CHAIN.height))
        pa = clamp01(t * 3); paste(im, L, 360 - L.width / 2 - sp, 720, pa); paste(im, R, 360 + R.width / 2 + sp, 720, pa)
        word(im, "o volver", IT(400, 56), 360, 380, T, Wd["volver"], LILL); word(im, "Más fuerte", IT(900, 112), 360, 1000, T, Wd["fuerte"], WHITE)
        return im
    if i == 2:   # septiembre 2024 … dijo adiós
        im = bg("w", "adiós"); pop(im, HOUR, 560, 780, t, .05, .45)
        gone = eo(prog(T, Wd["adios"], Wd["adios"] + 1.0))
        if gone < 1:
            tmp = canvas(); tenz_orbit(tmp, T, t, 250, 1300, 430, -1)
            if gone > 0: tmp = tmp.filter(ImageFilter.GaussianBlur(6 * gone))
            paste(im, tmp, 360, 640 - 50 * gone, 1 - gone)
        word(im, "septiembre 2024", IT(400, 50), 360, 220, t, .05, INK)
        word(im, "uno de los más grandes", IT(400, 40), 360, 300, T, Wd["grandes"], PUR)
        word(im, "Dijo adiós", IT(900, 108), 360, 410, T, Wd["adios"], INK)
        return im
    if i == 3:   # muchos pensaron que no volvería jamás
        im = bg("p"); ghost_tenz(im, t, .18); pop(im, MON, 360, 800, t, .05, .45)
        word(im, "muchos pensaron", IT(400, 52), 360, 260, t, .05, WHITE); word(im, "que no volvería", IT(400, 52), 360, 330, t, .4, LILL)
        word(im, "Jamás", IT(900, 140), 360, 470, T, Wd["jamas"] - .15, WHITE)
        return im
    if i == 4:   # 21 de octubre · LFT
        im = bg("w"); word(im, "hasta que el 21 de octubre", IT(400, 44), 360, 200, t, .05, INK)
        word(im, "publicó solo tres letras", IT(400, 44), 360, 260, T, Wd["letras"], PUR)
        ribbons(im, t); pop(im, PIN_LFT, 360, 900, t, .2, .45)
        for k, (ch, key) in enumerate(zip("LFT", ("L", "F", "Tt"))):
            pop(im, text_layer(ch, ANTON(190), PUR if k == 2 else INK), 200 + k * 160, 480, T, Wd[key], .3)
        word(im, "buscando equipo", IT(400, 46), 360, 1180, T, Wd["equipo"], PUR)
        return im
    if i == 5:   # 12 nov 2026 · T1 lo hace oficial · the KING is back
        im = bg("p", "T1")
        out = eo(prog(T, Wd["t1"] - .2, Wd["t1"] + .2))
        if out < 1:
            pop(im, text_layer("12", ANTON(420), WHITE), 360, 640 - 120 * out, T, C[5] + .05, .45, 1 - out)
            word(im, "de noviembre", IT(900, 76), 360, 900, T, C[5] + .5, LILL); word(im, "2026", ANTON(110), 360, 1010, T, Wd["nov"] + .9 if "nov" in Wd else C[5] + 1.2, WHITE)
        word(im, "12 · noviembre · 2026", IT(400, 48), 360, 190, T, Wd["t1"] - .1, LILL)
        pop(im, T1_W.resize((240, int(T1_W.height * 240 / T1_W.width))), 360, 405, T, Wd["t1"], .4)
        word(im, "lo hace", IT(400, 56), 360, 440, T, Wd["oficial"] - .05, WHITE); word(im, "Oficial", IT(900, 110), 360, 530, T, Wd["oficial"] + .2, WHITE)
        pop(im, TW_BACK, 360, 1000, T, Wd["king"] - .3, .45)
        return im
    if i == 6:   # Tyson TenZ Ngo vuelve a competir
        im = bg("w", "TenZ")
        tenz_orbit(im, T, t, 450, 1300, 500, max(0, T - Wd["tenz"]), crown_t0=Wd["tenz"], a=eo(prog(t, 0, .5)))
        cf = T2.clip("clip_tenz", t)
        if cf is not None: pop(im, card(duo(cf), 190, border=PUR), 120, 960, t, .3, .4)
        word(im, "Tyson", IT(400, 50), 60, 150, T, Wd["tyson"], INK, "lm")
        word(im, "TenZ", IT(900, 140), 50, 260, T, Wd["tenz"], PUR, "lm")
        word(im, "Ngo", IT(400, 50), 60, 370, T, Wd["ngo"], INK, "lm")
        word(im, "vuelve a", IT(400, 46), 60, 450, T, Wd["compite"], INK, "lm"); word(im, "competir", IT(900, 64), 60, 520, T, Wd["compite"] + .2, PUR, "lm")
        return im
    if i == 7:   # 2 veces campeón de Masters
        im = bg("w"); ImageDraw.Draw(im).rectangle((0, 960, W, H), fill=PUR + (255,))
        word(im, "y no vuelve con cualquiera", IT(400, 44), 360, 170, t, .05, INK)
        word(im, "dos veces campeón", IT(900, 78), 360, 260, T, Wd["campeon"], PUR)
        paste(im, COL, 360, lerp(1700, 1080, eo(prog(t, 0, .6))))
        cup = obj("45_copa", 340); cy = 1080 - COL.height / 2 - cup.height / 2 + 20
        p = eo(prog(T, Wd["campeon"], Wd["campeon"] + .6)); paste(im, cup, 360, lerp(-250, cy, p) + math.sin(T * 2.5) * 6 * p, clamp01(p * 3))
        word(im, "Reykjavík", IT(900, 44), 150, 820, T, Wd["reyk"], INK); word(im, "2021", IT(400, 40), 150, 870, T, Wd["reyk"] + .15, INK)
        word(im, "Madrid", IT(900, 44), 575, 820, T, Wd["madrid"], PUR); word(im, "2024", IT(400, 40), 575, 870, T, Wd["madrid"] + .15, PUR)
        return im
    if i == 8:   # su nuevo equipo
        im = bg("p"); ghost_tenz(im, t, .16 * (1 - prog(T, Wd["crashies"] - .3, Wd["crashies"] + .6))); word(im, "y su nuevo", IT(400, 52), 360, 150, t, .05, LILL); word(im, "Equipo", IT(900, 100), 360, 240, t, .3, WHITE)
        rows = [("crashies", "Crashies", "crashies"), ("stax", "Stax", "stax"), ("buzz", "BuZz", "buzz"), ("izu", "iZu", "izu"), ("tenz", "TenZ", "tenz2")]
        for k, (f, n, key) in enumerate(rows):
            y = 480 + k * 140; last = f == "tenz"; p = eo(prog(T, Wd[key], Wd[key] + .3))
            if p <= 0: continue
            paste(im, FACES[f], lerp(-100, 150, p), y, p)
            paste(im, text_layer(n, IT(900, 90 if last else 72), WHITE if last else LILL), lerp(900, 250, p), y, p, "lm")
            if last: ImageDraw.Draw(im).rectangle((250, y + 55, lerp(250, 640, p), y + 61), fill=WHITE + (255,))
        p = eo(prog(T, C[8] + .5, C[8] + .9))
        if p > 0:
            paste(im, FACES["sacy"].resize((90, 110)), lerp(900, 300, p), 1180, p)
            paste(im, text_layer("Sacy · coach (reportado)", IT(400, 34), LILL), lerp(1000, 360, p), 1180, p, "lm")
        return im
    if i == 9:   # debut esperado
        im = bg("w", "2027")
        k = KING.rotate((1 - eo(prog(t, .05, .7))) * 20, expand=True, resample=Image.BICUBIC); paste(im, k, lerp(620, 470, eo(prog(t, .05, .7))), lerp(1700, 1010, eo(prog(t, .05, .7))))
        word(im, "su debut esperado", IT(400, 48), 300, 200, t, .05, INK)
        word(im, "Red Bull Home Ground", IT(900, 52), 300, 290, T, Wd["rbhg"], PUR)
        word(im, "Diciembre", IT(900, 96), 260, 390, T, Wd["dic"], INK)
        word(im, "y en enero", IT(400, 46), 230, 500, T, Wd["enero"], PUR)
        word(im, "VCT Pacific", IT(900, 80), 250, 590, T, Wd["pacific"], PUR)
        pop(im, VLOGO.resize((160, int(VLOGO.height * 160 / VLOGO.width))), 160, 760, T, Wd["pacific"] + .3, .4)
        return im
    if i == 10:  # dos años después… eligió el segundo camino
        im = bg("p"); ghost_tenz(im, t, .18); pop(im, HOUR.resize((260, int(HOUR.height * 260 / HOUR.width))), 360, 760, t, .05, .4)
        p = eo(prog(T, Wd["camino"], Wd["camino"] + .5))
        word(im, "dos años después…", IT(400, 56), 360, 250, t, .05, WHITE)
        word(im, "eligió el segundo", IT(400, 52), 400, 960, T, Wd["camino"], LILL); word(im, "Camino", IT(900, 100), 420, 1050, T, Wd["camino"] + .25, WHITE)
        return im
    # 11: el rey volvió
    im = bg("w", "King")
    puzzle_tile(im, T, Wd["rey"] - .2, "R", 190, 820, 380)
    tenz_orbit(im, T, t, 360, 1340, 600, max(0, T - Wd["rey"] + .3), crown_t0=Wd["rey"] - .15)
    word(im, "el", IT(400, 50), 360, 80, t, .02, INK)
    word(im, "Rey", IT(900, 150), 250, 190, T, Wd["rey"], PUR); word(im, "volvió", IT(900, 100), 470, 300, T, Wd["volvio"], INK)
    for k, (s_, x, y, a) in enumerate([("DUPLEXDRAGON", 40, 1210, "lm"), ("@DuplexDragon_", 680, 1210, "rm"),
                                         ("Fuente: anuncio oficial de T1 · 12 nov 2026", 360, 1240, "mm"), ("Clips e imágenes: créditos a sus autores · fan edit", 360, 1262, "mm")]):
        p = prog(t, 1.0 + k * .2, 1.4 + k * .2)
        if p > 0: paste(im, text_layer(s_, SANS(400 if k > 1 else 600, 15 if k > 1 else 18), (110, 100, 125)), x, y, p, a)
    return im

SUBS = sorted([Wd[k] for k in ("caminos", "fuerte", "adios", "jamas", "L", "F", "Tt", "t1", "king", "tenz", "reyk", "madrid",
                                "crashies", "stax", "buzz", "izu", "tenz2", "dic", "pacific", "camino", "rey", "volvio")])

def frame(T):
    i = max(k for k in range(len(C)) if T >= C[k]); img = scene(i, T)
    if T > Wd["t1"] + .5:   # logo chico de T1 arriba a la izquierda (arriba a la derecha está el estallido)
        paste(img, T1_SMALL_W if i % 2 else T1_SMALL_P, 40, 60, .9 * clamp01(T - Wd["t1"] - .5), "lm")
    if i % 2 == 0: brackets(img, T - C[i], PUR, .8)
    img = fly_through(img, T)
    dc = T - C[i]; ds = min([T - s for s in SUBS if T >= s] or [9])
    s = 1 + .05 * (1 - eo(clamp01(dc / .3))) if i > 0 else 1
    s += .025 * max(0, 1 - ds / .2)
    img = scale_about(img, s, bg=WHITE + (255,))
    if i > 0 and dc < .12:
        img = Image.blend(img, canvas((WHITE if i % 2 else LILL) + (255,)), .85 * (1 - dc / .12))
    img = neg_flash(img, T)
    if T > DUR - 1.0: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, DUR - 1.0, DUR - .1))
    return img.convert("RGB")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((W // 2, H // 2)) for t in ts]; sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for k, x in enumerate(ims): sh.paste(x, (k * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview"); sys.exit()
    out = a[0]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(TZ, "mezcla_rev_sfx.wav"), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n):
        p.stdin.write(frame(k / FPS).tobytes())
        if k % 300 == 0: print(f"{k}/{n}", flush=True)
    p.stdin.close(); p.wait(); print("OK", out)
