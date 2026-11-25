#!/usr/bin/env python3
"""Cómo usar a Hush (Valorant, patch 13.09) — motion graphics morado con jugadas reales.
Fuentes: Riot Games, Liquipedia, Valorant Wiki, Beebom, Dot Esports (oct-nov 2026)."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "hush"); FPS = 30
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

ART = os.path.join(PD, "arte")
def ld(n): im = Image.open(os.path.join(ART, n)).convert("RGBA"); return im.crop(im.getchannel("A").getbbox())
HUSH = ld("fullportrait.png"); HICON = ld("icon.png")
HAB = {k: ld(f"hab_{v}.png") for k, v in (("F", "passive"), ("C", "grenade"), ("Q", "ability1"), ("E", "ability2"), ("X", "ultimate"))}
HNAME = {"F": "TELEQUINESIS", "C": "ÁNCORA", "Q": "ORBE FLASH", "E": "CINESTESIA", "X": "SUSPENSIÓN"}
ORB_ICONS = [HAB[k] for k in "QECXFQEC"]
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
CAL_OCT = [calcard("2026", "OCTUBRE", "18"), calcard("2026", "OCTUBRE", "22"), calcard("2026", "OCTUBRE", "27")]
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
CR = {"of": (0, 496, 720, 408), "tk1": (0, 400, 720, 880), "tk2": (0, 181, 576, 662), "tk3": (0, 340, 1080, 1228), "tk4": (0, 320, 576, 704), "tk5": (0, 373, 576, 331)}
_SC = {}
SECT = {"of": [(4.0, 10.6), (11.0, 22.8), (23.0, 27.9), (28.0, 34.9), (35.0, 42.6)]}   # secciones del video oficial (una por habilidad)
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
def scene(name, T):
    t = T - SEG[name]
    if name == "L0":                                  # gancho: Hush grande → la más difícil (TenZ) → así se usa
        tB, tC = wt(0, "más") - .1, wt(0, "así") - .1
        if T < tB:
            im = pur(T, name); slam(im, "HUSH", ANTON(170), 360, 170, T, .05, WHITE)
            pu = ease_back(prog(T, .1, .5), 1.2); hs = sc(HUSH, 340)
            orb(im, hs, 360, lerp(1500, 1240, pu) + 8 * math.sin(T * 2), T, max(0, T - .2), clamp01(pu), 70)
        elif T < tC:
            im = bg("w", "HUSH"); ring(im, 360, 600, 260, T * 1.5, PUR, .4)
            slam(im, "LA DUELISTA MÁS DIFÍCIL", ANTON(84), 360, 160, T, tB, PUR)
            clipin(im, "tk5", 49.0, T, tB + .05, (600, 344), 600)
            label(im, "TENZ · RANKED · BIND", T, tB + .2, False, 860)
        else:
            im = pur(T, name); slam(im, "ASÍ SE USA", ANTON(130), 360, 180, T, tC, WHITE)
            for k, key in enumerate("CQEXF"):
                habfly(im, T, tC + .05 + k * .08, key, 120 + k * 120, 620, 104, True)
            pop(im, nchip("GUÍA RÁPIDA · 5 HABILIDADES", WHITE, PUR, 32), 360, 820, T, tC + .3, .3)
        return flash(im, T, (tB, tC))
    if name == "L1":
        im = bg("w", "CHINA"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "viene de", IT(900, 52), 360, 140, T, SEG[name] + .05, INK); slam(im, "GUANGDONG, CHINA", ANTON(96), 360, 245, T, wt(1, "Guangdong") - .15, PUR)
        tq = wt(1, "telequinesis") - .2
        pu = ease_back(prog(T, SEG[name] + .1, SEG[name] + .5), 1.2); hs = sc(HUSH, 360)
        paste(im, hs, 360, 1330 - hs.height / 2 + 40 * (1 - pu) + 6 * math.sin(T * 2), clamp01(pu * 2))
        if T > tq: stamp(im, "TELEQUINESIS", 360, 510, T, tq, PUR, -4, 72)
        return im
    if name == "L2":
        im = pur(T, name); habhead(im, T, SEG[name] + .05, "F", True)
        synclip(im, "of", 5.6, wx(2, "presiona"), T, SEG[name] + .15, (600, 340), 600, 4.0)
        steps(im, T, [("M", wx(2, "apunta")), ("F", wx(2, "F"))], 880, True)
        return im
    if name == "L3":
        im = bg("w", "DASH"); stripes(im, T, SEG[name], PUR, .5); habhead(im, T, SEG[name] + .05, "C", False)
        synclip(im, "of", 28.3, wx(3, "salta"), T, SEG[name] + .15, (600, 340), 600, 6.0)
        steps(im, T, [("SALTO", wx(3, "salta")), ("M", wx(3, "apunta")), ("C", wx(3, "C", 1))], 880, False)
        return im
    if name == "L4":
        im = pur(T, name); habhead(im, T, SEG[name] + .05, "Q", True)
        synclip(im, "of", 23.6, wx(4, "clic"), T, SEG[name] + .15, (600, 340), 600, 4.0)
        steps(im, T, [("Q", wx(4, "Q", 1)), ("L", wx(4, "clic")), ("Q", wx(4, "Q", 2))], 880, True)
        return im
    if name == "L5":
        im = bg("w", "PULL"); stripes(im, T, SEG[name], PUR, .5); habhead(im, T, SEG[name] + .05, "E", False)
        synclip(im, "of", 13.0, wx(5, "lánzala"), T, SEG[name] + .15, (600, 340), 600, 9.0)
        ta = wx(5, "Atrae") - .2
        if T < ta: steps(im, T, [("E", wx(5, "E", 1)), ("L", wx(5, "clic")), ("R", wx(5, "clic", 1)), ("E", wx(5, "E", 2))], 880, False)
        else: label(im, "PARED = ATURDIDO" if T > wx(5, "pared") - .2 else "ATRAE A TODOS AL CENTRO", T, ta, False, 1080)
        return im
    if name == "L6":
        im = pur(T, name); habhead(im, T, SEG[name] + .05, "X", True)
        synclip(im, "of", 35.2, wx(6, "presiona"), T, SEG[name] + .15, (600, 340), 600, 7.0)
        tt = wx(6, "Todos") - .2
        if T < tt: steps(im, T, [("X", wx(6, "X", 1)), ("L", wx(6, "clic")), ("M", wx(6, "guíala")), ("X", wx(6, "X", 2))], 880, True)
        else: stamp(im, "TODOS LEVITANDO", 360, 1100, T, tt, (255, 255, 255), -4, 70)
        return im
    if name == "L7":
        im = bg("w", "TRUCO"); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "TRUCO 1", ANTON(130), 360, 160, T, SEG[name] + .05, PUR)
        synclip(im, "tk5", 7.0, wx(7, "flash"), T, SEG[name] + .15, (600, 344), 560, 5.0)
        label(im, "TENZ · ENTRY", T, SEG[name] + .4, False, 790)
        steps(im, T, [("Q", wx(7, "flash")), ("R", wx(7, "clic")), ("C", wx(7, "C"))], 900, False)
        return im
    if name == "L8":
        im = pur(T, name); slam(im, "TRUCO 2", ANTON(130), 360, 160, T, SEG[name] + .05, WHITE)
        synclip(im, "tk3", 40.0, wt(8, "Cinestesia"), T, SEG[name] + .15, (380, 434), 690, 2.5)
        tp = wt(8, "pared") - .2
        habfly(im, T, wt(8, "Cinestesia") - .2, "E", 590, 420, 92, True)
        if T > tp: label(im, "CINESTESIA + PARED = STUN", T, tp, True, 1140)
        return im
    if name == "L9":
        im = bg("w", "27"); stripes(im, T, SEG[name], PUR, .5); ty = wt(9, "ya") - .15
        if T < ty:
            word(im, "salió el", IT(900, 52), 360, 150, T, SEG[name] + .05, INK)
            calflip(im, T, SEG[name] + .1, wt(9, "octubre") + .1, CAL_OCT, 600)
        else:
            slam(im, "Y YA HAY JUGADAS ASÍ", ANTON(84), 360, 150, T, ty, PUR)
            synclip(im, "tk3", 3.0, ty + .4, T, ty, (360, 410), 640, 3.5)
            stamp(im, "ACE", 360, 1170, T, ty + .25, PUR, -6, 84)
        return flash(im, T, (ty,))
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "HUSH")
    word(im, "¿Ya la", IT(400, 56), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "PROBASTE?", ANTON(130), 360, 265, T, wt(k, "probaste") - .15, PUR)
    tc = wt(k, "comentarios") - .1; tsh = wt(k, "compártelo") - .15
    if tc < T < tsh: pop(im, U.COMMENT, 150, 530 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 150, 615, T, tc + .05, PUR)
    if T >= tsh: pop(im, U.SHARE, 150, 530 + math.sin(T * 5) * 10, T, tsh, .35); word(im, "compártelo", IT(900, 38), 150, 615, T, tsh + .05, PUR)
    orb(im, sc(HICON, 200), 480, 800 + 6 * math.sin(T * 2), T, max(0, t - .3), clamp01((t - .3) * 3), 56, PUR, LIL)
    for j, s_ in enumerate(("Fuentes: Riot Games (patch 13.09) · Liquipedia · Valorant Wiki · Beebom · Dot Esports", "Clips: TenZ · pitoexc · TikTok de la comunidad")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L4", "L6", "L8"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": " ", "L1": "CHINA", "L2": " ", "L3": " ", "L4": " ", "L5": " ", "L6": " ", "L7": " ", "L8": " ", "L9": "27", f"L{N-1}": "HUSH"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, wt(0, "más"), wt(0, "así"), wt(1, "telequinesis"), SEG["L2"] + .1, SEG["L3"] + .1, wt(3, "disparada"), SEG["L4"] + .1, wt(4, "mira"), SEG["L5"] + .1, wt(5, "pared"),
                              SEG["L6"] + .1, wt(6, "levitando"), wt(7, "C"), wt(8, "pared"), wt(9, "ya")])
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
        ("shimmer", wt(0, "así"), .4)] + [("pop", SEG[f"L{i}"] + .15, .5) for i in range(2, 7)] + [("swoosh", wt(3, "sales"), .6), ("impact", wt(4, "mira"), .5),
        ("impact", wt(5, "pared"), .5), ("riser", SEG["L6"] - 1.0, .35), ("braam", wt(6, "levitando"), .45), ("pop", wt(7, "flash"), .5), ("pop", wt(7, "C"), .5),
        ("typing", SEG["L9"] + .2, .35), ("boom", wt(9, "ya"), .5), ("cheer", wt(9, "ya") + .2, .3),
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
