#!/usr/bin/env python3
"""Vitality ficha a jawgemo tras perder la final de Champions — motion graphics morado.
Voz: Andrés (eleven_v4, 1.1x). Fuentes: @TeamVitalityVAL (10-11 nov 2026), Sheep Esports (18-19 nov), Strafe, Inven Global.
Uso: python3 render_prx.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "vit"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3; T1 = os.path.join(PD, "clips", "eg2023.mp4")

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
JAW = cut("jawgemo", 520); JAW_S = cut("jawgemo", 360)
LD = os.path.join(HERE, "..", "loud")
ERDE = S.duo(Image.open(os.path.join(LD, "rec", "erde.png")).convert("RGBA"), 1.08); ERDE = S.fade_bottom(ERDE.resize((240, int(ERDE.height * 240 / ERDE.width)), Image.LANCZOS), .18)
def logo_mask(path, h, col=PUR):
    im = Image.open(path).convert("RGBA"); a = np.asarray(im).astype(float); m = np.clip((255 * 3 - a[..., :3].sum(2) - 60) * 2, 0, 255) * (a[..., 3] / 255)
    o = Image.new("RGBA", im.size, col + (255,)); o.putalpha(Image.fromarray(m.astype(np.uint8))); o = o.crop(o.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)
def logo_a(path, h, col=PUR):
    im = Image.open(path).convert("RGBA"); o = Image.new("RGBA", im.size, col + (255,)); o.putalpha(im.getchannel("A")); o = o.crop(o.getbbox())
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)
VIT_P = logo_a(os.path.join(PD, "logos", "vitality.webp"), 120); VIT_W = logo_a(os.path.join(PD, "logos", "vitality.webp"), 70, WHITE)
AUR_P = logo_a(os.path.join(PD, "logos", "aurora.webp"), 100); LOUD_W = logo_a(os.path.join(LD, "logos", "loud_p.png"), 90, WHITE)
NEON = S.AGC["neon"]; NEON_B = S._agcrop("neon", 500)
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
    return Image.blend(clip(T1, t0, dur, (0, 0, 1080, 1920), (720, 1280), t), canvas(PUR + (255,)), a)
def vbgx(name, t0, dur, t, a=.5):
    return Image.blend(clip(os.path.join(PD, "clips", name + ".mp4"), t0, dur, (0, 0, 1080, 1920), (720, 1280), t), canvas(PUR + (255,)), a)
def nchip(txt, col=PUR, fg=WHITE, size=40): return SN.namechip(txt, col, fg, size)

def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # gancho
        im = vbg(18.0, 6.0, t * .9, .55); stripes(im, T, 0, WHITE); ring(im, 360, 980, 320, T * 1.5, LILL, .45)
        paste(im, JAW, 360, SY(1290) - JAW.height / 2 + 90 + 140 * (1 - eo(clamp01(t / .45))), clamp01(t * 5))
        slam(im, "PERDIERON LA FINAL", ANTON(84), 360, 175, T, .1, WHITE)
        tf = wt(0, "ficharon") - .2
        if T > tf: stamp(im, "Y FICHARON A UN CAMPEÓN", 360, 290, T, tf, (255, 255, 255), -5, 56)
        particles(im, T, WHITE, .45); return im
    if name == "L1":     # motivacional
        im = bg("w", "PIEZA"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "cuando te quedas a un", IT(400, 52), 360, 160, T, SEG[name] + .05, INK); slam(im, "PASO", ANTON(160), 360, 280, T, wt(1, "paso") - .15, PUR)
        tp = wt(1, "pieza") - .25
        if T > tp: ribbon(im, "CAMBIAS LA PIEZA QUE FALTA", 360, 560, T, tp, WHITE, PUR, 54, "mm")
        ring(im, 360, 780, 200, T * 1.4, PUR, .4); ring(im, 360, 780, 160, -T * 1.6, LIL, .35, 3, 22); return im
    if name == "L2":     # final Champions
        im = vbgx("neon_reac", 40.0, 4.0, t * .7, .62); stripes(im, T, SEG[name], WHITE)
        ribbon(im, "FINAL CHAMPIONS SHANGHÁI", 360, 150, T, SEG[name] + .05, WHITE, PUR, 50, "mm")
        pop(im, VIT_W, 220, 320, T, SEG[name] + .2, .35); word(im, "VS", ANTON(50), 420, 320, T, SEG[name] + .3, WHITE); pop(im, LOUD_W, 540, 320, T, SEG[name] + .35, .35)
        tl = wt(2, "tres") - .2
        if T > tl:
            counter(im, T, tl, tl + .4, 0, 1, ANTON(170), 250, 560, WHITE); slam(im, "–", ANTON(170), 360, 560, T, tl, WHITE)
            counter(im, T, tl, tl + .5, 0, 3, ANTON(170), 470, 560, WHITE); word(im, "ganó LOUD", IT(900, 46), 360, 700, T, tl + .3, WHITE)
        ts = wt(2, "subcampeón") - .2
        if T > ts: stamp(im, "SUBCAMPEONES", 360, 830, T, ts, (255, 255, 255), -6, 70)
        return im
    if name == "L3":     # Derke
        im = bg("w", "DERKE"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 250, T * 1.5, PUR, .4)
        word(im, "seis días después", IT(900, 52), 360, 140, T, SEG[name] + .05, INK)
        td = wt(3, "Derke") - .15
        if T > td: pop(im, chipx("DERKE", False, 420), 360, 270, T, td, .3)
        tt = wt(3, "trofeo") - .25
        if T > tt: pop(im, chipx("SU PRIMER TROFEO VCT", True, 520, PUR), 360, 530, T, tt, .3)
        ta = wt(3, "Aurora") - .2
        if T > ta: word(im, "hoy juega en", IT(900, 44), 360, 670, T, ta, INK); pop(im, AUR_P, 360, 790, T, ta + .1, .35)
        return im
    if name == "L4":     # llega jawgemo
        im = vbg(36.0, 3.0, t * .5, .55); stripes(im, T, SEG[name], WHITE)
        slam(im, "11 DE NOVIEMBRE", ANTON(70), 360, 140, T, SEG[name] + .05, WHITE)
        tj = wt(4, "jawgemo") - .2
        if T > tj:
            slam(im, "JAWGEMO", ANTON(100), 360, 270, T, tj, WHITE)
            p = eo(prog(T, tj, tj + .4)); paste(im, JAW_S, 360, SY(730) + 80 * (1 - p) + bob(T), p)
        tc = wt(4, "campeón") - .2
        if T > tc: ribbon(im, "CAMPEÓN DEL MUNDO 2023 · EG", 360, 900, T, tc, PUR, WHITE, 46, "mm"); confetti(im, T, tc + .1)
        return im
    if name == "L5":     # G2: 4 títulos, 0 internacionales
        im = bg("w", "G2"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 400, 150, T * 1.8, PUR, .35)
        word(im, "con G2 ganó", IT(900, 52), 360, 130, T, SEG[name] + .05, INK)
        counter(im, T, SEG[name] + .3, wt(5, "títulos"), 0, 4, ANTON(190), 360, 290, PUR)
        if T > wt(5, "títulos") - .2: word(im, "TÍTULOS DE AMÉRICAS", ANTON(64), 360, 540, T, wt(5, "títulos") - .2, INK)
        ti = wt(5, "ningún") - .2
        if T > ti: pop(im, chipx("0 TÍTULOS INTERNACIONALES", False, 580), 360, 690, T, ti, .3)
        return im
    if name == "L6":     # Neon
        im = vbgx("neon", 2.0, 6.0, t * .9, .55); stripes(im, T, SEG[name], WHITE)
        word(im, "hay un detalle", IT(900, 46), 360, 110, T, SEG[name] + .05, WHITE)
        tn = wt(6, "Neon") - .2; td = wt(6, "Derke") - .2
        if T > tn: slam(im, "NEON", ANTON(130), 360, 215, T, tn, WHITE)
        if T > td: ribbon(im, "DERKE CASI NO LA USABA", 360, 330, T, td, PUR, WHITE, 46, "mm")
        if T > tn: pop(im, shadow(NEON_B, 12, 12, .35), 360, 700, T, tn, .4)     # la agente SIEMPRE delante de los textos
        return im
    if name == "L7":     # coaches
        im = bg("w", "COACH"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        word(im, "también cambió el banquillo", IT(900, 46), 360, 140, T, SEG[name] + .05, INK)
        tp = wt(7, "PAL") - .15
        if T > tp: pop(im, chipx("PAL", False, 360), 360, 290, T, tp, .3)
        ts = wt(7, "Scuttt") - .15
        if T > ts: slam(im, "SCUTTT", ANTON(150), 360, 560, T, ts, PUR); pop(im, nchip("ENTRENADOR PRINCIPAL", INK, WHITE, 40), 360, 690, T, ts + .2, .3)
        tv = wt(7, "primera") - .2
        if T > tv: stamp(im, "POR PRIMERA VEZ", 360, 820, T, tv, PUR, -5, 70)
        return im
    if name == "L8":     # diciembre, China, Leviatán
        im = bg("w", "CHINA"); stripes(im, T, SEG[name], PUR, .5)
        ribbon(im, "DICIEMBRE · XIAMEN, CHINA", 360, 140, T, SEG[name] + .05, WHITE, PUR, 50, "mm")
        word(im, "Radiant International Invitational", IT(900, 36), 360, 215, T, SEG[name] + .3, INK)
        tr = wt(8, "reportes") - .3
        if T > tr: pop(im, nchip("SEGÚN REPORTES", INK, WHITE, 36), 360, 290, T, tr, .3)
        tl = wt(8, "Leviatán") - .2
        if T > tl:
            p = eo(prog(T, tl, tl + .4)); paste(im, ERDE, 360, SY(620) + 60 * (1 - p) + bob(T), p)
            pop(im, nchip("LEVIATÁN · ERDE Y LUKXO", PUR, WHITE, 40), 360, 830, T, tl + .2, .3)
        tg = wt(8, "ganaron") - .3
        if T > tg: stamp(im, "LOS QUE LES GANARON LA FINAL", 360, 900, T, tg, (200, 30, 60), -4, 40)
        return im
    if name == "L9":     # roster
        im = bg("w", "VIT"); ring(im, 360, 640, 340, T * 1.4, PUR, .35)
        pop(im, VIT_P, 360, 160, T, SEG[name] + .05, .35); word(im, "roster 2027", IT(900, 40), 360, 280, T, SEG[name] + .2, INK)
        rows = (("CHRONICLE", "Chronicle", "SIGUE"), ("JAMPPI", "Jamppi", "SIGUE"), ("PROFEK", "PROFEK", "SIGUE"), ("SAYONARA", "Sayonara", "SIGUE"), ("JAWGEMO", "jawgemo", "NUEVO"))
        for k, (tx, key, tag) in enumerate(rows):
            t0 = wt(9, key) - .15; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0:
                paste(im, nchip(tx, PUR if tag == "NUEVO" else INK, WHITE, 44), lerp(-300, 290, p), SY(370) + k * 92, clamp01(p))
                paste(im, nchip(tag, LIL if tag == "NUEVO" else LILL, INK, 28), lerp(1000, 530, p), SY(370) + k * 92, clamp01(p))
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "VIT")
    word(im, "¿Con jawgemo, Vitality por fin gana", IT(400, 46), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "UN INTERNACIONAL?", ANTON(92), 360, 260, T, SEG[f"L{k}"] + .3, PUR)
    tc = wt(k, "comentarios") - .1
    if T > tc: pop(im, U.COMMENT, 160, 470 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 160, 555, T, tc + .05, PUR)
    jj = JAW_S.resize((260, int(JAW_S.height * 260 / JAW_S.width))); paste(im, jj, 360, SY(700) + 6 * math.sin(T * 2), clamp01((t - .2) * 3))
    for j, s_ in enumerate(("Fuentes: @TeamVitalityVAL · Sheep Esports · Strafe · Inven Global · nov 2026", "Clips: VCT Champions 2023 / jawgemo Neon · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L4", "L6"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "VITALITY", "L1": "PIEZA", "L2": "3–1", "L3": "DERKE", "L4": "JAWGEMO", "L5": "G2", "L6": "NEON", "L7": "SCUTTT", "L8": "CHINA", "L9": "2027", f"L{N-1}": "VIT"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, wt(0, "ficharon"), SEG["L1"] + .1, wt(1, "pieza"), SEG["L2"] + .05, wt(2, "tres"), wt(3, "Derke"), wt(3, "Aurora"), wt(4, "jawgemo"), wt(5, "ningún"), wt(6, "Neon"), wt(7, "PAL"), wt(7, "Scuttt"), wt(8, "ganaron"), SEG["L9"] + .05])
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
    ev = [("braam", 0.0, .7), ("hit808", 0.0, .6), ("pop", wt(0, "ficharon"), .5)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("pop", SEG["L2"] + .2, .5), ("pop", SEG["L2"] + .35, .5), ("typing", wt(2, "tres") - .2, .4), ("impact", wt(2, "subcampeón"), .5),
        ("impact", wt(3, "Derke"), .5), ("shimmer", wt(3, "trofeo"), .5), ("pop", wt(3, "Aurora"), .5), ("braam", wt(4, "jawgemo"), .6), ("shimmer", wt(4, "campeón"), .5),
        ("cheer", wt(4, "campeón"), .35), ("typing", SEG["L5"] + .3, .4), ("impact", wt(5, "ningún"), .5), ("pop", wt(6, "Neon"), .6), ("impact", wt(7, "PAL"), .5),
        ("braam", wt(7, "Scuttt"), .5), ("pop", wt(8, "reportes"), .5), ("pop", wt(8, "Leviatán"), .5), ("clink", wt(8, "ganaron"), .5),
        ("pop", wt(9, "Chronicle"), .5), ("pop", wt(9, "Jamppi"), .5), ("pop", wt(9, "PROFEK"), .5), ("pop", wt(9, "Sayonara"), .5), ("boom", wt(9, "jawgemo"), .5), ("pop", wt(k, "comentarios"), .6)]
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
