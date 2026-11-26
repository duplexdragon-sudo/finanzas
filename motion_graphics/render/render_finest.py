#!/usr/bin/env python3
"""Revive me, Jett: homenaje a Lance \"Finest\" Arcilla.
Fuentes: Riot Games (@VALORANT 27/04/2022), Valorant Wiki, NME, Dexterto, Know Your Meme."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "finest"); FPS = 30
SONG = os.path.join(HERE, "..", "audio", "musica", "c9_ext84.wav"); SONG_AT = 0.0; T1 = os.path.join(HERE, "..", "zek", "clips", "despedida.mp4")

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
LS = []; t = 3.6
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

ART = os.path.join(PD, "arte")
def ld(n): im = Image.open(os.path.join(ART, n)).convert("RGBA"); return im.crop(im.getchannel("A").getbbox())
JETT = ld("jett.png"); SAGE = ld("sage.png"); SPRAY = ld("spray.png")
BANNER = Image.open(os.path.join(PD, "fotos", "finest_banner.jpg")).convert("RGBA").crop((240, 0, 720, 1170))
def headbust(img):
    a = np.asarray(img.getchannel("A")) > 120; rows = np.where(a.any(1))[0]; t0 = rows[0]; w = img.width
    r = t0 + int(.08 * img.height); cols = np.where(a[r])[0]; cx = (cols[0] + cols[-1]) / 2; hw = int(img.height * .42)
    return img.crop((int(cx - hw / 2), t0 - 20, int(cx + hw / 2), t0 - 20 + int(hw * 1.1)))
def headcrop(img, ar=1.15, k=2.4):
    """Recorte centrado en la cabeza: todas las caras quedan del mismo tamaño dentro de la tarjeta."""
    a = np.asarray(img.getchannel("A")) > 120; rows = np.where(a.any(1))[0]; t = rows[0]
    r = min(len(a) - 1, t + int(.10 * img.width)); cols = np.where(a[r])[0]
    hw = max(20, cols[-1] - cols[0]); cx = (cols[0] + cols[-1]) / 2
    w = int(hw * k); h = int(w * ar); x0 = int(cx - w / 2); y0 = int(t - .18 * hw)
    c = Image.new("RGBA", (w, h)); c.alpha_composite(img.crop((max(0, x0), max(0, y0), min(img.width, x0 + w), min(img.height, y0 + h))), (max(0, -x0), max(0, -y0))); return c
JETT_H, SAGE_H = ld("jett_icon.png"), ld("sage_icon.png")
ICON = {"jett": JETT_H, "sage": SAGE_H}
ORB_ICONS = [S.R.HAB[k] for k in ("jett_0", "jett_1", "jett_2", "jett_3", "jett_0", "jett_1", "jett_2", "jett_3") if k in S.R.HAB] or S.ICON_CY
def chipx(txt, ok, w=520, col=None):
    c = Image.new("RGBA", (w, 100)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, w - 1, 99), 30, fill=(col or (PUR if ok else (200, 30, 60))) + (255,))
    f = ANTON(50)
    while f.getlength(txt) > w - 130: f = ANTON(f.size - 2)
    d.text((32, 50), txt, font=f, fill=WHITE, anchor="lm")
    if ok: c.alpha_composite(L.check(56), (w - 82, 22))
    else: d.line((w - 78, 28, w - 34, 72), fill=WHITE, width=9); d.line((w - 34, 28, w - 78, 72), fill=WHITE, width=9)
    return shadow(c, 10, 10, .3)
def same(img, ar=1.15):
    w = img.width; h = int(w * ar)
    if img.height >= h: return img.crop((0, 0, w, h))
    c = Image.new("RGBA", (w, h)); c.alpha_composite(img, (0, h - img.height)); return c
def sc(img, w): return img.resize((w, int(img.height * w / img.width)), Image.LANCZOS)
def orb(im, logo, x, ybot, T, t_orb, a, size=60, col=WHITE, col2=LILL, pad_=True):
    pad = Image.new("RGBA", (int(logo.width * 1.5), int(logo.height * 1.2))); pad.alpha_composite(logo, ((pad.width - logo.width) // 2, 0))
    S.player_orbit(im, pad, x, ybot, T, t_orb, ORB_ICONS, a, size, col, col2)
def card(img, w, pad=22):
    im = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS); c = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, fill=255)
    c.paste(WHITE + (255,), (0, 0, c.width, c.height)); c.alpha_composite(im, (pad, pad)); c.putalpha(m)
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, outline=PUR + (255,), width=5); return shadow(c, 14, 14, .35)
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
CAL_20 = [calcard("2020", "JUN"), calcard("2020", "JUL"), calcard("2020", "AGO")]
CAL_21 = [calcard("2020", "DIC"), calcard("2021", "ENE"), calcard("2021", "FEB")]
CAL_22 = [calcard("2022", "FEB"), calcard("2022", "MAR"), calcard("2022", "ABR")]
def pur(T, name):
    im = Image.new("RGBA", (W, H), PUR + (255,)); stripes(im, T, SEG[name], WHITE); ring(im, 360, 700, 330, T * 1.5, LILL, .35); ring(im, 360, 700, 280, -T * 1.6, WHITE, .3, 3, 24); return im
def flash(im, T, ts):
    tt = T - max([x for x in ts if x <= T] or [-9])
    return Image.blend(im, canvas(LILL + (255,)), .75 * (1 - tt / .12)) if 0 < tt < .12 and T > .3 else im
CL = os.path.join(PD, "clips"); _GC = {}
def gclip(name, ss, crop, t, size, dur=6.0):
    key = (name, ss, crop, size)
    if key not in _GC:
        x, y, w, h = crop
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", os.path.join(CL, name + ".mp4"), "-vf",
                              f"fps=30,crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:force_original_aspect_ratio=increase,crop={size[0]}:{size[1]},eq=contrast=1.06:saturation=1.1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0], 3).astype(np.float32)
        l = a.mean(3, keepdims=True) / 255; shd = np.clip(.55 - l, 0, .55) / .55
        _GC[key] = np.clip(a * (1 - .25 * shd) + np.array(PUR, np.float32) * .25 * shd, 0, 255).astype(np.uint8)
    fr = _GC[key]; return Image.fromarray(fr[int(t * 30) % len(fr)]).convert("RGBA")
def vcard(name, ss, crop, T, t0, size, grow=.008):
    pc = ease_back(prog(T, t0, t0 + .3), 1.2)
    if pc <= 0: return None
    c = L.rcard(gclip(name, ss, crop, T - t0, size), 28, WHITE); s_ = lerp(.85, 1, pc) * (1 + grow * max(0, T - t0))
    return c.resize((int(c.width * s_), int(c.height * s_))), clamp01(pc * 2)
# recortes del área de juego de cada clip (con arma y HUD)
CR = {"tk1": (0, 0, 576, 660), "tk2": (0, 270, 576, 400)}
_SC = {}
SECT = {"tk2": [(0.0, 3.6), (51.5, 57.0)], "tk1": [(0.5, 13.5)]}
def synclip(im, name, ss, t_word, T, tcard, size, y, win=3.0):
    lo, hi = next(((a, b) for a, b in SECT.get(name, []) if a <= ss <= b), (0.0, 1e9))
    pre = max(0.0, t_word - tcard); st = max(lo, ss - pre); win = min(win, hi - ss); dur = (ss - st) + win
    key = (name, st, CR[name], size)
    if key not in _GC: gclip(name, st, CR[name], 0, size, dur)
    fr = _GC[key]; n = len(fr); i = int((T - t_word + (ss - st)) * 30)        # la habilidad cae justo en la palabra
    if i < 0: i = i % n                                                         # antes: repite su propia sección, nunca otra cosa
    elif i >= n: k0 = int((ss - st) * 30); i = k0 + (i - k0) % max(1, n - k0)
    pc = ease_back(prog(T, tcard, tcard + .3), 1.2)
    if pc <= 0: return
    c = L.rcard(Image.fromarray(fr[min(i, n - 1)]).convert("RGBA"), 28, WHITE); s_ = lerp(.85, 1, pc)
    c = c.resize((int(c.width * s_), int(c.height * s_))); c._clip = True; paste(im, c, 360, y, clamp01(pc * 2))
def mousecap(side, sz=96):
    c = Image.new("RGBA", (sz, sz)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, sz - 1, sz - 1), 20, fill=WHITE + (255,), outline=PUR + (255,), width=5)
    x0, y0, x1, y1 = sz * .3, sz * .14, sz * .7, sz * .86; d.rounded_rectangle((x0, y0, x1, y1), int(sz * .2), outline=PUR + (255,), width=4)
    xm, ym = sz / 2, sz * .45; d.line((xm, y0, xm, ym), fill=PUR + (255,), width=3); d.line((x0, ym, x1, ym), fill=PUR + (255,), width=3)
    if side == "L": d.rounded_rectangle((x0 + 3, y0 + 3, xm - 2, ym - 2), 6, fill=PUR + (255,))
    elif side == "R": d.rounded_rectangle((xm + 2, y0 + 3, x1 - 3, ym - 2), 6, fill=PUR + (255,))
    else: d.ellipse((xm - 6, ym + 8, xm + 6, ym + 20), fill=PUR + (255,))
    return shadow(c, 8, 8, .3)
def stepcap(it, sz=96):
    if it in ("L", "R", "M"): return mousecap(it, sz)
    if it == "SALTO":
        c = Image.new("RGBA", (int(sz * 1.6), sz)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, c.width - 1, sz - 1), 20, fill=WHITE + (255,), outline=PUR + (255,), width=5)
        d.text((c.width / 2, sz / 2), "ESPACIO", font=ANTON(int(sz * .3)), fill=PUR, anchor="mm"); return shadow(c, 8, 8, .3)
    return keycap("F·" if it == "F" else it, sz)
STEPLBL = {"L": "CLIC IZQ.", "R": "CLIC DER.", "M": "MIRA", "SALTO": "SALTAR"}
def steps(im, T, items, y, purple_bg):
    """Fila de teclas que aparecen una por una, justo cuando la voz las dice, con flechas entre ellas."""
    sz = 92; caps = [stepcap(k, sz) for k, _ in items]; gap = 46; tw = sum(c.width for c in caps) + gap * (len(caps) - 1); x = 360 - tw / 2
    fg = WHITE if purple_bg else PUR
    for i, ((k, t0), c) in enumerate(zip(items, caps)):
        cx = x + c.width / 2; p = ease_back(prog(T, t0 - .1, t0 + .2), 1.6)
        if p > 0:
            on = T < (items[i + 1][1] - .1 if i + 1 < len(items) else 1e9)          # la tecla que se está diciendo late
            cc = c.resize((max(1, int(c.width * p * (1.08 if on else 1))), max(1, int(c.height * p * (1.08 if on else 1)))))
            paste(im, cc, cx, y, clamp01(p * 2))
            if k in STEPLBL: paste(im, text_layer(STEPLBL[k], ANTON(22), fg), cx, y + 66, clamp01(p * 2))
            if i > 0: paste(im, text_layer("›", ANTON(60), fg), x - gap / 2, y - 4, clamp01(p * 2))
        x += c.width + gap
def wx(k, w_, n=0):
    """Tiempo de una palabra EXACTA (sin puntuación), la n-ésima vez que aparece en la frase k."""
    hits = [st for w, st in WT[k] if w.strip(".,:;¿?¡!…").lower() == w_.lower()]
    return LS[k] + hits[min(n, len(hits) - 1)]
def keycap(k, sz=96):
    c = Image.new("RGBA", (sz, sz)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, sz - 1, sz - 1), 20, fill=WHITE + (255,), outline=PUR + (255,), width=5)
    t = {"F": "PASIVA", "F·": "F"}.get(k, k); f = ANTON(int(sz * (.55 if len(t) == 1 else .26))); d.text((sz / 2, sz / 2), t, font=f, fill=PUR, anchor="mm"); return shadow(c, 8, 8, .3)
def habdisc(k, sz, purple_bg):
    c = Image.new("RGBA", (sz, sz)); d = ImageDraw.Draw(c); d.ellipse((0, 0, sz - 1, sz - 1), fill=(WHITE if purple_bg else PUR) + (255,))
    ic = sc(HAB[k], int(sz * .62)); t = Image.new("RGBA", ic.size, (PUR if purple_bg else WHITE) + (255,)); t.putalpha(ic.getchannel("A"))
    c.alpha_composite(t, ((sz - ic.width) // 2, (sz - ic.height) // 2)); return shadow(c, 8, 8, .3)
def habfly(im, T, t0, k, x, y, sz, purple_bg):
    p = prog(T, t0, t0 + .35)
    if p <= 0: return
    e = ease_back(p, 1.6); ic = habdisc(k, sz, purple_bg).rotate((1 - eo(p)) * 300, resample=Image.BICUBIC, expand=True)
    paste(im, ic, lerp(x + 420, x, e), lerp(y - 240, y, e) + 4 * math.sin(T * 5), clamp01(p * 3))
def habhead(im, T, t0, k, purple_bg):
    """Cabecera de habilidad: tecla + nombre + ícono oficial que entra volando."""
    fg = WHITE if purple_bg else PUR
    slam(im, HNAME[k], ANTON(96), 400, 150, T, t0, fg)
    if T > t0 + .25: pop(im, keycap(k, 84), 120, 150, T, t0 + .25, .3)
    habfly(im, T, t0 + .3, k, 360, SY(240), 84, purple_bg)

RED = (200, 30, 60)
def clipin(im, name, ss, T, t0, size, y=660):
    y = y + 40 if y >= 640 and y <= 700 else y
    r = vcard(name, ss, CR[name], T, t0, size)
    if r: paste(im, r[0], 360, y, r[1])
def label(im, txt, T, t0, purple_bg, y=1135):
    pop(im, nchip(txt, WHITE if purple_bg else PUR, PUR if purple_bg else WHITE, 30), 360, y, T, t0, .3)
RED = (200, 30, 60)
def bubble(im, txt, who, x, y, T, t0, left=True, w=470):
    """Globo de diálogo con el ícono del agente al lado (nunca sobre su cara)."""
    p = ease_back(prog(T, t0, t0 + .3), 1.4)
    if p <= 0: return
    f = IT(700, 30); words = txt.split(); lines, cur = [], ""
    for w_ in words:
        if f.getlength((cur + " " + w_).strip()) > w - 50 and cur: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    lines.append(cur); h = 44 * len(lines) + 40
    b = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(b); d.rounded_rectangle((0, 0, w - 1, h - 1), 28, fill=WHITE + (255,), outline=PUR + (255,), width=5)
    for i, ln in enumerate(lines): d.text((26, 22 + i * 44), ln, font=f, fill=INK)
    b = shadow(b, 10, 10, .3); ic = sc(ICON[who], 96); ic2 = Image.new("RGBA", (104, 104)); ImageDraw.Draw(ic2).ellipse((0, 0, 103, 103), fill=WHITE + (255,), outline=PUR + (255,), width=4); ic2.alpha_composite(ic.resize((90, 90)), (7, 7))
    bx = x + (70 if left else -70); ix = x - w / 2 - 10 if left else x + w / 2 + 10
    bb = b.resize((max(1, int(b.width * p)), max(1, int(b.height * p)))); paste(im, bb, bx, y, clamp01(p * 2)); paste(im, ic2, ix + (0 if left else 0), y, clamp01(p * 2))
def scene(name, T):
    t = T - SEG[name]
    if name == "L0":
        if T < 3.45:                                  # su voz original: "Jett, revive me… use your ulti, Jett"
            im = pur(T, name)
            synclip(im, "tk2", 0.0, 0.1, T, 0.0, (540, 376), 700, 3.4)
            for k, (tx, t0) in enumerate((("«JETT,", .05), ("REVIVE ME!»", .55))):
                slam(im, tx, ANTON(110), 360, 150 + k * 100, T, t0, WHITE)
            pop(im, nchip("AUDIO ORIGINAL · 2020", WHITE, PUR, 30), 360, 1080, T, .9, .3)
        else:
            im = bg("w", ""); stripes(im, T, 3.45, PUR, .5)
            slam(im, "REVIVE ME, JETT", ANTON(110), 360, 150, T, 3.5, PUR)
            pu = ease_back(prog(T, 3.55, 4.0), 1.2); js = sc(JETT, 380)
            orb(im, js, 360, lerp(1500, 1250, pu) + 6 * math.sin(T * 2), T, max(0, T - 3.6), clamp01(pu), 64, PUR, LIL)
            tf = wt(0, "frase") - .2
            if T > tf: pop(im, nchip("LA FRASE MÁS FAMOSA DE VALORANT", PUR, WHITE, 30), 360, 262, T, tf, .3)
            th = wt(0, "historia") - .2
            if T > th: stamp(im, "HISTORIA REAL", 360, 1160, T, th, PUR, -5, 70)
        return flash(im, T, (3.45,))
    if name == "L1":
        im = pur(T, name); tr = wt(1, "rogaba") - .2
        if T < tr:
            calflip(im, T, SEG[name] + .1, wt(1, "veinte") + .1, CAL_20, 520)
            tl = wt(1, "Lance") - .2
            if T > tl: pop(im, nchip("LANCE \"FINEST\" ARCILLA", WHITE, PUR, 40), 360, 860, T, tl, .3); pop(im, nchip("FILIPINAS", PUR, WHITE, 28), 360, 930, T, wt(1, "filipino") - .2, .3)
        else:
            slam(im, "«JETT, REVÍVEME»", ANTON(96), 360, 160, T, tr, WHITE)
            synclip(im, "tk2", 1.0, tr + .3, T, tr, (560, 390), 620, 3.0)
        return flash(im, T, (tr,))
    if name == "L2":
        im = bg("w", ""); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "EL DETALLE", ANTON(110), 360, 150, T, SEG[name] + .05, PUR)
        tj, ts = wt(2, "Jett") - .2, wt(2, "Sage") - .5
        pj = ease_back(prog(T, tj, tj + .35), 1.2); pp = ease_back(prog(T, ts, ts + .35), 1.2)
        if pj > 0: paste(im, card(JETT_H, 230), 200, 600, clamp01(pj * 2)); pop(im, chipx("JETT", False, 250), 200, 860, T, wt(2, "no") - .1, .3)
        if pp > 0: paste(im, card(SAGE_H, 230), 520, 600, clamp01(pp * 2)); pop(im, chipx("SAGE", True, 250, PUR), 520, 860, T, wt(2, "Sage") - .1, .3)
        return im
    if name == "L3":
        im = pur(T, name); word(im, "el clip pasó los", IT(900, 52), 360, 150, T, SEG[name] + .05, WHITE)
        counter(im, T, SEG[name] + .3, wt(3, "millones") + .2, 0, 3, ANTON(240), 360, 450, WHITE)
        tm = wt(3, "millones") - .1
        if T > tm: slam(im, "MILLONES DE VISTAS", ANTON(80), 360, 620, T, tm, WHITE)
        tg = wt(3, "meme") - .3
        if T > tg: stamp(im, "EL MEME MÁS GRANDE DEL JUEGO", 360, 820, T, tg, (255, 255, 255), -4, 60)
        return im
    if name == "L4":
        im = bg("w", ""); stripes(im, T, SEG[name], PUR, .5)
        word(im, "hasta los", IT(900, 52), 360, 150, T, SEG[name] + .05, INK); slam(im, "ACTORES DE VOZ", ANTON(110), 360, 260, T, wt(4, "actores") - .15, PUR)
        synclip(im, "tk1", 5.0, wt(4, "reaccionaron"), T, SEG[name] + .15, (380, 436), 700, 3.0)
        tr = wt(4, "reaccionaron") - .2
        if T > tr: pop(im, nchip("REACCIONARON AL MEME", PUR, WHITE, 30), 360, 1135, T, tr, .3)
        return im
    if name == "L5":
        im = pur(T, name); tg = wt(5, "grafiti") - .2
        if T < tg:
            calflip(im, T, SEG[name] + .1, wt(5, "veintiuno") + .1, CAL_21, 540)
            tr = wt(5, "Riot") - .2
            if T > tr: pop(im, nchip("RIOT LO METIÓ AL JUEGO", WHITE, PUR, 34), 360, 880, T, tr, .3)
        else:
            slam(im, "GRAFITI OFICIAL", ANTON(110), 360, 160, T, tg, WHITE)
            ps = ease_back(prog(T, tg, tg + .4), 1.5); sp = sc(SPRAY, 400).rotate(4 * math.sin(T * 2), resample=Image.BICUBIC, expand=True)
            paste(im, shadow(sp, 12, 12, .35), 360, 690 + 8 * math.sin(T * 2.2), clamp01(ps * 2))
            pop(im, nchip("«REVIVE ME, JETT!»", WHITE, PUR, 36), 360, 1150, T, tg + .3, .3)
        return flash(im, T, (tg,))
    if name == "L6":
        im = bg("w", ""); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "EN EL JUEGO", ANTON(110), 360, 150, T, SEG[name] + .05, PUR)
        bubble(im, "Sage, ¿cuándo me vas a enseñar a revivir?", "jett", 330, 520, T, wt(6, "Jett") - .2, True)
        bubble(im, "Jett, así no funcionan los radiantes… Ah, es una broma.", "sage", 390, 760, T, wt(6, "enseñar") - .2, False)
        pop(im, nchip("DIÁLOGO DEL JUEGO", PUR, WHITE, 26), 360, 1110, T, wt(6, "revivir") - .3, .3)
        return im
    if name == "L7":                                  # parte emotiva: más calma, sin golpes
        im = Image.new("RGBA", (W, H), (40, 10, 60, 255)); ring(im, 360, 640, 300, T * .6, LIL, .25); ring(im, 360, 640, 250, -T * .7, WHITE, .2, 3, 24)
        calflip(im, T, SEG[name] + .1, wt(7, "veintidós") + .1, CAL_22, 520)
        tl = wt(7, "falleció") - .3
        if T > tl: word(im, "Lance falleció", IT(900, 60), 360, 880, T, tl, WHITE)
        ta = wt(7, "veintiún") - .2
        if T > ta: pop(im, nchip("21 AÑOS", WHITE, PUR, 40), 360, 980, T, ta, .4)
        return im
    if name == "L8":
        im = Image.new("RGBA", (W, H), (40, 10, 60, 255)); ring(im, 360, 640, 320, T * .6, LIL, .25)
        word(im, "el homenaje de Riot", IT(900, 52), 360, 150, T, SEG[name] + .05, WHITE)
        pb = ease_back(prog(T, wt(8, "título") - .3, wt(8, "título") + .2), 1.2)
        if pb > 0: bn = sc(BANNER, 250); paste(im, shadow(bn, 14, 14, .4), 360, 650 + 6 * math.sin(T * 1.6), clamp01(pb * 2))
        tt = wt(8, "todos") - .2
        if T > tt: pop(im, nchip("TÍTULO DE JUGADOR · EPISODIO 4, ACTO 3", WHITE, PUR, 26), 360, 1175, T, tt, .3)
        return im
    if name == "L9":
        im = Image.new("RGBA", (W, H), (40, 10, 60, 255)); ring(im, 360, 640, 320, T * .6, LIL, .25)
        word(im, "como dijo Riot:", IT(900, 52), 360, 200, T, SEG[name] + .05, WHITE)
        tq = wt(9, "regaló") - .3
        if T > tq:
            for k, ln in enumerate(("«…le regaló a la comunidad", "momentos de alegría", "inolvidables»")):
                word(im, ln, IT(900, 50), 360, 480 + k * 80, T, tq + k * .25, WHITE)
            pop(im, nchip("RIOT GAMES · 27 DE ABRIL DE 2022", WHITE, PUR, 28), 360, 820, T, tq + .8, .3)
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", ""); stripes(im, T, SEG[f"L{k}"], PUR, .5); ring(im, 360, 640, 280, T * 1.3, PUR, .35); ring(im, 360, 640, 230, -T * 1.5, LIL, .3, 3, 24)
    word(im, "cada vez que alguien grita", IT(900, 48), 360, 150, T, SEG[f"L{k}"] + .1, INK)
    slam(im, "«REVIVE ME, JETT»", ANTON(96), 360, 255, T, wx(k, "revive") - .15, PUR)
    tf = wx(k, "Finest") - .2
    if T > tf:
        ps = ease_back(prog(T, tf, tf + .4), 1.4); sp = sc(SPRAY, 290); paste(im, shadow(sp, 10, 10, .3), 360, 640 + 6 * math.sin(T * 2), clamp01(ps * 2))
        pop(im, nchip("FINEST SIGUE EN EL JUEGO", PUR, WHITE, 34), 360, 830, T, tf + .2, .3)
    te = wx(k, "Escribe") - .2
    if T > te: pop(im, nchip("ESCRIBE «FINEST» EN LOS COMENTARIOS", INK, WHITE, 28), 360, 1080, T, te, .3)
    for j, s_ in enumerate(("Fuentes: Riot Games (@VALORANT, 27/04/2022) · Valorant Wiki · NME · Dexerto", "Clip original: Zelch Kyli Jhin (2020) · Q.E.P.D. Lance \"Finest\" Arcilla")):
        p = prog(t, 2 + j * .2, 2.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 960 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L1", "L3", "L5", "L7", "L8", "L9"}
SN.PURPLE_SC = PURPLE_SC
KICK = {f"L{i}": " " for i in range(N)}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, 3.5, wt(0, "historia"), wt(1, "rogaba"), wt(2, "no"), wt(2, "Sage"), wt(3, "meme"), wt(4, "actores"), wt(5, "grafiti"), wt(6, "Jett")])
    return HITS
def frame(T):
    name = [n for n in ORDER if T >= SEG[n]][-1]; idx = ORDER.index(name); img = scene(name, T); dc = T - SEG[name]
    nxt = SEG[ORDER[idx + 1]] if idx + 1 < len(ORDER) else DUR
    img = scale_about(img, 1 + .035 * clamp01(dc / max(1, nxt - SEG[name])), bg=WHITE + (255,)); SN.kicker(img, name, dc)
    particles(img, T + idx * 7, WHITE if name in PURPLE_SC else LIL, .3)
    if idx % 2 == 0: brackets(img, dc, WHITE if name in PURPLE_SC else PUR, .8)
    paste(img, text_layer("@DuplexDragon_", SANS(600, 18), WHITE if name in PURPLE_SC else PUR), 40, 175, .7, "lm")
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
        ("impact", wt(2, "no"), .5), ("shimmer", wt(2, "Sage"), .5), ("typing", SEG["L3"] + .3, .35), ("boom", wt(3, "meme"), .45), ("pop", wt(5, "grafiti"), .5),
        ("pop", wt(6, "Jett"), .5), ("pop", wt(6, "enseñar"), .5), ("shimmer", wt(8, "título"), .4), ("pop", wx(N - 1, "Finest"), .5)]
    ev = [e for e in ev if e[1] < SEG["L7"] - .3 or e[0] in ("shimmer", "pop")]           # parte emotiva sin golpes fuertes
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    o = subprocess.run(["ffmpeg", "-v", "error", "-t", "3.4", "-i", os.path.join(PD, "clips", "tk1.mp4"), "-vn", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
    og = np.frombuffer(o, np.int16).reshape(-1, 2).astype(np.float32) / 32768; og = og / max(1e-3, np.abs(og).max()) * .9; vox[:len(og)] += og[:Ns]   # su voz original
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(PD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(PD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(PD, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume='if(lt(t,3.4),0.12,if(lt(t,{SEG["L7"]}),0.32,0.16))':eval=frame[m];"
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
