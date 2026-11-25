#!/usr/bin/env python3
"""Paper Rex 2027: Primmie + regreso de PatMen (pedido en comentarios) — motion graphics morado.
Voz: Andrés (eleven_v4, 1.1x). Fuentes: anuncio de @pprxteam (19 nov 2026), Sheep Esports, pley.gg, Hotspawn, bo3.gg.
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
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "prx"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3; T1 = os.path.join(PD, "clips", "t1.mp4")

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
def head(n, w):
    im = duo(Image.open(os.path.join(RC, n + "_head.png")).convert("RGBA"), 1.1); return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
HD = {n: head(n, 300) for n in ("primmie", "patmen", "forsaken", "something", "invy", "sumthang")}
PRI_B = head("primmie", 430); PAT_B = head("patmen", 400); SOM_B = head("something", 340); SUM_B = head("sumthang", 260)
COMM = Image.open(os.path.join(PD, "fotos", "comentario.png")).convert("RGBA"); FAN = Image.open(os.path.join(PD, "fotos", "fan_prediccion.png")).convert("RGBA")
def card(img, w, pad=22):
    im = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS); c = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, fill=255)
    c.paste(WHITE + (255,), (0, 0, c.width, c.height)); c.alpha_composite(im, (pad, pad)); c.putalpha(m)
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, outline=PUR + (255,), width=5); return shadow(c, 14, 14, .35)
COMM_C = card(COMM, 600); FAN_C = card(FAN, 560)
CM = {n: card(Image.open(os.path.join(PD, "fotos", n + ".png")).convert("RGBA"), 440, 12) for n in ("c_jester", "c_yesway", "c_poyo", "c_whatiwant", "c_kuro", "c_swear")}
_ge = Image.open(os.path.join(HERE, "..", "xavi", "logos", "ge.png")).convert("RGBA")
def ge_logo(h, col=WHITE):
    a = np.asarray(_ge).astype(float); m = np.clip((255 - a[..., :3].min(2) - 30) * 3, 0, 255) * (a[..., 3] / 255)
    im = Image.new("RGBA", _ge.size, col + (255,)); im.putalpha(Image.fromarray(m.astype(np.uint8))); im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
GE_W = ge_logo(140)
def flag_th(w=180, h=120):
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im); ys = [0, 1, 2, 4, 5, 6]; cols = [PUR, WHITE, LIL, WHITE, PUR]
    for k, c in enumerate(cols): d.rectangle((0, h * ys[k] / 6, w, h * ys[k + 1] / 6), fill=c + (255,))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=255); im.putalpha(m); return shadow(im, 10, 10, .3)
TH = flag_th()
def chipx(txt, ok, w=520, col=None):
    c = Image.new("RGBA", (w, 100)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, w - 1, 99), 30, fill=(col or (PUR if ok else (200, 30, 60))) + (255,))
    f = ANTON(50)
    while f.getlength(txt) > w - 130: f = ANTON(f.size - 2)
    d.text((32, 50), txt, font=f, fill=WHITE, anchor="lm")
    if ok: c.alpha_composite(L.check(56), (w - 82, 22))
    else: d.line((w - 78, 28, w - 34, 72), fill=WHITE, width=9); d.line((w - 34, 28, w - 78, 72), fill=WHITE, width=9)
    return shadow(c, 10, 10, .3)
_ch = {}
def headring(im, hd, name, x, y, T, a=1.0, col=PUR, rx=None):
    """Homenaje al anuncio de PRX: la cabeza con su nombre girando alrededor."""
    if a <= 0: return
    rx = rx or hd.width * .62; ry = hd.height * .6; f = ANTON(30); txt = (name.upper() + " · ") * 6
    lay = canvas(); n = len(txt); off = T * .35
    for k, chr_ in enumerate(txt):
        ang = off + k * 2 * math.pi / n; px, py = x + rx * math.cos(ang), y + ry * math.sin(ang)
        key = (chr_, col)
        if key not in _ch: _ch[key] = text_layer(chr_, f, col) if chr_.strip() else None
        g = _ch[key]
        if g is None: continue
        g2 = g.rotate(-math.degrees(ang) - 90, expand=True, resample=Image.BICUBIC); lay.alpha_composite(g2, (int(px - g2.width / 2), int(py - g2.height / 2)))
    paste(im, lay, 0, 0, a, "lt"); paste(im, shadow(hd, 12, 12, .3), x, y, a)
def vbg(t0, dur, t, a=.55):
    return Image.blend(clip(T1, t0, dur, (186, 420, 204, 348), (720, 1280), t), canvas(PUR + (255,)), a)
def bob(T, k=0): return 8 * math.sin(T * 2.4 + k)

def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # mención al comentario
        im = bg("w", "PEDIDO"); stripes(im, T, 0, PUR, .5); ring(im, 360, 640, 330, T * 1.5, PUR, .35)
        word(im, "me lo pidieron en los", IT(900, 52), 360, 200, T, .05, INK); slam(im, "COMENTARIOS", ANTON(110), 360, 300, T, .2, PUR)
        p = ease_back(prog(T, .35, .7), 1.4); paste(im, COMM_C, 360, SY(600) + 60 * (1 - p) + bob(T) * .4, clamp01(p))
        if T > .9:
            hp = .5 + .5 * math.sin(T * 9); heart = U.HEART if hasattr(U, "HEART") else None
            if heart is not None: paste(im, heart.resize((70, 70)), 600, SY(560), hp)
        tq = wt(0, "aquí") - .1
        if T > tq: stamp(im, "AQUÍ ESTÁ", 360, 730, T, tq, (255, 255, 255), -6, 100)
        for j, n in enumerate(("primmie", "patmen")):
            pj = ease_back(prog(T, .8 + j * .2, 1.15 + j * .2), 1.4); hd = HD[n].resize((200, int(HD[n].height * 200 / HD[n].width)))
            if pj > 0: paste(im, shadow(hd, 10, 10, .3), 200 + j * 320, SY(880) + bob(T, j), clamp01(pj))
        return im
    if name == "L1":     # gancho
        im = vbg(2.4, 2.2, t * .7, .55); stripes(im, T, SEG[name], WHITE); ring(im, 360, 900, 300, T * 1.6, LILL, .45)
        p = eo(clamp01(t / .4)); headring(im, PRI_B, "primmie", 360, SY(820) + 120 * (1 - p) + bob(T), T, p, WHITE)
        slam(im, "LO BARRIERON", ANTON(92), 360, 210, T, SEG[name] + .05, WHITE)
        counter(im, T, wt(1, "tres") - .1, wt(1, "cero") + .1, 0, 3, ANTON(150), 250, 360, WHITE)
        if T > wt(1, "cero"): slam(im, "– 0", ANTON(150), 440, 360, T, wt(1, "cero"), WHITE)
        ta = wt(1, "ahora") - .1
        if T > ta: stamp(im, "Y AHORA JUEGA PARA ELLOS", 360, 520, T, ta, (255, 255, 255), -5, 54)
        return im
    if name == "L2":     # motivacional
        im = bg("w", "PUERTA"); SN.graph(im, T, SEG[name] + .05, SEG[name] + DL[2])
        word(im, "a veces el que te", IT(400, 54), 360, 160, T, SEG[name] + .05, INK); slam(im, "GANA", ANTON(170), 360, 290, T, wt(2, "gana") - .1, PUR)
        ta = wt(2, "abre") - .1
        if T > ta: ribbon(im, "ES EL QUE TE ABRE LA PUERTA", 360, 460, T, ta, WHITE, PUR, 50, "mm")
        ring(im, 360, 700, 200, T * 1.4, PUR, .4); ring(im, 360, 700, 160, -T * 1.6, LIL, .35, 3, 22)
        return im
    if name == "L3":     # anuncio oficial
        im = Image.blend(clip(T1, 0.0, 2.3, (0, 0, 576, 768), (720, 1280), min(t * .5, 2.2)), canvas(PUR + (255,)), .62)
        ribbon(im, "ES OFICIAL · ROSTER 2027", 360, 150, T, SEG[name] + .05, WHITE, PUR, 50, "mm")
        word(im, "@pprxteam · 19 nov", IT(900, 38), 360, 230, T, SEG[name] + .25, WHITE)
        tp = wt(3, "Primmie") - .15; tm = wt(3, "PatMen") - .15
        if T < tp:     # comentarios de los seguidores en el post del anuncio (uno tras otro)
            pairs = (("c_jester", "c_yesway"), ("c_poyo", "c_whatiwant"), ("c_kuro", "c_swear")); span = (tp - SEG[name] - .4) / 3
            for j, (a1, a2) in enumerate(pairs):
                t0 = SEG[name] + .35 + j * span; t1 = t0 + span
                if not (t0 <= T < t1 + .25): continue
                out = eo(prog(T, t1, t1 + .25)); p1 = ease_back(prog(T, t0, t0 + .3), 1.4); p2 = ease_back(prog(T, t0 + .45, t0 + .75), 1.4)
                if p1 > 0: paste(im, CM[a1], lerp(-300, 330, p1) - 700 * out, SY(470) + bob(T, j) * .3, clamp01(p1) * (1 - out))
                if p2 > 0: paste(im, CM[a2], lerp(1000, 390, p2) + 700 * out, SY(470) + 150 + bob(T, j + 1) * .3, clamp01(p2) * (1 - out))
        if T > tp: headring(im, HD["primmie"], "primmie", 200, SY(600) + bob(T), T, ease_back(prog(T, tp, tp + .35), 1.3), WHITE)
        if T > tm:
            headring(im, HD["patmen"], "patmen", 520, SY(640) + bob(T, 2), T, ease_back(prog(T, tm, tm + .35), 1.3), WHITE)
            stamp(im, "REGRESA", 520, 820, T, tm + .2, (255, 255, 255), 8, 64)
        if T > tp: stamp(im, "NUEVO", 200, 790, T, tp + .2, (255, 255, 255), -8, 64)
        return im
    if name == "L4":     # salidas
        im = bg("w", "ADIÓS"); stripes(im, T, SEG[name], PUR, .5)
        slam(im, "PARA HACER ESPACIO", ANTON(76), 360, 170, T, SEG[name] + .05, PUR)
        for k, (nm, key) in enumerate((("JINGGG", "Jinggg"), ("D4V41", "d4v41"))):
            t0 = wt(4, key) - .15; p = ease_back(prog(T, t0, t0 + .35), 1.4)
            if p > 0: paste(im, chipx(nm, False, 480), lerp(-300, 360, p), SY(330) + k * 120, clamp01(p))
        tc = wt(4, "cinco") - .1
        if T > tc:
            counter(im, T, tc, tc + .6, 0, 5, ANTON(170), 300, 600, PUR); word(im, "AÑOS", ANTON(80), 470, 620, T, tc + .2, INK)
            word(im, "dos leyendas del equipo", IT(900, 44), 360, 740, T, tc + .3, PUR)
        return im
    if name == "L5":     # perfil Primmie
        im = vbg(9.0, 3.0, t * .8, .55); ring(im, 360, 700, 300, T * 1.6, WHITE, .35)
        headring(im, HD["primmie"], "primmie", 360, SY(680) + bob(T), T, clamp01(t * 4), WHITE)
        pop(im, TH, 140, 230, T, SEG[name] + .1, .35)
        for k, (tx, key) in enumerate((("DUELISTA", "duelista"), ("22 AÑOS", "veintidós"), ("MIRA TOP DEL PACÍFICO", "miras"))):
            t0 = wt(5, key) - .15
            if T > t0: pop(im, SN.namechip(tx, WHITE, PUR, 40), 480 if k < 2 else 360, 200 + k * 80 if k < 2 else 370, T, t0, .3)
        tf = wt(5, "FULL") - .15; tb = wt(5, "barrió") - .1
        if T > tf and T < tb + .1: ribbon(im, "FINAL STAGE 1 · CON FULL SENSE", 360, 900, T, tf, PUR, WHITE, 42, "mm")
        if T > tb: slam(im, "PRX 3 – 0 FS", ANTON(110), 360, 900, T, tb, WHITE)
        return im
    if name == "L6":     # sin series ganadas
        im = bg("w", "0 SERIES"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 420, 150, T * 1.8, PUR, .35); ring(im, 360, 420, 120, -T * 2, LIL, .3, 3, 22)
        word(im, "en sus dos internacionales", IT(900, 46), 360, 120, T, SEG[name] + .05, INK)
        counter(im, T, SEG[name] + .2, wt(6, "serie"), 9, 0, ANTON(190), 360, 290, PUR)
        if T > wt(6, "serie") - .2: word(im, "SERIES GANADAS", ANTON(70), 360, 510, T, wt(6, "serie") - .2, INK)
        for k, tx in enumerate(("CHAMPIONS 2024", "MASTERS LONDON 2026")):
            t0 = wt(6, "serie") + .1 + k * .25; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0: paste(im, chipx(tx, False, 520), lerp(1000, 360, p), SY(625) + k * 112, clamp01(p))
        tg = wt(6, "ganador") - .3
        if T > tg: ribbon(im, "AHORA: EL EQUIPO MÁS GANADOR DE LA REGIÓN", 360, 880, T, tg, WHITE, PUR, 36, "mm")
        return im
    if name == "L7":     # PatMen conoce la casa
        im = bg("w", "TORONTO"); ring(im, 360, 700, 320, T * 1.5, PUR, .4); ring(im, 360, 700, 270, -T * 1.6, LIL, .35, 3, 26)
        word(im, "PatMen ya conoce", IT(900, 52), 360, 160, T, SEG[name] + .05, INK); slam(im, "LA CASA", ANTON(130), 360, 270, T, wt(7, "casa") - .1, PUR)
        headring(im, HD["patmen"], "patmen", 360, SY(690) + bob(T), T, clamp01(t * 4))
        tt = wt(7, "Masters") - .15
        if T > tt:
            ribbon(im, "CAMPEÓN MASTERS TORONTO 2025", 360, 900, T, tt, WHITE, PUR, 44, "mm"); confetti(im, T, tt + .1)
        return im
    if name == "L8":     # GE y regreso
        im = vbg(17.0, 3.0, t * .8, .6); stripes(im, T, SEG[name], WHITE)
        tv = wt(8, "vuelve") - .15
        if T < tv:
            pop(im, GE_W, 360, 230, T, wt(8, "Global") - .15, .35)
            ts = wt(8, "etapa") - .15
            if T > ts: pop(im, chipx("CAMPEÓN STAGE 2 · 2026", True, 560, PUR), 360, 490, T, ts, .3)
            tc = wt(8, "cerró") - .1
            if T > tc: stamp(im, "EQUIPO CERRADO", 360, 680, T, tc, (255, 255, 255), -6, 80)
        else:
            slam(im, "VUELVE A CASA", ANTON(100), 360, 230, T, tv, WHITE)
            headring(im, HD["patmen"], "patmen", 360, SY(660) + bob(T), T, ease_back(prog(T, tv, tv + .35), 1.3), WHITE)
        return im
    if name == "L9":     # something nacionalizado
        im = bg("w", "APAC"); stripes(im, T, SEG[name], PUR, .5)
        pop(im, SN.namechip("SEGÚN REPORTES", INK, WHITE, 40), 360, 140, T, SEG[name] + .05, .3)
        headring(im, HD["something"], "something", 360, SY(560) + bob(T), T, clamp01(t * 4))
        tn = wt(9, "nacionalizado") - .15
        if T > tn: slam(im, "DE RUSIA A APAC", ANTON(80), 360, 835, T, tn, PUR)
        tr = wt(9, "reglas") - .15
        if T > tr: word(im, "mínimo 3 jugadores de la región", IT(900, 40), 360, 900, T, tr, INK)
        return im
    if name == "L10":    # roster
        im = bg("w", "PRX"); ring(im, 360, 640, 340, T * 1.4, PUR, .35)
        ribbon(im, "PAPER REX 2027", 360, 170, T, SEG[name] + .05, WHITE, PUR, 64, "mm")
        pos = [("forsaken", "f0rsakeN", 130, 360), ("something", "something", 360, 360), ("invy", "invy", 590, 360), ("patmen", "PatMen", 230, 760), ("primmie", "Primmie", 490, 760)]
        for k, (n, key, x, y) in enumerate(pos):
            t0 = wt(10, key) - .15
            if T > t0:
                p = ease_back(prog(T, t0, t0 + .3), 1.5); hd = HD[n].resize((170 if k < 3 else 210, int(HD[n].height * (170 if k < 3 else 210) / HD[n].width)))
                paste(im, shadow(hd, 10, 10, .3), x, SY(y) - 20 + bob(T, k), clamp01(p)); paste(im, SN.namechip(key.upper(), PUR, WHITE, 32), x, SY(y) + hd.height / 2 + 10, clamp01(p))
        return im
    if name == "L11":    # el fan que lo adivinó
        im = bg("w", "OCT 27"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "un fan lo adivinó en", IT(900, 50), 360, 160, T, SEG[name] + .05, INK); slam(im, "OCTUBRE", ANTON(120), 360, 270, T, wt(11, "octubre") - .1, PUR)
        p = ease_back(prog(T, wt(11, "octubre"), wt(11, "octubre") + .4), 1.3); paste(im, FAN_C, 360, SY(610) + 50 * (1 - p), clamp01(p))
        tc = wt(11, "respondió") - .1
        if T > tc:
            ribbon(im, "PRX: “HOW DID BRO KNOW”", 360, 880, T, tc, WHITE, PUR, 50, "mm")
            p2 = eo(prog(T, tc + .2, tc + .6)); sb = SUM_B.resize((190, int(SUM_B.height * 190 / SUM_B.width))); paste(im, sb, lerp(900, 600, p2), SY(760) + bob(T), p2)
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "PRX")
    word(im, "¿Este Paper Rex por fin gana", IT(400, 50), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "UN INTERNACIONAL?", ANTON(92), 360, 260, T, SEG[f"L{k}"] + .3, PUR)
    tc = wt(k, "comentarios") - .1
    if T > tc: pop(im, U.COMMENT, 360, 470 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 360, 555, T, tc + .05, PUR)
    for j, n in enumerate(("forsaken", "something", "invy", "patmen", "primmie")):
        hd = HD[n].resize((120, int(HD[n].height * 120 / HD[n].width))); p = clamp01((t - .2 - j * .08) * 4)
        paste(im, hd, 120 + j * 120, SY(700) + 8 * math.sin(T * 3 + j), p)
    for j, s_ in enumerate(("Fuentes: @pprxteam · Sheep Esports · pley.gg · Hotspawn · bo3.gg · nov 2026", "Clip: reacciones de streamers (TikTok) · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 860 + j * 26, p)
    return im

PURPLE_SC = {"L1", "L3", "L5", "L8"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "PEDIDO", "L1": "3–0", "L2": "PUERTA", "L3": "2027", "L4": "ADIÓS", "L5": "PRIMMIE", "L6": "0 SERIES", "L7": "TORONTO", "L8": "VUELVE",
        "L9": "APAC", "L10": "PRX", "L11": "OCT 27", f"L{N-1}": "PRX"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.2, wt(0, "aquí"), SEG["L1"] + .05, wt(1, "cero"), wt(1, "ahora"), wt(2, "gana"), SEG["L3"] + .05, wt(3, "PatMen"), wt(4, "Jinggg"), wt(4, "d4v41"),
                              wt(5, "barrió"), wt(6, "serie"), wt(7, "Toronto"), wt(8, "cerró"), wt(8, "vuelve"), wt(9, "nacionalizado"), SEG["L10"] + .05, wt(11, "respondió")])
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
    ev = [("braam", 0.0, .6), ("pop", .4, .6), ("pop", wt(0, "aquí"), .5)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("braam", SEG["L1"] + .05, .7), ("pop", wt(1, "cero"), .5), ("riser", SEG["L3"] - 1.0, .45), ("shimmer", wt(3, "Primmie"), .5), ("pop", wt(3, "PatMen"), .5),
        ("impact", wt(4, "Jinggg"), .5), ("impact", wt(4, "d4v41"), .5), ("typing", wt(4, "cinco") - .1, .35), ("braam", wt(5, "barrió"), .6), ("typing", SEG["L6"] + .2, .4),
        ("shimmer", wt(7, "Masters"), .6), ("cheer", wt(7, "Masters"), .35), ("clink", wt(8, "cerró"), .7), ("crowd", wt(8, "vuelve"), .35), ("typing", SEG["L9"] + .05, .35),
        ("pop", wt(10, "f0rsakeN"), .5), ("pop", wt(10, "something"), .5), ("pop", wt(10, "invy"), .5), ("pop", wt(10, "PatMen"), .5), ("boom", wt(10, "Primmie"), .5),
        ("whoosh", wt(11, "octubre"), .5), ("pop", wt(11, "respondió"), .6), ("pop", wt(k, "comentarios"), .6)]
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
