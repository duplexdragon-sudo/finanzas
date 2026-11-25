#!/usr/bin/env python3
"""Worlds 2026 de League of Legends: Bilibili Gaming campeón — motion graphics morado.
Fuentes: LoL Esports, Liquipedia, Sheep Esports, Dot Esports, CGTN (nov 2026)."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "lol"); FPS = 30
SONG = os.path.join(HERE, "..", "audio", "musica", "c9_ext.wav"); SONG_AT = 0.0; T1 = os.path.join(HERE, "..", "zek", "clips", "despedida.mp4")

N = len(json.load(open(os.path.join(PD, "guion.json")))); DL, WT = [], []
for i in range(N):
    w = wave.open(os.path.join(PD, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(PD, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
    for ch, a in zip(al["characters"], al["character_start_times_seconds"]):
        if ch.isspace():
            if cur: ws.append((cur, st)); cur = ""
        else:
            if not cur: st = a
            cur += ch
    if cur: ws.append((cur, st))
    WT.append(ws)
LS = []; t = .15
for d in DL: LS.append(t); t += d + .2
DUR = t + 1.3
SEG = {f"L{i}": (LS[i] - .1 if i else 0.0) for i in range(N)}
ORDER = sorted(SEG, key=SEG.get)
def wt(k, s, n=0):
    hits = [st for w_, st in WT[k] if s.lower() in w_.lower()]
    return LS[k] + (hits[min(n, len(hits) - 1)] if hits else 0)

# ---------- zona segura TikTok / Instagram ----------
def SY(y): return y + 110 if y < 400 else (y - 170 if y > 900 else y)
_word, _slam, _ribbon, _stamp, _pop, _counter = word, slam, ribbon, stamp, pop, counter
# margen: ningún texto pasa de MAXW px (queda aire a los lados, el borde derecho libre para los botones)
from PIL import ImageFont
MAXW = 580
def fitf(txt, f, maxw=MAXW):
    while f.getlength(txt) > maxw and f.size > 18: f = ImageFont.truetype(f.path, f.size - 2)
    return f
def word(im, s_, f, x, y, *a, **k): return _word(im, s_, fitf(s_, f), x, SY(y), *a, **k)
def slam(im, s_, f, x, y, *a, **k): return _slam(im, s_, fitf(s_, f), x, SY(y), *a, **k)
def ribbon(im, txt, x, y, *a, **k):
    a = list(a)
    if len(a) > 4:
        while ANTON(a[4]).getlength(txt) + 60 > MAXW + 20 and a[4] > 20: a[4] -= 2
    return _ribbon(im, txt, x, SY(y), *a, **k)
def stamp(im, txt, x, y, *a, **k):
    a = list(a)
    if len(a) > 4:
        while ANTON(a[4]).getlength(txt) + 80 > MAXW and a[4] > 20: a[4] -= 2
    return _stamp(im, txt, x, SY(y), *a, **k)
def pop(im, img, x, y, *a, **k): return _pop(im, img, x, SY(y), *a, **k)
def counter(im, T, t0, t1, v0, v1, font, x, y, *a, **k): return _counter(im, T, t0, t1, v0, v1, font, x, SY(y), *a, **k)

RC = os.path.join(PD, "rec")
def cut(n, w):
    im = duo(Image.open(os.path.join(RC, n + ".png")).convert("RGBA"), 1.08); im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
    im = S.fade_bottom(im, .14); return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
def has(n): return os.path.exists(os.path.join(RC, n + ".png"))
BIN = cut("bin", 300); XUN = cut("xun", 300); KNI = cut("knight", 300); VIP = cut("viper", 300); FAK = cut("faker", 300)
ON_ = cut("on", 300) if has("on") else None
COPA = Image.open(os.path.join(RC, "copa.png")).convert("RGBA"); COPA = COPA.crop(COPA.getchannel("A").getbbox())
def logo_c(path, h):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
BLG = logo_c(os.path.join(PD, "logos", "blg.webp"), 200); GEN = logo_c(os.path.join(PD, "logos", "geng.png"), 200)
def gem(col, k):
    """Ícono de 'gema hextech' (rombo con brillo) para el anillo que gira, sin usar arte de Riot."""
    s = 96; c = Image.new("RGBA", (s, s)); d = ImageDraw.Draw(c)
    if k % 2: d.polygon([(48, 4), (92, 48), (48, 92), (4, 48)], fill=col + (255,)); d.polygon([(48, 22), (74, 48), (48, 74), (22, 48)], fill=WHITE + (255,))
    else: d.regular_polygon((48, 48, 44), 6, fill=col + (255,)); d.regular_polygon((48, 48, 22), 6, rotation=30, fill=WHITE + (255,))
    return c
def champ(k):
    im = Image.open(os.path.join(PD, "champs", f"c{k}.png")).convert("RGBA"); c = Image.new("RGBA", (136, 136)); ImageDraw.Draw(c).ellipse((0, 0, 135, 135), fill=WHITE + (255,))
    c.alpha_composite(im, (4, 4)); return c
def mono(img, keep_light=False):
    """Logo a un solo color (la plantilla del anillo lo tiñe: blanco sobre morado, morado sobre blanco)."""
    im = img.convert("RGBA"); a = np.asarray(im).astype(int)
    if keep_light: m = ((a[..., :3].min(2) > 170) & (a[..., 3] > 128)).astype(np.uint8) * 255   # BLG: solo las letras blancas
    else: m = (a[..., 3] > 128).astype(np.uint8) * 255
    o = Image.new("RGBA", im.size, (255, 255, 255, 255)); o.putalpha(Image.fromarray(m)); o = o.crop(o.getbbox()); o.thumbnail((128, 128), Image.LANCZOS)
    c = Image.new("RGBA", (128, 128)); c.alpha_composite(o, ((128 - o.width) // 2, (128 - o.height) // 2)); return c
def twotone(img, base, inner, light_only=True):
    """Logo en dos tonos de marca: silueta del color 'base' y letras claras del color 'inner'."""
    a = np.asarray(img.convert("RGBA")).astype(int); sil = a[..., 3] > 100; lt = (a[..., :3].min(2) > 170) & sil
    o = np.zeros(a.shape, np.uint8); o[sil] = base + (255,); o[lt] = inner + (255,); return Image.fromarray(o, "RGBA")
def solid(img, col):
    a = np.asarray(img.convert("RGBA")); o = Image.new("RGBA", img.size, col + (255,)); o.putalpha(Image.fromarray(a[..., 3])); return o
BLG_P, BLG_W = twotone(BLG, PUR, WHITE), twotone(BLG, WHITE, PUR)     # morado sobre fondo blanco · blanco sobre fondo morado
GEN_W = solid(GEN, WHITE)
TEAMS = [mono(BLG, True), mono(GEN)] + [mono(logo_c(os.path.join(PD, "logos", f), 200)) for f in sorted(os.listdir(os.path.join(PD, "logos"))) if f.startswith("eq_")]
ORB_ICONS = [TEAMS[k % len(TEAMS)] for k in range(max(8, len(TEAMS)))]   # logos de los equipos del Mundial girando (teñidos)
_XE = Image.open(os.path.join(PD, "logos", "marca_xe.png")).convert("RGBA"); _XE = _XE.crop(_XE.getchannel("A").getbbox()); _XE = _XE.resize((58, int(_XE.height * 58 / _XE.width)), Image.LANCZOS)
def marca(col):
    m = Image.new("RGBA", _XE.size, col + (255,)); m.putalpha(_XE.getchannel("A").point(lambda v: int(v * .85))); return m
XE_W, XE_P = marca(WHITE), marca(PUR)
def orb(im, logo, x, ybot, T, t_orb, a, size=60, col=WHITE, col2=LILL):
    pad = Image.new("RGBA", (int(logo.width * 1.7), int(logo.height * 1.35))); pad.alpha_composite(logo, ((pad.width - logo.width) // 2, 0))
    S.player_orbit(im, pad, x, ybot, T, t_orb, ORB_ICONS, a, size, col, col2)
def card(img, w, pad=22):
    im = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS); c = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, fill=255)
    c.paste(WHITE + (255,), (0, 0, c.width, c.height)); c.alpha_composite(im, (pad, pad)); c.putalpha(m)
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, outline=PUR + (255,), width=5); return shadow(c, 14, 14, .35)
def chipx(txt, ok, w=520, col=None):
    c = Image.new("RGBA", (w, 100)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, w - 1, 99), 30, fill=(col or (PUR if ok else (200, 30, 60))) + (255,))
    f = ANTON(50)
    while f.getlength(txt) > w - 130: f = ANTON(f.size - 2)
    d.text((32, 50), txt, font=f, fill=WHITE, anchor="lm")
    if ok: c.alpha_composite(L.check(56), (w - 82, 22))
    else: d.line((w - 78, 28, w - 34, 72), fill=WHITE, width=9); d.line((w - 34, 28, w - 78, 72), fill=WHITE, width=9)
    return shadow(c, 10, 10, .3)
def bob(T, k=0): return 8 * math.sin(T * 2.4 + k)
def nchip(txt, col=PUR, fg=WHITE, size=40): return SN.namechip(txt, col, fg, size)
def calcard(top, mes, dia=None, w=400, h=440):
    c = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=WHITE + (255,), outline=PUR + (255,), width=6)
    d.rounded_rectangle((0, 0, w - 1, 120), 34, fill=PUR + (255,)); d.rectangle((0, 80, w - 1, 120), fill=PUR + (255,))
    d.text((w / 2, 62), top, font=ANTON(60), fill=WHITE, anchor="mm")
    for x in (110, w - 110): d.rounded_rectangle((x - 12, -24, x + 12, 34), 10, fill=(60, 10, 90, 255))
    if dia: d.text((w / 2, 245), dia, font=ANTON(170), fill=PUR, anchor="mm"); d.text((w / 2, 380), mes, font=ANTON(64), fill=INK, anchor="mm")
    else: d.text((w / 2, 280), mes, font=ANTON(170), fill=PUR, anchor="mm")
    return shadow(c, 18, 16, .35)
def calflip(im, T, t0, t1, cards, y=560):
    if T < t0: return
    a = eo(clamp01((T - t0) / .3)); f = eo(clamp01((T - t0) / max(.1, t1 - t0))) * (len(cards) - 1); i = int(f); fr = f - i
    if T >= t1: i, fr = len(cards) - 1, 0
    card_ = cards[i]
    if fr > 0 and i < len(cards) - 1:
        sy = abs(math.cos(math.pi * fr)); card_ = cards[i] if fr < .5 else cards[i + 1]; card_ = card_.resize((card_.width, max(1, int(card_.height * sy))), Image.BICUBIC)
    b = 1 + .12 * math.exp(-(T - t1) * 7) if T >= t1 else 1
    if b != 1: card_ = card_.resize((int(card_.width * b), int(card_.height * b)), Image.BICUBIC)
    paste(im, card_, 360, y, a)
CAL_24 = [calcard("WORLDS", "2024"), calcard("WORLDS", "2025"), calcard("WORLDS", "2026")]
CAL_NOV = [calcard("2026", "NOVIEMBRE", "1"), calcard("2026", "NOVIEMBRE", "7"), calcard("2026", "NOVIEMBRE", "14")]
def headcrop(img, ar=1.15, k=2.4):
    """Recorte centrado en la cabeza: todas las caras quedan del mismo tamaño dentro de la tarjeta."""
    a = np.asarray(img.getchannel("A")) > 120; rows = np.where(a.any(1))[0]; t = rows[0]
    r = min(len(a) - 1, t + int(.10 * img.width)); cols = np.where(a[r])[0]
    hw = max(20, cols[-1] - cols[0]); cx = (cols[0] + cols[-1]) / 2
    w = int(hw * k); h = int(w * ar); x0 = int(cx - w / 2); y0 = int(t - .18 * hw)
    c = Image.new("RGBA", (w, h)); c.alpha_composite(img.crop((max(0, x0), max(0, y0), min(img.width, x0 + w), min(img.height, y0 + h))), (max(0, -x0), max(0, -y0))); return c
def same(img, ar=1.15):
    w = img.width; h = int(w * ar)
    if img.height >= h: return img.crop((0, 0, w, h))
    c = Image.new("RGBA", (w, h)); c.alpha_composite(img, (0, h - img.height)); return c
LANE = {"Bin": "TOP", "Shun": "JG", "Náit": "MID", "Váiper": "ADC", "On": "SUP"}
_BD = {}
def badge(key, sz):
    """Disco blanco con borde morado y la posición (TOP/JG/MID/ADC/SUP) en morado."""
    if (key, sz) in _BD: return _BD[(key, sz)]
    k = 4; S_ = sz * k; c = Image.new("RGBA", (S_, S_)); d = ImageDraw.Draw(c)
    d.ellipse((0, 0, S_ - 1, S_ - 1), fill=WHITE + (255,), outline=PUR + (255,), width=4 * k)
    t = LANE.get(key, ""); f = ANTON(int(S_ * (.42 if len(t) <= 3 else .34))); d.text((S_ / 2, S_ / 2), t, font=f, fill=PUR, anchor="mm")
    _BD[(key, sz)] = c.resize((sz, sz), Image.LANCZOS); return _BD[(key, sz)]
def rolefly(im, T, t0, key, x, y, sz=58):
    p = prog(T, t0, t0 + .32)
    if p <= 0: return
    e = ease_back(p, 1.6); ic = badge(key, sz).rotate((1 - eo(p)) * 300, resample=Image.BICUBIC, expand=True); sx = 1 if x > 360 else -1
    paste(im, shadow(ic, 6, 6, .3), lerp(x + sx * 420, x, e), lerp(y - 260, y, e) + 4 * math.sin(T * 5), clamp01(p * 3))
def pur(T, name):
    im = Image.new("RGBA", (W, H), PUR + (255,)); stripes(im, T, SEG[name], WHITE); ring(im, 360, 700, 330, T * 1.5, LILL, .35); ring(im, 360, 700, 280, -T * 1.6, WHITE, .3, 3, 24); return im
def flash(im, T, ts):
    tt = T - max([x for x in ts if x <= T] or [-9])
    return Image.blend(im, canvas(LILL + (255,)), .75 * (1 - tt / .12)) if 0 < tt < .12 and T > .3 else im
CL = os.path.join(PD, "clips"); _GC = {}
def gclip(name, ss, crop, t, size, dur=2.5):
    key = (name, ss, crop, size)
    if key not in _GC:
        x, y, w, h = crop
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", os.path.join(CL, name + ".mp4"), "-vf",
                              f"fps=30,crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:force_original_aspect_ratio=increase,crop={size[0]}:{size[1]},eq=contrast=1.06:saturation=1.1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0], 3).astype(np.float32)
        l = a.mean(3, keepdims=True) / 255; shd = np.clip(.55 - l, 0, .55) / .55
        _GC[key] = np.clip(a * (1 - .25 * shd) + np.array(PUR, np.float32) * .25 * shd, 0, 255).astype(np.uint8)
    fr = _GC[key]; return Image.fromarray(fr[int(np.clip(t * 30, 0, len(fr) - 1))]).convert("RGBA")
def vcard(name, ss, crop, t, size, T, t0, y, grow=.03):
    pc = ease_back(prog(T, t0, t0 + .3), 1.2)
    if pc <= 0: return None
    c = L.rcard(gclip(name, ss, crop, t, size), 28, WHITE); s_ = lerp(.85, 1, pc) * (1 + grow * max(0, T - t0))
    return c.resize((int(c.width * s_), int(c.height * s_))), clamp01(pc * 2)
def tile(txt, ok):
    c = Image.new("RGBA", (124, 112)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 123, 111), 22, fill=(PUR if ok else (200, 30, 60)) + (255,))
    d.text((62, 34), txt, font=ANTON(34), fill=WHITE, anchor="mm")
    if ok: c.alpha_composite(L.check(44).resize((44, 44)), (40, 58))
    else: d.line((44, 62, 80, 98), fill=WHITE, width=8); d.line((80, 62, 44, 98), fill=WHITE, width=8)
    return shadow(c, 8, 8, .3)
def sc(img, w): return img.resize((w, int(img.height * w / img.width)), Image.LANCZOS)

RED = (200, 30, 60)
PLAYERS = [("Bin", "BIN", "TOP"), ("Shun", "XUN", "JUNGLA"), ("Náit", "KNIGHT", "MID"), ("Váiper", "VIPER", "ADC"), ("On", "ON", "SUPPORT")]
IMG = {"Bin": BIN, "Shun": XUN, "Náit": KNI, "Váiper": VIP, "On": ON_}
def scene(name, T):
    t = T - SEG[name]
    if name == "L0":                                  # gancho: jugadores → racha rota → la copa
        tB, tC = wt(0, "rompió") - .1, wt(0, "son") - .1
        if T < tB:
            im = pur(T, name); slam(im, "BILIBILI GAMING", ANTON(110), 360, 150, T, .05, WHITE)
            for k, (key, x, y) in enumerate((("Bin", 220, 480), ("Shun", 500, 480), ("Náit", 220, 810), ("Váiper", 500, 810))):
                pk = ease_back(prog(T, .1 + k * .1, .4 + k * .1), 1.5)
                if pk > 0: paste(im, card(headcrop(IMG[key]), max(10, int(185 * pk))), x, y + bob(T, k) * .5, clamp01(pk * 2))
            for k, (key, x, y) in enumerate((("Bin", 220, 480), ("Shun", 500, 480), ("Náit", 220, 810), ("Váiper", 500, 810))):
                rolefly(im, T, .3 + k * .1, key, x + 88, y - 112 + bob(T, k) * .5, 62)
        elif T < tC:
            im = bg("w", "COREA"); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
            pop(im, chipx("LCK · 4 MUNDIALES SEGUIDOS", False, 600), 360, 250, T, tB, .3)
            r = vcard("tk6", 9.0, (0, 330, 720, 950), T - tB, (380, 424), T, tB + .05, 640)
            if r: paste(im, r[0], 360, 640, r[1])
            stamp(im, "RACHA ROTA", 360, 1110, T, wt(0, "racha") - .1, RED, -6, 110)
        else:
            im = pur(T, name); slam(im, "CAMPEONES DEL MUNDO", ANTON(100), 360, 150, T, tC, WHITE)
            pu = ease_back(prog(T, tC + .05, tC + .5), 1.2); cp = sc(COPA, 230)
            orb(im, cp, 360, lerp(1300, 930, pu) + 8 * math.sin(T * 2), T, max(0, T - tC), clamp01(pu), 70)
            if T > wt(0, "Lig") - .2: ribbon(im, "LEAGUE OF LEGENDS · WORLDS 2026", 360, 1080, T, wt(0, "Lig") - .2, PUR, WHITE, 40, "mm")
        im = flash(im, T, (tB, tC)); return im
    if name == "L1":
        im = bg("w", "2024"); stripes(im, T, SEG[name], PUR, .5); tv = wt(1, "volvieron") - .15
        if T < tv:
            word(im, "hace dos años", IT(900, 56), 360, 150, T, SEG[name] + .05, INK)
            calflip(im, T, SEG[name] + .1, SEG[name] + .3, CAL_24[:1], 560)
            tl = wt(1, "Ti") - .2
            if T > tl: pop(im, chipx("FINAL 2024 · T1 3–2 BLG", False, 560), 360, 880, T, tl, .3)
        else:
            slam(im, "VOLVIERON", ANTON(130), 360, 160, T, tv, PUR)
            r = vcard("tk5", 0.5, (0, 0, 720, 540), T - tv, (480, 360), T, tv + .05, 600)
            if r: paste(im, r[0], 360, 600, r[1])
            tc = wt(1, "copa") - .2
            if T > tc: stamp(im, "POR LA COPA", 360, 1060, T, tc, PUR, -5, 100)
        return flash(im, T, (tv,))
    if name == "L2":
        im = pur(T, name); tg = wt(2, "ganaron") - .2
        if T < tg:
            word(im, "la gran final", IT(900, 56), 360, 150, T, SEG[name] + .05, WHITE)
            tn = wt(2, "Nueva") - .2
            if T < tn: calflip(im, T, SEG[name] + .1, wt(2, "noviembre") + .1, CAL_NOV, 580)
            else:
                r = vcard("tk4", 8.0, (0, 300, 720, 720), T - tn, (520, 520), T, tn, 600)
                if r: paste(im, r[0], 360, 600, r[1])
                pop(im, nchip("NUEVA YORK · BARCLAYS CENTER", WHITE, PUR, 34), 360, 1080, T, tn + .1, .3)
        else:
            ribbon(im, "14 NOV · NUEVA YORK", 360, 160, T, tg, PUR, WHITE, 46, "mm")
            pop(im, sc(BLG_W, 220), 175, 520, T, tg, .35); pop(im, sc(GEN_W, 130), 545, 520, T, wt(2, "Yen") - .1, .35)
            counter(im, T, tg, wt(2, "uno"), 0, 3, ANTON(150), 330, 520, WHITE); slam(im, "–1", ANTON(150), 400, 520, T, wt(2, "uno") - .05, WHITE)
            tf = wt(2, "Yi") + .1
            if T > tf: stamp(im, "BLG 3–1 GEN.G", 360, 780, T, tf, (255, 255, 255), -5, 90)
        return flash(im, T, (tg,))
    if name == "L3":
        im = bg("w", "MAPA"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "perdieron el primer mapa", IT(900, 50), 360, 140, T, SEG[name] + .05, INK)
        r = vcard("tk2", 4.0, (0, 512, 576, 512), T - SEG[name], (560, 500), T, SEG[name] + .1, 560)
        if r: paste(im, r[0], 360, 560, r[1])
        ks = [wt(3, "mapa") - .3, wt(3, "no") - .1, wt(3, "ni") - .1, wt(3, "más") - .1]
        for k, ok in enumerate((False, True, True, True)):
            pp = ease_back(prog(T, ks[k], ks[k] + .3), 1.5)
            if pp > 0: paste(im, tile(f"MAPA {k + 1}", ok).resize((int(132 * pp) + 1, int(120 * pp) + 1)), 132 + k * 152, 900, clamp01(pp * 2))
        return im
    if name == "L4":
        im = Image.blend(gclip("tk3", 2.0, (0, 0, 720, 1280), min(t, 4.9), (720, 1280), 5.0), canvas(PUR + (255,)), .72)
        stripes(im, T, SEG[name], WHITE); word(im, "el segundo mapa duró", IT(900, 54), 360, 150, T, SEG[name] + .05, WHITE)
        counter(im, T, wt(4, "duró"), wt(4, "minutos"), 0, 53, ANTON(260), 360, 500, WHITE)
        tm = wt(4, "minutos") - .1
        if T > tm: slam(im, "MINUTOS", ANTON(90), 360, 680, T, tm, WHITE)
        tl = wt(4, "largo") - .3
        if T > tl: stamp(im, "EL MÁS LARGO DEL TORNEO", 360, 830, T, tl, (255, 255, 255), -5, 70)
        return im
    if name == "L5":
        im = bg("w", "LCK"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "eliminaron a los", IT(900, 52), 360, 140, T, SEG[name] + .05, INK); slam(im, "4 DE COREA", ANTON(120), 360, 250, T, wt(5, "cuatro") - .15, PUR)
        ks = [wt(5, "Janwa"), wt(5, "Di"), wt(5, "Ti"), wt(5, "Yen")]
        for k, tx in enumerate(("HANWHA LIFE · 2–0", "DPLUS KIA · 3–0", "T1 · 3–1", "GEN.G · 3–1")):
            pp = ease_back(prog(T, ks[k] - .25, ks[k] + .05), 1.4)
            if pp > 0: paste(im, chipx(tx, False, 520), lerp(1020 if k % 2 else -300, 360, pp), 520 + k * 120, clamp01(pp))
        return im
    if name == "L6":
        tm = wt(6, "MVP") - .25
        if T < tm:                                    # presentación jugador por jugador
            ts = [SEG["L6"]] + [wt(6, k) - .15 for k, _, _ in PLAYERS[1:]]
            j = max([i for i, x in enumerate(ts) if x <= T] or [0]); key, nm, lane = PLAYERS[j]; t0 = ts[j]
            im = Image.new("RGBA", (W, H), PUR + (255,)) if j % 2 == 0 else bg("w", nm)
            if j % 2 == 0: stripes(im, T, t0, WHITE)
            fg, bgc = (WHITE, PUR) if j % 2 == 0 else (PUR, WHITE)
            slam(im, nm, ANTON(110), 360, 140, T, t0, fg); pop(im, nchip(lane, fg, bgc, 30), 360, 230, T, t0 + .1, .3)
            pc = ease_back(prog(T, t0, t0 + .3), 1.2)
            body = IMG[key] if IMG[key] is not None else None
            if key == "Náit":                          # Knight con su jugada (quadrakill de Orianna)
                r = vcard("tk7", 20.0, (0, 40, 576, 760), T - t0, (420, 554), T, t0, 690, .02)
                if r: paste(im, r[0], 360, 690, r[1])
                ph = ease_back(prog(T, t0 + .15, t0 + .45), 1.4)
                if ph > 0: hd = sc(KNI, 170); paste(im, shadow(hd, 8, 8, .35), 115, 1010 - hd.height / 2, clamp01(ph * 2))
            elif body is not None:
                c = card(headcrop(body, 1.05, 2.8), int(380 * lerp(.85, 1, pc))); paste(im, c, 360, 650 + bob(T, j) * .4, clamp01(pc * 2))
            else:
                c = card(sc(BLG_P, 300), int(380 * lerp(.85, 1, pc))); paste(im, c, 360, 650, clamp01(pc * 2))
            if key == "Náit": rolefly(im, T, t0 + .15, key, 615, 1040, 84)
            else: rolefly(im, T, t0 + .15, key, 560, 860, 96)
            return flash(im, T, ts[1:])
        im = pur(T, name)                             # MVP: Knight
        slam(im, "MVP DE LA FINAL", ANTON(100), 360, 150, T, tm, WHITE)
        pk = ease_back(prog(T, tm, tm + .35), 1.2); kn = sc(KNI, 430)
        if T < wt(6, "Chóvi") - .25: paste(im, shadow(kn, 12, 12, .35), 360, 640 + bob(T) * .5, clamp01(pk * 2))
        tk = wt(6, "Náit", 1) - .2
        if T > tk: ribbon(im, "KNIGHT · 13 / 6 / 41", 360, 1000, T, tk, PUR, WHITE, 46, "mm")
        tc = wt(6, "Chóvi") - .25
        if T > tc:
            r = vcard("tk1", 5.6, (0, 690, 576, 280), T - tc, (600, 292), T, tc, 600)
            if r: paste(im, r[0], 360, 600, r[1])
            pop(im, nchip("LE GANÓ EL DUELO A CHOVY", INK, WHITE, 30), 360, 1095, T, tc, .3)
        return flash(im, T, (tm,))
    if name == "L7":
        im = pur(T, name); td = wt(7, "después") - .15
        if T < td:
            slam(im, "PRIMER MID CHINO", ANTON(100), 360, 150, T, SEG[name] + .05, WHITE)
            pop(im, nchip("CAMPEÓN DEL MUNDO", WHITE, PUR, 34), 360, 240, T, wt(7, "campeón") - .2, .3)
            pk = ease_back(prog(T, SEG[name] + .1, SEG[name] + .45), 1.2); paste(im, shadow(sc(KNI, 420), 12, 12, .35), 360, 700 + bob(T) * .5, clamp01(pk * 2))
        else:
            counter(im, T, td, wt(7, "años"), 0, 13, ANTON(220), 360, 190, WHITE)
            word(im, "años de mids coreanos", IT(900, 50), 360, 340, T, wt(7, "años") - .1, WHITE)
            tf = wt(7, "Féiker") - .2
            if T > tf:
                pf = ease_back(prog(T, tf, tf + .3), 1.3); paste(im, card(same(FAK, 1.0), int(300 * lerp(.85, 1, pf))), 360, 700, clamp01(pf * 2))
                pop(im, nchip("FAKER", WHITE, PUR, 40), 360, 1080, T, tf + .1, .3)
        return flash(im, T, (td,))
    if name == "L8":
        im = bg("w", "VIPER"); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "VIPER", ANTON(130), 360, 150, T, wt(8, "Váiper") - .15, PUR)
        pk = ease_back(prog(T, SEG[name] + .1, SEG[name] + .4), 1.3); paste(im, card(same(VIP, 1.0), int(240 * lerp(.85, 1, pk))), 360, 520, clamp01(pk * 2))
        for k, (tx, key) in enumerate((("2021 · EDWARD GAMING", "suma"), ("2026 · BILIBILI GAMING", "título"))):
            t0 = wt(8, key) - .2; pp = ease_back(prog(T, t0, t0 + .3), 1.4)
            if pp > 0: paste(im, chipx(tx, True, 540, PUR), lerp(1000, 360, pp), 790 + k * 115, clamp01(pp))
        return im
    if name == "L9":
        im = pur(T, name)
        word(im, "China no ganaba un Mundial desde", IT(900, 46), 360, 140, T, SEG[name] + .05, WHITE)
        counter(im, T, SEG[name] + .3, wt(9, "veintiuno"), 2026, 2021, ANTON(150), 360, 235, WHITE)
        r = vcard("tk2", 46.0, (0, 512, 576, 512), T - SEG[name], (470, 418), T, SEG[name] + .1, 700)
        if r: paste(im, r[0], 360, 700, r[1])
        tf = wt(9, "veintiuno")
        if T > tf: stamp(im, "5 AÑOS DE ESPERA", 360, 1130, T, tf, (255, 255, 255), -5, 70)
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "LOL")
    word(im, "¿Se acabó el reinado de", IT(400, 50), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "COREA?", ANTON(130), 360, 265, T, wt(k, "Corea") - .15, PUR)
    tc = wt(k, "comentarios") - .1; tsh = wt(k, "compártelo") - .15
    if tc < T < tsh: pop(im, U.COMMENT, 150, 530 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 150, 615, T, tc + .05, PUR)
    if T >= tsh: pop(im, U.SHARE, 150, 530 + math.sin(T * 5) * 10, T, tsh, .35); word(im, "compártelo", IT(900, 38), 150, 615, T, tsh + .05, PUR)
    orb(im, sc(BLG_P, 220), 480, 800 + 6 * math.sin(T * 2), T, max(0, t - .3), clamp01((t - .3) * 3), 56, PUR, LIL)
    for j, s_ in enumerate(("Fuentes: LoL Esports · Liquipedia · Sheep Esports · Dot Esports · CGTN · nov 2026", "Final Worlds 2026: Bilibili Gaming 3–1 Gen.G · Barclays Center, Nueva York")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L4", "L7", "L9"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "BLG", "L1": "2024", "L2": "3–1", "L3": "MAPA", "L4": "53", "L5": "LCK", "L6": " ", "L7": "MID", "L8": "VIPER", "L9": "2021", f"L{N-1}": "LOL"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, wt(0, "rompió"), wt(0, "racha"), wt(0, "son"), SEG["L1"] + .1, wt(1, "volvieron"), wt(2, "ganaron"), wt(2, "Yi"), wt(3, "no"), wt(4, "minutos"), wt(4, "largo"),
                              wt(5, "Janwa"), wt(5, "Di"), wt(5, "Ti"), wt(5, "Yen"), wt(6, "MVP"), wt(7, "Féiker"), wt(8, "título"), wt(9, "veintiuno")])
    return HITS
def frame(T):
    name = [n for n in ORDER if T >= SEG[n]][-1]; idx = ORDER.index(name); img = scene(name, T); dc = T - SEG[name]
    nxt = SEG[ORDER[idx + 1]] if idx + 1 < len(ORDER) else DUR
    img = scale_about(img, 1 + .035 * clamp01(dc / max(1, nxt - SEG[name])), bg=WHITE + (255,)); SN.kicker(img, name, dc)
    particles(img, T + idx * 7, WHITE if name in PURPLE_SC else LIL, .3)
    if idx % 2 == 0: brackets(img, dc, WHITE if name in PURPLE_SC else PUR, .8)
    paste(img, text_layer("@DuplexDragon_", SANS(600, 18), WHITE if name in PURPLE_SC else PUR), 40, 175, .7, "lm")
    import numpy as _np                                      # marca de agua XE en todo el video: blanca sobre morado, morada sobre blanco
    zone = _np.asarray(img.crop((630, 150, 700, 200)).convert("L")).mean()
    paste(img, XE_W if zone < 150 else XE_P, 650, 175, .9)
    if idx > 0 and dc < .18:
        p = dc / .18; lay = canvas(); d = ImageDraw.Draw(lay); x = lerp(-200, W + 900, p)
        d.polygon([(x - 900, 0), (x, 0), (x - 500, H), (x - 1400, H)], fill=PUR + (255,)); img.alpha_composite(lay)
    s = 1 + .06 * (1 - eo(clamp01(dc / .35))) if idx > 0 else 1; img = scale_about(img, s, bg=WHITE + (255,))
    S.HITS[:] = hits(); img = S.impact_fx(img, T)
    if T < .08: img = Image.blend(img, canvas(WHITE + (255,)), .7 * (1 - T / .08))
    if T > DUR - .8: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, DUR - .8, DUR - .1))
    return img.convert("RGB")

def audio(out):
    SR = 48000; Ns = int(DUR * SR); vox = np.zeros((Ns, 2), np.float32)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    for i, s in enumerate(LS):
        v = rd(os.path.join(PD, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    Sx = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "clink", "boom", "cheer", "braam", "hit808", "glitch", "swoosh", "riser", "crowd", "typing")}
    k = N - 1
    ev = [("braam", 0.0, .7), ("hit808", 0.0, .6)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("impact", wt(0, "racha"), .5), ("cheer", wt(0, "campeones"), .35), ("shimmer", wt(0, "campeones"), .5), ("typing", SEG["L2"] + .2, .35), ("boom", wt(2, "Yi") + .1, .5),
        ("impact", wt(3, "mapa"), .5), ("pop", wt(3, "no"), .5), ("pop", wt(3, "ni"), .5), ("pop", wt(3, "más"), .5), ("typing", wt(4, "duró"), .4), ("clink", wt(4, "largo"), .5),
        ("impact", wt(5, "Janwa"), .5), ("impact", wt(5, "Di"), .5), ("impact", wt(5, "Ti"), .5), ("impact", wt(5, "Yen"), .5)] + [("pop", wt(6, k), .5) for k, _, _ in PLAYERS] + [
        ("riser", wt(6, "MVP") - 1.0, .4), ("braam", wt(6, "MVP"), .5), ("cheer", wt(6, "MVP"), .3), ("typing", wt(7, "después"), .4), ("pop", wt(7, "Féiker"), .5),
        ("shimmer", wt(8, "suma"), .5), ("shimmer", wt(8, "título"), .5), ("typing", SEG["L9"] + .3, .4), ("clink", wt(9, "veintiuno"), .5),
        ("pop", wt(k, "comentarios"), .6), ("pop", wt(k, "compártelo"), .6), ("shimmer", wt(k, "compártelo"), .4)]
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(PD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(PD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(PD, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.34[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[md];"
                    f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=first,atrim=0:{DUR},afade=t=out:st={DUR - 1.5}:d=1.5,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(x).resize((W // 2, H // 2)) for x in ts]; sh = Image.new("RGB", (W // 2 * min(6, len(ims)), H // 2 * ((len(ims) + 5) // 6)))
        for k, x in enumerate(ims): sh.paste(x, ((k % 6) * W // 2, (k // 6) * H // 2))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=85); print("preview", {k: round(SEG[k], 2) for k in ORDER}, round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(PD, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
