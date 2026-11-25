#!/usr/bin/env python3
"""zekken deja MIBR y (según reportes) va a NRG — motion graphics morado.
Fuentes: @MIBR (19 nov 2026), Sheep Esports, Lion Esports, Strafe, Inven Global."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "zek"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3; T1 = os.path.join(PD, "clips", "despedida.mp4")

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
ZEK_M = cut("zekken_mibr2", 480); ZEK_MS = cut("zekken_mibr2", 300); ZEK_S = cut("zekken_sen", 440)
ASP = S.duo(Image.open(os.path.join(HERE, "..", "aspas", "rec", "aspas_mibr.png")).convert("RGBA"), 1.08); ASP = ASP.crop(ASP.getchannel("A").getbbox()); ASP = S.fade_bottom(ASP.resize((260, int(ASP.height * 260 / ASP.width)), Image.LANCZOS), .18)
def logo_a(path, h, col=PUR):
    im = Image.open(path).convert("RGBA"); o = Image.new("RGBA", im.size, col + (255,)); o.putalpha(im.getchannel("A")); o = o.crop(o.getbbox())
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)
MIBR_P = logo_a(os.path.join(PD, "logos", "mibr.webp"), 90); MIBR_W = logo_a(os.path.join(PD, "logos", "mibr.webp"), 80, WHITE)
NRG_P = logo_a(os.path.join(PD, "logos", "nrg.png"), 80); NRG_W = logo_a(os.path.join(PD, "logos", "nrg.png"), 80, WHITE)
SEN_P = logo_a(os.path.join(HERE, "..", "sen", "logos", "sen_w.png"), 110)
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
        im = vbgx("despedida", 33.0, 6.0, t * .8, .55); stripes(im, T, 0, WHITE); ring(im, 360, 980, 320, T * 1.5, LILL, .45)
        slam(im, "SE SEPARÓ DE ASPAS", ANTON(84), 360, 175, T, .1, WHITE)
        tc = wt(0, "campeón") - .3
        if T > tc: stamp(im, "Y VA AL CAMPEÓN DEL MUNDO", 360, 290, T, tc, (255, 255, 255), -5, 56)
        paste(im, ZEK_M, 360, SY(1290) - ZEK_M.height / 2 + 90 + 140 * (1 - eo(clamp01(t / .45))), clamp01(t * 5))
        particles(im, T, WHITE, .45); return im
    if name == "L1":     # motivacional
        im = bg("w", "NIVEL"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "un mal año", IT(400, 56), 360, 160, T, SEG[name] + .05, INK); slam(im, "NO BORRA", ANTON(150), 360, 290, T, wt(1, "borra") - .15, PUR)
        te = wt(1, "eres") - .3
        if T > te: ribbon(im, "LO QUE ERES", 360, 570, T, te, WHITE, PUR, 66, "mm")
        ring(im, 360, 780, 200, T * 1.4, PUR, .4); ring(im, 360, 780, 160, -T * 1.6, LIL, .35, 3, 22); return im
    if name == "L2":     # Masters Madrid
        im = bg("w", "MADRID"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 640, 300, T * 1.5, PUR, .4)
        pop(im, SEN_P, 360, 150, T, SEG[name] + .05, .35)
        tm = wt(2, "Madrid") - .25
        if T > tm: ribbon(im, "CAMPEÓN MASTERS MADRID 2024", 360, 290, T, tm, WHITE, PUR, 46, "mm"); confetti(im, T, tm + .1)
        p = eo(prog(T, SEG[name] + .2, SEG[name] + .6)); paste(im, ZEK_S, 360, SY(640) + 60 * (1 - p) + bob(T), p)
        tv = wt(2, "MVP") - .2
        if T > tv: stamp(im, "MVP DE LA FINAL", 360, 880, T, tv, PUR, -5, 70)
        return im
    if name == "L3":     # MIBR 2026
        im = vbgx("despedida", 7.5, 4.0, t * .8, .6); stripes(im, T, SEG[name], WHITE)
        pop(im, MIBR_W, 360, 140, T, SEG[name] + .05, .35); word(im, "2026", ANTON(60), 360, 230, T, SEG[name] + .2, WHITE)
        ta = wt(3, "aspas") - .2
        if T > ta:
            p = eo(prog(T, ta, ta + .4)); paste(im, ZEK_MS, 220, SY(520) + 40 * (1 - p) + bob(T), p); paste(im, ASP, 510, SY(530) + 40 * (1 - p) + bob(T, 1), p)
            word(im, "+ aspas", IT(900, 44), 360, 690, T, ta + .1, WHITE)
        for k, (tx, key) in enumerate((("MASTERS", "Masters"), ("CHAMPIONS", "Champions"))):
            t0 = wt(3, key) - .2; pp = ease_back(prog(T, t0, t0 + .3), 1.4)
            if pp > 0: paste(im, chipx(tx, False, 440), lerp(-300, 360, pp), SY(790) + k * 105, clamp01(pp))
        return im
    if name == "L4":     # banca
        im = bg("w", "BANCA"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        word(im, "23 de octubre", IT(900, 52), 360, 140, T, SEG[name] + .05, INK); pop(im, MIBR_P, 360, 780, T, SEG[name] + .2, .35)
        tb = wt(4, "banca") - .3
        if T > tb: stamp(im, "TODO EL EQUIPO A LA BANCA", 360, 290, T, tb, (200, 30, 60), -5, 56)
        tr = wt(4, "reportes") - .3
        if T > tr: pop(im, nchip("SEGÚN REPORTES", INK, WHITE, 36), 360, 470, T, tr, .3)
        tbr = wt(4, "Brasil") - .4
        if T > tbr: ribbon(im, "NO QUISO MUDARSE A BRASIL", 360, 600, T, tbr, WHITE, PUR, 50, "mm")
        return im
    if name == "L5":     # despedida
        im = vbgx("despedida", 36.0, 6.0, t * .9, .5); stripes(im, T, SEG[name], WHITE)
        ribbon(im, "“OBRIGADO, ZEKINHA”", 360, 150, T, SEG[name] + .1, WHITE, PUR, 60, "mm")
        word(im, "— MIBR · 19 nov", IT(900, 40), 360, 245, T, SEG[name] + .4, WHITE)
        return im
    if name == "L6":     # NRG
        im = bg("w", "NRG"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        word(im, "¿y a dónde va?", IT(900, 56), 360, 130, T, SEG[name] + .05, INK)
        ts = wt(6, "Sheep") - .2
        if T > ts: pop(im, nchip("SEGÚN SHEEP ESPORTS", INK, WHITE, 36), 360, 230, T, ts, .3)
        tn = wt(6, "NRG") - .2
        if T > tn: pop(im, shadow(NRG_P.resize((int(NRG_P.width * 1.6), int(NRG_P.height * 1.6))), 10, 10, .25), 360, 480, T, tn, .4); word(im, "acuerdo verbal", IT(900, 46), 360, 600, T, tn + .2, PUR)
        tc = wt(6, "campeones") - .3
        if T > tc: ribbon(im, "CAMPEONES DEL MUNDO 2025", 360, 730, T, tc, WHITE, PUR, 50, "mm"); confetti(im, T, tc + .1)
        return im
    if name == "L7":     # keiko
        im = bg("w", "KEIKO"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "ocuparía el lugar de", IT(900, 50), 360, 140, T, SEG[name] + .05, INK)
        tk = wt(7, "keiko") - .15
        if T > tk: slam(im, "KEIKO", ANTON(150), 360, 280, T, tk, PUR)
        ts = wt(7, "Sentinels") - .2
        if T > ts: word(im, "se fue a", IT(900, 44), 360, 520, T, ts, INK); pop(im, SEN_P, 360, 640, T, ts + .1, .35)
        ta = wt(7, "antiguo") - .3
        if T > ta: stamp(im, "SU ANTIGUO EQUIPO", 360, 820, T, ta, (200, 30, 60), -5, 64)
        return im
    if name == "L8":     # roster NRG
        im = bg("w", "NRG"); ring(im, 360, 640, 340, T * 1.4, PUR, .35)
        pop(im, NRG_P, 360, 160, T, SEG[name] + .05, .35); word(im, "roster 2027 · según reportes", IT(900, 36), 360, 270, T, SEG[name] + .2, INK)
        rows = (("ETHAN", "Ethan", "SIGUE"), ("MADA", "mada", "SIGUE"), ("SKUBA", "skuba", "SIGUE"), ("EEIU", "eeiu", "VUELVE"), ("ZEKKEN", "zekken", "NUEVO"))
        for k, (tx, key, tag) in enumerate(rows):
            t0 = wt(8, key) - .15; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0:
                paste(im, nchip(tx, PUR if tag != "SIGUE" else INK, WHITE, 40), lerp(-300, 290, p), SY(350) + k * 80, clamp01(p))
                paste(im, nchip(tag, LIL if tag != "SIGUE" else LILL, INK, 26), lerp(1000, 520, p), SY(350) + k * 80, clamp01(p))
        return im
    if name == "L9":     # debut
        im = vbgx("despedida", 2.0, 4.0, t * .8, .6); stripes(im, T, SEG[name], WHITE)
        word(im, "su debut", IT(900, 52), 360, 150, T, SEG[name] + .05, WHITE)
        tr = wt(9, "Red") - .3
        if T > tr: ribbon(im, "RED BULL HOME GROUND", 360, 270, T, tr, PUR, WHITE, 56, "mm"); word(im, "10–13 dic · Los Ángeles", IT(900, 42), 360, 370, T, tr + .2, WHITE)
        p = eo(prog(T, SEG[name] + .3, SEG[name] + .7)); paste(im, ZEK_MS, 360, SY(700) + 60 * (1 - p) + bob(T), p)
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "ZEKKEN")
    word(im, "¿zekken vuelve a su", IT(400, 52), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "MEJOR NIVEL?", ANTON(110), 360, 260, T, SEG[f"L{k}"] + .3, PUR)
    tc = wt(k, "comentarios") - .1
    if T > tc: pop(im, U.COMMENT, 160, 470 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 160, 555, T, tc + .05, PUR)
    jj = ZEK_MS.resize((260, int(ZEK_MS.height * 260 / ZEK_MS.width))); paste(im, jj, 400, SY(700) + 6 * math.sin(T * 2), clamp01((t - .2) * 3))
    for j, s_ in enumerate(("Fuentes: @MIBR · Sheep Esports · Lion Esports · Strafe · Inven Global · nov 2026", "Clip: despedida oficial de MIBR · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L3", "L5", "L9"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "ZEKKEN", "L1": "NIVEL", "L2": "MADRID", "L3": "MIBR", "L4": "BANCA", "L5": "OBRIGADO", "L6": "NRG", "L7": "KEIKO", "L8": "2027", "L9": "LA", f"L{N-1}": "ZEKKEN"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, wt(0, "campeón"), SEG["L1"] + .1, wt(1, "eres"), wt(2, "Madrid"), wt(2, "MVP"), wt(3, "aspas"), wt(3, "Champions"), wt(4, "banca"), wt(4, "Brasil"), SEG["L5"] + .1, wt(6, "NRG"), wt(7, "keiko"), wt(7, "antiguo"), SEG["L8"] + .05, wt(9, "Red")])
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
    ev = [("braam", 0.0, .7), ("hit808", 0.0, .6), ("pop", wt(0, "campeón"), .5)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("shimmer", wt(2, "Madrid"), .5), ("cheer", wt(2, "Madrid"), .35), ("pop", wt(2, "MVP"), .5), ("pop", wt(3, "aspas"), .5), ("impact", wt(3, "Masters"), .5), ("impact", wt(3, "Champions"), .5),
        ("clink", wt(4, "banca"), .6), ("pop", wt(4, "reportes"), .5), ("riser", SEG["L5"] - 1.0, .4), ("pop", wt(6, "Sheep"), .5), ("braam", wt(6, "NRG"), .6), ("shimmer", wt(6, "campeones"), .5),
        ("pop", wt(7, "keiko"), .5), ("pop", wt(7, "Sentinels"), .5), ("impact", wt(7, "antiguo"), .5), ("pop", wt(8, "Ethan"), .5), ("pop", wt(8, "mada"), .5), ("pop", wt(8, "skuba"), .5),
        ("pop", wt(8, "eeiu"), .5), ("boom", wt(8, "zekken"), .5), ("whoosh", wt(9, "Red"), .5), ("pop", wt(k, "comentarios"), .6)]
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
