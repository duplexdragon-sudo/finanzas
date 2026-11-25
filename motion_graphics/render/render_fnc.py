#!/usr/bin/env python3
"""Fnatic despide a Boaster y se rearma para 2027 — motion graphics morado.
Voz: Andrés (eleven_v4, 1.1x). Fuentes: @FNATIC / @OfficialBoaster (6 nov 2026), Sheep Esports (17 nov), Strafe, RG.org.
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
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "fnc"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3; T1 = os.path.join(PD, "clips", "boaster_baile.mp4")

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
BST = cut("boaster", 560); BST_S = cut("boaster", 380)
def logo_mask(path, h, col=PUR):
    im = Image.open(path).convert("RGBA"); a = np.asarray(im).astype(float); m = np.clip((255 * 3 - a[..., :3].sum(2) - 60) * 2, 0, 255) * (a[..., 3] / 255)
    o = Image.new("RGBA", im.size, col + (255,)); o.putalpha(Image.fromarray(m.astype(np.uint8))); o = o.crop(o.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)
FNC_P = logo_mask(os.path.join(PD, "logos", "fnatic.png"), 170); FNC_W = logo_mask(os.path.join(PD, "logos", "fnatic.png"), 150, WHITE)
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


CM = {n: card(Image.open(os.path.join(PD, "fotos", n + ".png")).convert("RGBA"), 600, 12) for n in ("c_cojo", "c_magnum", "c_desmo")}
CRASH = card(Image.open(os.path.join(PD, "fotos", "tuit_crashies.png")).convert("RGBA"), 470, 12)
def vbg(t0, dur, t, a=.5):
    return Image.blend(clip(T1, t0, dur, (0, 300, 1080, 1620), (720, 1280), t), canvas(PUR + (255,)), a)
P2 = os.path.join(PD, "clips", "boaster_paris.mp4")
def vbg2(t0, dur, t, a=.5):
    return Image.blend(clip(P2, t0, dur, (205, 360, 660, 1170), (720, 1280), t), canvas(PUR + (255,)), a)
def vbgx(name, t0, dur, t, a=.5):
    return Image.blend(clip(os.path.join(PD, "clips", name + ".mp4"), t0, dur, (0, 0, 1080, 1920), (720, 1280), t), canvas(PUR + (255,)), a)
def nchip(txt, col=PUR, fg=WHITE, size=40): return SN.namechip(txt, col, fg, size)

def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # gancho
        im = vbg(5.0, 3.0, t * .8, .55); stripes(im, T, 0, WHITE); ring(im, 360, 980, 320, T * 1.5, LILL, .45)
        paste(im, BST, 360, SY(1290) - BST.height / 2 + 140 * (1 - eo(clamp01(t / .45))), clamp01(t * 5))
        slam(im, "ADIÓS AL CAPITÁN", ANTON(90), 360, 200, T, .1, WHITE)
        tt = wt(0, "trofeos") - .2
        if T > tt: pop(im, chipx("2 TROFEOS INTERNACIONALES", True, 560), 360, 330, T, tt, .3)
        tu = wt(0, "único") - .2
        if T > tu: stamp(im, "Y NO FUE EL ÚNICO", 360, 470, T, tu, (255, 255, 255), -6, 70)
        particles(im, T, WHITE, .45); return im
    if name == "L1":     # motivacional
        im = bg("w", "ERA"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "hasta las eras más", IT(400, 54), 360, 160, T, SEG[name] + .05, INK); slam(im, "GRANDES", ANTON(150), 360, 280, T, wt(1, "grandes") - .15, PUR)
        tf = wt(1, "final") - .15
        if T > tf: ribbon(im, "TIENEN UN FINAL", 360, 440, T, tf, WHITE, PUR, 60, "mm")
        ring(im, 360, 720, 200, T * 1.4, PUR, .4); ring(im, 360, 720, 160, -T * 1.6, LIL, .35, 3, 22); return im
    if name == "L2":     # palmarés
        im = vbgx("tokio", 39.5, 8.0, t * .85, .5); stripes(im, T, SEG[name], WHITE)
        pop(im, FNC_W, 360, 200, T, SEG[name] + .05, .35); word(im, "la voz de Fnatic", IT(900, 50), 360, 330, T, wt(2, "voz") - .1, WHITE)
        for k, (tx, key, ok) in enumerate((("LOCK//IN SÃO PAULO 2023", "LOCK", True), ("MASTERS TOKIO 2023", "Tokio", True), ("SUBCAMPEÓN CHAMPIONS 2025", "subcampeones", True))):
            t0 = wt(2, key) - .2; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0: paste(im, chipx(tx, ok, 580, PUR if k < 2 else INK), lerp(-320, 360, p), SY(450) + k * 118, clamp01(p))
        if T > wt(2, "Tokio"): confetti(im, T, wt(2, "Tokio"))
        return im
    if name == "L3":     # peor año
        im = bg("w", "2026"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 420, 150, T * 1.8, PUR, .35); ring(im, 360, 420, 120, -T * 2, LIL, .3, 3, 22)
        word(im, "2026: su peor año", IT(900, 52), 360, 130, T, SEG[name] + .05, INK)
        counter(im, T, SEG[name] + .3, wt(3, "internacional"), 3, 0, ANTON(190), 360, 290, PUR)
        if T > wt(3, "internacional") - .2: word(im, "INTERNACIONALES", ANTON(66), 360, 500, T, wt(3, "internacional") - .2, INK)
        tp = wt(3, "play-ins") - .2
        if T > tp: pop(im, chipx("FUERA EN PLAY-INS VS CHALLENGERS", False, 590), 360, 640, T, tp, .3)
        tc = wt(3, "Challengers")
        if T > tc: stamp(im, "POR PRIMERA VEZ", 360, 780, T, tc, PUR, -5, 70)
        return im
    if name == "L4":     # salidas
        im = bg("w", "6 NOV"); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "6 DE NOVIEMBRE", ANTON(90), 360, 140, T, SEG[name] + .05, PUR)
        if T < wt(4, "crashies") - .2:
            paste(im, BST_S, 360, SY(560) + bob(T), clamp01(t * 4))
            tb = wt(4, "Boaster") - .1
            if T > tb: stamp(im, "SALE BOASTER", 360, 800, T, tb, (200, 30, 60), -6, 76)
        else:
            tc = wt(4, "crashies") - .2; p = ease_back(prog(T, tc, tc + .35), 1.3); paste(im, CRASH, 360, SY(520) + 40 * (1 - p), clamp01(p))
            tt = wt(4, "TenZ") - .2
            if T > tt: pop(im, nchip("CRASHIES → T1 CON TENZ".replace("→", "A"), PUR, WHITE, 40), 360, 790, T, tt, .3)
            ta = wt(4, "Alfajer") - .15
            if T > ta: pop(im, chipx("ALFAJER", False, 400), 360, 880, T, ta, .3)
        return im
    if name == "L5":     # despedidas
        im = vbgx("mejores", 13.8, 2.4, t * .4, .55); stripes(im, T, SEG[name], WHITE)
        ribbon(im, "“DEFINISTE UNA ERA”", 360, 130, T, SEG[name] + .1, WHITE, PUR, 60, "mm")
        word(im, "— FNATIC", IT(900, 40), 360, 215, T, SEG[name] + .4, WHITE)
        tc = wt(5, "compañero") - .2
        for k, (n, dt) in enumerate((("c_cojo", 0), ("c_magnum", .45), ("c_desmo", .9))):
            p = ease_back(prog(T, tc + dt, tc + dt + .3), 1.4)
            if p > 0: paste(im, CM[n], lerp(1000, 360, p) if k % 2 else lerp(-300, 360, p), SY(480) + k * 165 + bob(T, k) * .3, clamp01(p))
        return im
    if name == "L6":     # valyn
        im = bg("w", "VALYN"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        word(im, "¿y quién llega?", IT(900, 56), 360, 140, T, SEG[name] + .05, INK)
        pop(im, nchip("SEGÚN SHEEP ESPORTS", INK, WHITE, 36), 360, 250, T, wt(6, "Sheep") - .2, .3)
        tv = wt(6, "valyn") - .15
        if T > tv: slam(im, "VALYN", ANTON(170), 360, 470, T, tv, PUR)
        tg = wt(6, "G2") - .15
        if T > tg: pop(im, nchip("LÍDER DE G2", PUR, WHITE, 44), 360, 630, T, tg, .3)
        ti = wt(6, "IGL") - .2
        if T > ti: stamp(im, "NUEVO IGL", 360, 760, T, ti, PUR, -6, 80)
        return im
    if name == "L7":     # marteen, Minny, ANGE1
        im = bg("w", "GM"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "también llegarían", IT(900, 52), 360, 130, T, SEG[name] + .05, INK)
        for k, (tx, key) in enumerate((("MARTEEN", "marteen"), ("MINNY", "Minny"))):
            t0 = wt(7, key) - .15; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0: paste(im, nchip(tx, PUR, WHITE, 60), lerp(-300, 200 + k * 320, p), SY(280), clamp01(p))
        tg = wt(7, "Gentle") - .15
        if T > tg: word(im, "desde Gentle Mates", IT(900, 44), 360, 380, T, tg, PUR)
        ta = wt(7, "ANGE1") - .15
        if T > ta:
            slam(im, "ANGE1", ANTON(150), 360, 640, T, ta, PUR); pop(im, nchip("ENTRENADOR", INK, WHITE, 40), 360, 770, T, ta + .2, .3)
        tc = wt(7, "Copenhague") - .3
        if T > tc: ribbon(im, "CAMPEÓN MASTERS COPENHAGUE 2022", 360, 880, T, tc, WHITE, PUR, 44, "mm"); confetti(im, T, tc + .2)
        return im
    if name == "L8":     # roster
        im = bg("w", "FNC"); ring(im, 360, 640, 340, T * 1.4, PUR, .35)
        pop(im, FNC_P, 360, 160, T, SEG[name] + .05, .35); word(im, "roster 2027 · según reportes", IT(900, 36), 360, 290, T, SEG[name] + .2, INK)
        rows = (("KAAJAK", "kaajak", "SIGUE"), ("CLOUD", "Cloud", "SIGUE"), ("VALYN", None, "NUEVO"), ("MARTEEN", None, "NUEVO"), ("MINNY", None, "NUEVO"))
        t0b = wt(8, "Cloud") + .3
        for k, (tx, key, tag) in enumerate(rows):
            t0 = (wt(8, key) - .15) if key else t0b + (k - 2) * .18; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0:
                paste(im, nchip(tx, PUR if tag == "NUEVO" else INK, WHITE, 40), lerp(-300, 290, p), SY(350) + k * 80, clamp01(p))
                paste(im, nchip(tag, LIL if tag == "NUEVO" else LILL, INK, 26), lerp(1000, 520, p), SY(350) + k * 80, clamp01(p))
        tr = wt(8, "diciembre") - .2
        if T > tr: ribbon(im, "DEBUT: RED BULL HOME GROUND · DIC", 360, 900, T, tr, WHITE, PUR, 40, "mm")
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = Image.blend(vbgx("twerk", 31.5, 6.0, t * .9, .3), bg("w", "FNC"), .72)
    word(im, "¿Fnatic sin Boaster", IT(400, 54), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "PUEDE VOLVER A GANAR?", ANTON(80), 360, 260, T, SEG[f"L{k}"] + .3, PUR)
    tc = wt(k, "comentarios") - .1
    if T > tc: pop(im, U.COMMENT, 160, 470 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 160, 555, T, tc + .05, PUR)
    bb = BST_S.resize((260, int(BST_S.height * 260 / BST_S.width))); paste(im, bb, 360, SY(690) + 6 * math.sin(T * 2), clamp01((t - .2) * 3))
    for j, s_ in enumerate(("Fuentes: @FNATIC · @OfficialBoaster · Sheep Esports · Strafe · RG.org · nov 2026", "Clips: VCT / Masters Tokio 2023 / Champions París · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L5"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "BOASTER", "L1": "ERA", "L2": "2023", "L3": "2026", "L4": "ADIÓS", "L5": "CAPITÁN", "L6": "VALYN", "L7": "ANGE1", "L8": "2027", f"L{N-1}": "FNC"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, wt(0, "trofeos"), wt(0, "único"), SEG["L1"] + .1, wt(1, "final"), SEG["L2"] + .05, wt(2, "Tokio"), wt(3, "internacional"), wt(3, "Challengers"), wt(4, "Boaster"), wt(4, "Alfajer"), wt(6, "valyn"), wt(6, "IGL"), wt(7, "ANGE1"), SEG["L8"] + .05])
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
    ev = [("braam", 0.0, .7), ("hit808", 0.0, .6), ("pop", wt(0, "trofeos"), .5)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("shimmer", wt(2, "LOCK"), .5), ("shimmer", wt(2, "Tokio"), .5), ("cheer", wt(2, "Tokio"), .35), ("typing", SEG["L3"] + .3, .4), ("impact", wt(3, "play-ins"), .5),
        ("clink", wt(4, "Boaster"), .6), ("pop", wt(4, "crashies"), .5), ("impact", wt(4, "Alfajer"), .5), ("riser", SEG["L5"] - 1.0, .4), ("pop", wt(5, "compañero"), .5),
        ("pop", wt(6, "Sheep"), .5), ("braam", wt(6, "valyn"), .6), ("pop", wt(7, "marteen"), .5), ("pop", wt(7, "Minny"), .5), ("braam", wt(7, "ANGE1"), .5),
        ("shimmer", wt(7, "Copenhague"), .5), ("pop", wt(8, "kaajak"), .5), ("pop", wt(8, "Cloud"), .5), ("whoosh", wt(8, "diciembre"), .5), ("pop", wt(k, "comentarios"), .6)]
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
