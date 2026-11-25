#!/usr/bin/env python3
"""Leviatán 2027: erde y lukxo (según reportes) — pedido en comentarios.
Fuentes: @LeviatanGG (13 nov 2026), Sheep Esports, THESPIKE Brasil, Strafe."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "lev"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3; T1 = os.path.join(PD, "clips", "kingg.mp4")

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
LD = os.path.join(HERE, "..", "loud")
def cutx(path, w, fade=.14):
    im = duo(Image.open(path).convert("RGBA"), 1.08); im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
    im = S.fade_bottom(im, fade); return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
ERDE = cutx(os.path.join(LD, "rec", "erde.png"), 300); ERDE_B = cutx(os.path.join(LD, "rec", "erde.png"), 340)
LUK = cutx(os.path.join(RC, "p124.png"), 300)
TRIO = [cutx(os.path.join(RC, n + ".png"), 220) for n in ("p122", "p123", "p125")]
NEON_ART = Image.open(os.path.join(PD, "fotos", "neon_agente.jpg")).convert("RGBA").resize((240, 240))
_m = Image.new("L", (240, 240), 0); ImageDraw.Draw(_m).ellipse((0, 0, 239, 239), fill=255); NEON_ART.putalpha(_m); NEON_ART = duo(NEON_ART, 1.05)
def logo_a(path, h, col=PUR):
    im = Image.open(path).convert("RGBA"); o = Image.new("RGBA", im.size, col + (255,)); o.putalpha(im.getchannel("A")); o = o.crop(o.getbbox())
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)
MIBR_P = logo_a(os.path.join(PD, "logos", "mibr.webp"), 80)
LEV_P = logo_a(os.path.join(PD, "logos", "leviatan.png"), 170); LEV_W = logo_a(os.path.join(PD, "logos", "leviatan.png"), 150, WHITE)
G2_P = logo_a(os.path.join(PD, "logos", "g2.webp"), 80)
VIT_P = logo_a(os.path.join(HERE, "..", "vit", "logos", "vitality.webp"), 70)
def card(img, w, pad=22):
    im = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS); c = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, fill=255)
    c.paste(WHITE + (255,), (0, 0, c.width, c.height)); c.alpha_composite(im, (pad, pad)); c.putalpha(m)
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, outline=PUR + (255,), width=5); return shadow(c, 14, 14, .35)
COMM_C = card(Image.open(os.path.join(PD, "fotos", "comentario.png")).convert("RGBA"), 600)
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


def vbg(t0, dur, t, a=.5):
    return Image.blend(clip(T1, t0, dur, (0, 0, 1080, 1560), (720, 1280), t), canvas(PUR + (255,)), a)
def vbgx(name, t0, dur, t, a=.5):
    return Image.blend(clip(os.path.join(PD, "clips", name + ".mp4"), t0, dur, (0, 0, 1080, 1920), (720, 1280), t), canvas(PUR + (255,)), a)
def nchip(txt, col=PUR, fg=WHITE, size=40): return SN.namechip(txt, col, fg, size)

def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # comentario
        im = bg("w", "PEDIDO"); stripes(im, T, 0, PUR, .5); ring(im, 360, 640, 330, T * 1.5, PUR, .35)
        word(im, "me lo pidieron en los", IT(900, 52), 360, 150, T, .05, INK); slam(im, "COMENTARIOS", ANTON(110), 360, 250, T, .2, PUR)
        p = ease_back(prog(T, .35, .7), 1.4); paste(im, COMM_C, 360, SY(520) + 60 * (1 - p) + bob(T) * .4, clamp01(p))
        tl = wt(0, "Leviatán") - .3
        if T > tl: pop(im, shadow(LEV_P, 10, 10, .25), 360, 760, T, tl, .4)
        return im
    if name == "L1":     # gancho
        im = vbg(44.0, 6.0, t * .8, .55); stripes(im, T, SEG[name], WHITE); ring(im, 360, 980, 320, T * 1.5, LILL, .45)
        slam(im, "MIBR OFRECIÓ MÁS", ANTON(90), 360, 175, T, SEG[name] + .05, WHITE)
        te = wt(1, "eligieron") - .3
        if T > te: stamp(im, "Y ELIGIERON LEVIATÁN", 360, 290, T, te, (255, 255, 255), -5, 60)
        p = eo(clamp01(t / .45)); paste(im, ERDE, 230, SY(1290) - ERDE.height / 2 + 90 + 140 * (1 - p), p); paste(im, LUK, 490, SY(1290) - LUK.height / 2 + 90 + 140 * (1 - p), p)
        return im
    if name == "L2":     # motivacional
        im = bg("w", "JUNTOS"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "hay cosas que", IT(400, 56), 360, 160, T, SEG[name] + .05, INK); slam(im, "NO SE COMPRAN", ANTON(120), 360, 290, T, wt(2, "compran") - .2, PUR)
        tj = wt(2, "ganas") - .3
        if T > tj: ribbon(im, "LAS GANAS DE JUGAR JUNTOS", 360, 570, T, tj, WHITE, PUR, 50, "mm")
        ring(im, 360, 780, 200, T * 1.4, PUR, .4); ring(im, 360, 780, 160, -T * 1.6, LIL, .35, 3, 22); return im
    if name == "L3":     # Masters Londres
        im = vbg(48.0, 6.0, t * .6, .55); stripes(im, T, SEG[name], WHITE)
        ribbon(im, "CAMPEÓN MASTERS LONDRES 2026", 360, 150, T, SEG[name] + .05, WHITE, PUR, 46, "mm"); confetti(im, T, SEG[name] + .2)
        tt = wt(3, "tres") - .2
        if T > tt:
            counter(im, T, tt, tt + .4, 0, 3, ANTON(160), 250, 300, WHITE); slam(im, "–", ANTON(160), 360, 300, T, tt, WHITE)
            counter(im, T, tt, tt + .5, 0, 2, ANTON(160), 470, 300, WHITE); word(im, "vs Paper Rex", IT(900, 46), 360, 560, T, tt + .3, WHITE)
        tc = wt(3, "Champions") - .3
        if T > tc: pop(im, chipx("CHAMPIONS 2026", False, 500), 360, 860, T, tc, .3)
        return im
    if name == "L4":     # kiNgg
        im = bg("w", "KINGG"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        word(im, "13 de noviembre", IT(900, 52), 360, 140, T, SEG[name] + .05, INK)
        tk = wt(4, "kiNgg") - .2
        if T > tk: pop(im, chipx("KINGG", False, 420), 360, 270, T, tk, .3); word(im, "5 años como capitán", IT(900, 44), 360, 480, T, tk + .2, PUR)
        tr = wt(4, "reportes") - .3
        if T > tr: pop(im, nchip("SEGÚN REPORTES", INK, WHITE, 36), 360, 580, T, tr, .3)
        tg = wt(4, "G2") - .4
        if T > tg: word(im, "kiNgg y Sato a", IT(900, 46), 360, 680, T, tg, INK); pop(im, G2_P, 360, 790, T, tg + .1, .35)
        return im
    if name == "L5":     # llegan erde y lukxo
        im = bg("w", "ERDE"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 600, 300, T * 1.5, PUR, .4)
        word(im, "¿y quién llega?", IT(900, 56), 360, 130, T, SEG[name] + .05, INK)
        tr = wt(5, "reportes") - .3
        if T > tr: pop(im, nchip("SEGÚN REPORTES", INK, WHITE, 36), 360, 230, T, tr, .3)
        for k, (img, nm, key) in enumerate(((ERDE, "ERDE", "erde"), (LUK, "LUKXO", "lukxo"))):
            t0 = wt(5, key) - .2
            if T > t0:
                p = eo(prog(T, t0, t0 + .4)); x = 220 + k * 280
                paste(im, img, x, SY(560) + 60 * (1 - p) + bob(T, k), p); paste(im, nchip(nm, PUR, WHITE, 40), x, SY(560) + img.height / 2 + 10, p)
        tc = wt(5, "campeones") - .3
        if T > tc: ribbon(im, "CAMPEONES DEL MUNDO CON LOUD", 360, 890, T, tc, WHITE, PUR, 44, "mm"); confetti(im, T, tc + .1)
        return im
    if name == "L6":     # erde vuelve a casa
        im = bg("w", "CASA"); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "ERDE", ANTON(130), 360, 150, T, SEG[name] + .05, PUR)
        tm = wt(6, "MVP") - .2
        if T > tm: pop(im, nchip("MVP DE CHAMPIONS · 18 AÑOS", INK, WHITE, 38), 360, 270, T, tm, .3)
        p = eo(prog(T, SEG[name] + .2, SEG[name] + .6)); paste(im, ERDE_B, 360, SY(700) + 60 * (1 - p) + bob(T), p)
        tc = wt(6, "casa") - .3
        if T > tc: stamp(im, "VUELVE A CASA", 360, 890, T, tc, PUR, -5, 72)
        return im
    if name == "L7":     # MIBR ofreció más
        im = bg("w", "DINERO"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        pop(im, nchip("SEGÚN THESPIKE BRASIL", INK, WHITE, 36), 360, 140, T, SEG[name] + .05, .3)
        tm = wt(7, "MIBR") - .2
        if T > tm: pop(im, MIBR_P, 360, 290, T, tm, .35); word(im, "ofreció más dinero", IT(900, 48), 360, 500, T, tm + .2, INK)
        tl = wt(7, "Leviatán") - .5
        if T > tl: stamp(im, "PREFIRIERON JUGAR JUNTOS", 360, 640, T, tl, (200, 30, 60), -5, 52); pop(im, LEV_P, 360, 820, T, tl + .2, .35)
        return im
    if name == "L8":     # se quedan
        im = vbg(20.0, 6.0, t * .7, .6); stripes(im, T, SEG[name], WHITE)
        word(im, "se quedan", IT(900, 56), 360, 130, T, SEG[name] + .05, WHITE)
        pop(im, nchip("NEON · BLOWZ · SPIKEZIN", WHITE, PUR, 46), 360, 240, T, SEG[name] + .25, .3)
        tn = wt(8, "MVP") - .3
        if T > tn: ribbon(im, "NEON: MVP DE MASTERS LONDRES", 360, 340, T, tn, PUR, WHITE, 42, "mm")
        pa = eo(prog(T, SEG[name] + .3, SEG[name] + .7)); paste(im, NEON_ART, 360, SY(600) + bob(T, 3), pa * .9)    # guiño: agente delante del texto
        for k, img in enumerate(TRIO):
            p = eo(prog(T, SEG[name] + .4 + k * .15, SEG[name] + .8 + k * .15)); paste(im, img, 140 + k * 220, SY(840) + 60 * (1 - p) + bob(T, k), p)
        return im
    if name == "L9":     # China / revancha
        im = bg("w", "CHINA"); stripes(im, T, SEG[name], PUR, .5)
        ribbon(im, "DICIEMBRE · XIAMEN, CHINA", 360, 140, T, SEG[name] + .05, WHITE, PUR, 50, "mm")
        word(im, "Radiant International Invitational", IT(900, 36), 360, 230, T, SEG[name] + .3, INK)
        tv = wt(9, "Vitality") - .2
        if T > tv: pop(im, LEV_P.resize((int(LEV_P.width * .7), int(LEV_P.height * .7))), 220, 430, T, tv, .35); word(im, "VS", ANTON(60), 360, 430, T, tv + .1, PUR); pop(im, VIT_P, 520, 430, T, tv + .15, .35)
        tf = wt(9, "final") - .3
        if T > tf: stamp(im, "LA REVANCHA DE LA FINAL", 360, 640, T, tf, (200, 30, 60), -5, 56)
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "LEV")
    word(im, "¿Este Leviatán puede ser", IT(400, 52), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "CAMPEÓN DEL MUNDO?", ANTON(92), 360, 260, T, SEG[f"L{k}"] + .3, PUR)
    tc = wt(k, "comentarios") - .1
    if T > tc: pop(im, U.COMMENT, 160, 470 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 160, 555, T, tc + .05, PUR)
    pop(im, LEV_P, 450, 500, T, SEG[f"L{k}"] + .4, .35)
    for j, s_ in enumerate(("Fuentes: @LeviatanGG · Sheep Esports · THESPIKE Brasil · Strafe · nov 2026", "Clip: despedida oficial de kiNgg (Leviatán) · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L1", "L3", "L8"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "PEDIDO", "L1": "LEV", "L2": "JUNTOS", "L3": "LONDRES", "L4": "KINGG", "L5": "ERDE", "L6": "CASA", "L7": "MIBR", "L8": "NEON", "L9": "CHINA", f"L{N-1}": "LEV"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.2, wt(0, "Leviatán"), SEG["L1"] + .05, wt(1, "eligieron"), wt(2, "compran"), SEG["L3"] + .05, wt(3, "tres"), wt(3, "Champions"), wt(4, "kiNgg"), wt(4, "G2"), wt(5, "erde"), wt(5, "lukxo"), wt(6, "casa"), wt(7, "MIBR"), wt(7, "Leviatán"), SEG["L8"] + .1, wt(9, "final")])
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
    ev = [("braam", 0.0, .6), ("pop", .4, .6), ("pop", wt(0, "Leviatán"), .5)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("braam", SEG["L1"] + .05, .7), ("shimmer", SEG["L3"] + .1, .6), ("cheer", SEG["L3"] + .1, .35), ("typing", wt(3, "tres") - .2, .4), ("impact", wt(3, "Champions"), .5),
        ("impact", wt(4, "kiNgg"), .5), ("pop", wt(4, "reportes"), .5), ("pop", wt(4, "G2"), .5), ("pop", wt(5, "erde"), .5), ("pop", wt(5, "lukxo"), .5), ("shimmer", wt(5, "campeones"), .5),
        ("pop", wt(6, "MVP"), .5), ("clink", wt(6, "casa"), .5), ("pop", wt(7, "MIBR"), .5), ("braam", wt(7, "Leviatán"), .5), ("pop", SEG["L8"] + .25, .5), ("riser", SEG["L9"] - 1.0, .4),
        ("impact", wt(9, "final"), .6), ("pop", wt(k, "comentarios"), .6)]
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(PD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(PD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(PD, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.2[m];"
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
