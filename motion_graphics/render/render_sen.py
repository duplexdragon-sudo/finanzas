#!/usr/bin/env python3
"""SENTINELS 2027: de 0 internacionales a superequipo (keiko, la pieza final) — motion graphics morado.
Voz: Andrés (eleven_v4, 1.1x). Fuentes: Insider Gaming, esportsinsider, Hotspawn, THESPIKE.GG, pley.gg, RG.org (16–17 nov 2026).
Clips: videos oficiales de anuncio de Sentinels (Instagram @sentinels).
Uso: python3 render_sen.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, wave, json, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_smg as S
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, player_orbit,
                        rcard, brackets, puzzle_tile, U, R, clip, stamp, cutp)
import render_loud as L
from render_motion import grid as M_grid
HERE = os.path.dirname(os.path.abspath(__file__)); SD = os.path.join(HERE, "..", "sen"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3
C = lambda n: os.path.join(SD, "clips", n + ".mp4")
KEIKO, ZELL, CANE, JOHN, BRAWK, OXYV = C("ig"), C("ig2"), C("ig3"), C("ig4"), C("ig5"), C("ig6")

N = 13; DL, WT = [], []
for i in range(N):
    w = wave.open(os.path.join(SD, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(SD, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
    for ch, a in zip(al["characters"], al["character_start_times_seconds"]):
        if ch.isspace():
            if cur: ws.append((cur, st)); cur = ""
        else:
            if not cur: st = a
            cur += ch
    if cur: ws.append((cur, st))
    WT.append(ws)
LS = []; t = .15
for d in DL: LS.append(t); t += d + .22
DUR = t + 1.2
SEG = {f"L{i}": (LS[i] - .1 if i else 0.0) for i in range(11)}; SEG["cta"] = LS[11] - .1
ORDER = sorted(SEG, key=SEG.get)
def wt(k, s, n=0):
    hits = [st for w_, st in WT[k] if s.lower() in w_.lower()]
    return LS[k] + (hits[min(n, len(hits) - 1)] if hits else 0)

RC = os.path.join(SD, "rec")
_o = Image.open(os.path.join(SD, "fotos", "oficial_crop.png")).convert("RGBA"); OFI = _o.resize((700, int(_o.height * 700 / _o.width)), Image.LANCZOS); OFI_A = OFI.getchannel("A")
JOHN_P = cutp(os.path.join(RC, "johnqt.png"), 420); OXY_P = cutp(os.path.join(RC, "oxy.png"), 520); CANE_P = cutp(os.path.join(RC, "canezerra.png"), 380)
SEN = Image.open(os.path.join(SD, "logos", "sen_w.png")).convert("RGBA")
def senlogo(h, col=WHITE): return R.tint(SEN.resize((int(SEN.width * h / SEN.height), h), Image.LANCZOS), col)
ICONS = [R.HAB[k] for k in ("omen_0", "jett_0", "raze_0", "chamber_0", "omen_1", "jett_1", "raze_1", "chamber_1") if k in R.HAB]

def vcard(path, t0, dur, crop, size, t, border=WHITE, r=26):
    return rcard(clip(path, t0, dur, crop, size, t), r, border)
def namechip(txt, col=PUR, fg=WHITE, size=46):
    f = ANTON(size); tw = int(f.getlength(txt)); c = Image.new("RGBA", (tw + 60, int(size * 1.6))); ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), c.height // 2, fill=col + (255,))
    ImageDraw.Draw(c).text((c.width / 2, c.height / 2 + 2), txt, font=f, fill=fg, anchor="mm"); return c
def xcard(txt, ok, w=540):
    c = Image.new("RGBA", (w, 110)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, w - 1, 109), 30, fill=(PUR if ok else (200, 30, 60)) + (255,))
    d.text((40, 55), txt, font=ANTON(54), fill=WHITE, anchor="lm")
    if ok: c.alpha_composite(L.check(60), (w - 90, 25))
    else: d.line((w - 85, 30, w - 35, 80), fill=WHITE, width=10); d.line((w - 35, 30, w - 85, 80), fill=WHITE, width=10)
    return shadow(c, 10, 10, .3)
def graph(im, T, t0, t1):
    """Línea que cae a cero y luego se dispara hacia arriba."""
    pts = [(80, 360), (200, 420), (300, 560), (380, 760), (440, 800), (500, 640), (580, 420), (650, 220)]
    p = clamp01((T - t0) / max(.1, t1 - t0)); n = 1 + p * (len(pts) - 1); k = int(n); fr = n - k
    seg = pts[:k] + ([(lerp(pts[k - 1][0], pts[k][0], fr), lerp(pts[k - 1][1], pts[k][1], fr))] if k < len(pts) else [])
    d = ImageDraw.Draw(im)
    if len(seg) > 1: d.line(seg, fill=PUR + (255,), width=14, joint="curve")
    if len(seg) > 1:
        x, y = seg[-1]; d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=PUR + (255,))
    if p > .45: d.ellipse((440 - 22, 800 - 22, 440 + 22, 800 + 22), outline=(200, 30, 60, 255), width=6)

def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # gancho: foto oficial "Sentinels 2027"
        im = canvas(PUR + (255,)); M_grid(im, (128, 34, 178, 255), 56); ring(im, 360, 640, 330, T * 1.4, LILL, .4)
        rr = L.RAYS.rotate(T * 20, resample=Image.BICUBIC); rr = rr.resize((int(rr.width * .9), int(rr.height * .9))); paste(im, rr, 360, 640, clamp01(t * 4) * .5)
        ts_ = wt(0, "superequipo") - .2
        # foto oficial con zoom de entrada y oscurecido mientras habla de 2026
        zi = lerp(1.25, 1.0, eo(clamp01(t / .5))) * (1 + .02 * t)
        ph = OFI.resize((int(OFI.width * zi), int(OFI.height * zi)), Image.LANCZOS)
        dark = .55 * clamp01((T - .9) * 3) * (1 - clamp01((T - ts_) * 3))
        if dark > 0: ph = Image.blend(ph, Image.new("RGBA", ph.size, (20, 0, 35, 255)), dark); ph.putalpha(OFI_A.resize(ph.size))
        paste(im, rcard(ph, 30, WHITE), 360, 580, clamp01(t * 6))
        if t < .15: im = Image.blend(im, canvas(WHITE + (255,)), .6 * (1 - t / .15))
        # título del post
        tl = Image.new("RGBA", (560, 96), WHITE + (255,)); d = ImageDraw.Draw(tl); d.text((40, 50), "SENTINELS 2027", font=ANTON(64), fill=PUR, anchor="lm")
        lx = 470; d.rounded_rectangle((lx, 44, lx + 54, 84), 8, fill=PUR + (255,)); d.arc((lx + 9, 14, lx + 45, 60), 180, 360, fill=PUR + (255,), width=8)
        p0 = eo(prog(T, .1, .45)); paste(im, tl.crop((0, 0, max(1, int(560 * p0)), 96)), 80, 200, 1, "lm")
        pop(im, senlogo(70), 640, 200, T, .1, .3)
        # sello 0 internacionales
        if T < ts_ + .2: stamp(im, "0 INTERNACIONALES EN 2026", 360, 580, T, .95, (255, 255, 255), -8, 54)
        for k, (tx, t0) in enumerate((("MASTERS", 1.6), ("CHAMPIONS", 1.9))):
            p = ease_back(prog(T, t0, t0 + .3), 1.6)
            if p > 0 and T < ts_ + .1:
                c = Image.new("RGBA", (320, 96)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 319, 95), 28, fill=(200, 30, 60, 255))
                d.text((24, 48), tx, font=ANTON(44), fill=WHITE, anchor="lm"); d.line((256, 30, 292, 66), fill=WHITE, width=9); d.line((292, 30, 256, 66), fill=WHITE, width=9)
                paste(im, shadow(c, 8, 8, .3), (190, 530)[k], 1000 + 260 * (1 - p), p * (1 - clamp01((T - ts_) * 6)))
        if T < ts_ + .1 and T > 2.2:
            pb = eo(prog(T, 2.2, 2.5)); tl2 = text_layer("en 2026 no jugaron ni uno", IT(900, 46), WHITE); band = Image.new("RGBA", (tl2.width + 50, tl2.height + 24), INK + (220,))
            band.alpha_composite(tl2, (25, 12)); paste(im, band, 360, 1120 + 20 * (1 - pb), pb * (1 - clamp01((T - ts_) * 6)))
        # superequipo + nombres
        if T > ts_:
            ribbon(im, "Y ARMÓ UN SUPEREQUIPO", 360, 990, T, ts_, WHITE, PUR, 58, "mm"); confetti(im, T, ts_ + .1)
        for k, (nm, sub) in enumerate((("johnqt", "se queda"), ("OXY", "ex Cloud9"), ("brawk", "campeón 2025"), ("canezerra", "ex Envy"), ("keiko", "ex NRG"))):
            t0 = ts_ + .3 + k * .15; p = ease_back(prog(T, t0, t0 + .3), 1.5)
            if p <= 0: continue
            c = Image.new("RGBA", (200, 92)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 199, 91), 22, fill=INK + (240,))
            d.text((100, 34), nm.upper(), font=ANTON(36), fill=WHITE, anchor="mm"); d.text((100, 70), sub, font=SANS(600, 20), fill=LILL, anchor="mm")
            x = (140, 360, 580, 250, 470)[k]; y = 1095 if k < 3 else 1195
            paste(im, shadow(c, 8, 8, .3), x, y + 40 * (1 - p), clamp01(p * 2))
        particles(im, T, WHITE, .45); return im
    if name == "L1":     # motivacional
        im = bg("w", "FONDO"); graph(im, T, SEG["L1"] + .05, SEG["L1"] + DL[1])
        word(im, "tocar", IT(400, 56), 360, 150, T, SEG["L1"] + .05, INK); slam(im, "FONDO", ANTON(140), 360, 250, T, SEG["L1"] + .1, PUR)
        word(im, "también es un", IT(400, 52), 360, 960, T, wt(1, "también"), INK); slam(im, "PUNTO DE PARTIDA", ANTON(92), 360, 1060, T, wt(1, "partida"), PUR); return im
    if name == "L2":     # 2026 sin Masters ni Champions
        im = bg("p", "2026"); slam(im, "2026", ANTON(170), 360, 180, T, wt(2, "2026"), WHITE)
        for j, (tx, t0) in enumerate((("MASTERS SANTIAGO", wt(2, "Masters")), ("MASTERS LONDON", wt(2, "Masters") + .25), ("CHAMPIONS SHANGHÁI", wt(2, "Champions")))):
            p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0: paste(im, xcard(tx, False, 580), lerp(-300, 360, p), 420 + j * 150, p)
        stamp(im, "CERO", 360, 950, T, wt(2, "Champions") + .4, (255, 255, 255), -10, 120); particles(im, T, WHITE, .4); return im
    if name == "L3":     # cuatro fichajes, solo queda johnqt
        im = bg("w", "2027"); stripes(im, T, SEG["L3"], PUR, .6); ring(im, 360, 700, 300, T * 1.5, PUR, .45); ring(im, 360, 700, 250, -T * 1.5, LIL, .35, 3, 26)
        word(im, "lo cambiaron casi todo", IT(900, 52), 360, 150, T, SEG["L3"] + .05, PUR)
        slam(im, "4 FICHAJES", ANTON(110), 360, 260, T, SEG["L3"] + .15, INK)
        for j in range(5):
            t0 = wt(3, "fichajes") + j * .1; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p <= 0: continue
            keep = j == 0; c = namechip("JOHNQT" if keep else "NUEVO", PUR if keep else (200, 30, 60), WHITE, 34)
            paste(im, c, 360 if keep else lerp(-200, 360, p), 380 + j * 78, p)
        if T > wt(3, "johnqt") - .1:
            pj = eo(prog(T, wt(3, "johnqt") - .1, wt(3, "johnqt") + .3)); q = JOHN_P.resize((int(JOHN_P.width * .8), int(JOHN_P.height * .8))); paste(im, q, 360, 1200 - q.height / 2 + 120 * (1 - pj), pj)
        if T > wt(3, "johnqt"): ribbon(im, "EL ÚNICO QUE SIGUE", 360, 1220, T, wt(3, "johnqt"), INK, WHITE, 44, "mm")
        return im
    if name == "L4":     # OXY
        cf = clip(OXYV, 51.2, 3.6, (0, 0, 720, 720), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .5)
        paste(im, OXY_P, 360, 1290 - OXY_P.height / 2 + 100 * (1 - eo(clamp01(t / .4))), clamp01(t * 4))
        word(im, "primero llegó", IT(400, 56), 360, 160, T, SEG["L4"] + .05, LILL); slam(im, "OXY", ANTON(190), 360, 300, T, SEG["L4"] + .1, WHITE)
        pop(im, namechip("EX CLOUD9 · DUELISTA", WHITE, PUR, 40), 360, 450, T, wt(4, "Cloud9"), .35); return im
    if name == "L5":     # brawk campeón del mundo 2025
        cf = clip(BRAWK, 12, 6, (0, 140, 720, 580), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .7)
        paste(im, vcard(BRAWK, 5.0, 1.0, (200, 0, 440, 720), (380, 620), t * .2), 360, 920, clamp01(t * 3))
        word(im, "después", IT(400, 56), 360, 150, T, SEG["L5"] + .05, LILL); slam(im, "BRAWK", ANTON(180), 360, 280, T, SEG["L5"] + .1, WHITE)
        ribbon(im, "CAMPEÓN DEL MUNDO 2025", 360, 430, T, wt(5, "campeón"), WHITE, PUR, 58, "mm")
        if T > wt(5, "campeón"): confetti(im, T, wt(5, "campeón"))
        return im
    if name == "L6":     # canezerra vuelve
        im = bg("p", "VUELVE"); paste(im, vcard(CANE, 8.4, 1.6, (0, 60, 720, 600), (560, 467), t), 360, 520, clamp01(t * 3))
        word(im, "luego", IT(400, 56), 360, 120, T, SEG["L6"] + .05, LILL); slam(im, "CANEZERRA", ANTON(120), 360, 210, T, SEG["L6"] + .1, WHITE)
        stamp(im, "VUELVE", 360, 860, T, wt(6, "vuelve"), (255, 255, 255), -8, 110)
        word(im, "tras una suspensión", IT(900, 50), 360, 1010, T, wt(6, "suspensión") - .1, LILL); particles(im, T, WHITE, .4); return im
    if name == "L7":     # keiko, la pieza final
        cf = clip(KEIKO, 3.2, 5, (0, 0, 720, 720), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .45)
        word(im, "y el lunes", IT(400, 52), 360, 140, T, SEG["L7"] + .05, LILL)
        ribbon(im, "LA PIEZA FINAL", 360, 250, T, wt(7, "pieza") - .1, WHITE, PUR, 70, "mm")
        slam(im, "KEIKO", ANTON(200), 360, 960, T, SEG["L7"] + .15, WHITE)
        pop(im, namechip("CONTROLADOR · REINO UNIDO", WHITE, PUR, 38), 360, 1100, T, wt(7, "controlador"), .35)
        pop(im, namechip("VIENE DE NRG", INK, WHITE, 38), 360, 1190, T, wt(7, "NRG"), .35); return im
    if name == "L8":     # historial de keiko
        im = bg("w", "KEIKO"); paste(im, vcard(KEIKO, 13.8, 1.6, (120, 0, 480, 720), (300, 450), t), 360, 960, clamp01(t * 3))
        for j, (top, sub, t0) in enumerate((("TEAM LIQUID · 2025", "campeón VCT EMEA Stage 2", SEG["L8"] + .1), ("NRG · 2026", "3° en todas las etapas de Américas", wt(8, "NRG")))):
            p = eo(prog(T, t0, t0 + .35))
            if p <= 0: continue
            c = Image.new("RGBA", (600, 150)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 599, 149), 30, fill=(PUR if j == 0 else INK) + (255,))
            d.text((300, 52), top, font=ANTON(52), fill=WHITE, anchor="mm"); d.text((300, 108), sub, font=SANS(600, 26), fill=LILL, anchor="mm")
            paste(im, shadow(c, 10, 10, .3), lerp(-320, 360, p) if j == 0 else lerp(W + 320, 360, p), 230 + j * 200, p)
        return im
    if name == "L9":     # reencuentro con brawk
        im = bg("p", "NRG"); word(im, "y lo mejor:", IT(400, 56), 360, 140, T, SEG["L9"] + .05, LILL)
        ribbon(im, "SE REENCUENTRAN", 360, 250, T, wt(9, "reencuentra"), WHITE, PUR, 70, "mm")
        p1 = eo(prog(T, SEG["L9"] + .1, SEG["L9"] + .5)); p2 = eo(prog(T, wt(9, "brawk"), wt(9, "brawk") + .4))
        paste(im, vcard(KEIKO, 4, 3, (150, 0, 420, 720), (290, 497), t), lerp(-200, 190, p1), 700, p1)
        paste(im, vcard(BRAWK, 5.0, 1.0, (150, 0, 420, 720), (290, 497), t * .2), lerp(W + 200, 530, p2), 700, p2)
        pop(im, namechip("KEIKO", WHITE, PUR, 40), 190, 990, T, SEG["L9"] + .3, .3); pop(im, namechip("BRAWK", WHITE, PUR, 40), 530, 990, T, wt(9, "brawk") + .1, .3)
        slam(im, "+", ANTON(140), 360, 700, T, wt(9, "brawk"), WHITE)
        ribbon(im, "EX COMPAÑEROS EN NRG", 360, 1110, T, wt(9, "compañero"), INK, WHITE, 44, "mm"); particles(im, T, WHITE, .4); return im
    if name == "L10":    # Zellsis sexto jugador
        cf = clip(ZELL, 60, 4, (0, 0, 720, 720), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .45)
        slam(im, "ZELLSIS", ANTON(150), 360, 200, T, SEG["L10"] + .1, WHITE)
        ribbon(im, "VUELVE COMO SEXTO JUGADOR", 360, 340, T, wt(10, "sexto") - .2, WHITE, PUR, 48, "mm")
        pop(im, namechip("“ZADDY'S BACK”", INK, WHITE, 44), 360, 1150, T, wt(10, "vuelve"), .35); return im
    return cta(T)

def cta(T):
    t = T - SEG["cta"]; im = bg("w", "SEN")
    pop(im, senlogo(110, PUR), 360, 130, T, SEG["cta"] + .05, .35)
    word(im, "¿Este Sentinels vuelve a", IT(400, 50), 360, 240, T, SEG["cta"] + .1, INK)
    slam(im, "UN INTERNACIONAL?", ANTON(92), 360, 340, T, wt(11, "internacional"), PUR)
    tc = wt(11, "comentarios")
    if T > tc: pop(im, U.COMMENT, 360, 480 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 360, 570, T, tc + .05, PUR)
    ts = wt(12, "Sígueme")
    if T > ts:
        clicked = T > ts + .6; pop(im, U.follow_btn(clicked), 360, 670, T, ts, .35)
        cp = eo(prog(T, ts + .1, ts + .6)); paste(im, R.CURSOR, lerp(620, 420, cp), lerp(880, 690, cp), clamp01(cp * 3), "lt")
    tsh = wt(12, "compártelo")
    if T > tsh: pop(im, U.SHARE.resize((110, 110)), 140, 810, T, tsh, .35); word(im, "comparte", IT(900, 32), 140, 880, T, tsh + .1, PUR)
    tg = wt(12, "guárdalo")
    if T > tg: f = eo(prog(T, tg + .1, tg + .6)); pop(im, U.icon_save(120, f), 580, 810, T, tg, .35); word(im, "guárdalo", IT(900, 32), 580, 890, T, tg + .1, PUR)
    for j, (ph, x) in enumerate(((CANE_P, 150), (JOHN_P, 360), (OXY_P, 570))):
        q = ph.resize((int(ph.width * .36), int(ph.height * .36))); paste(im, q, x, 1215 - q.height / 2 + 6 * math.sin(T * 2 + j), clamp01((t - .3) * 3))
    for j, s_ in enumerate(("Fuentes: Insider Gaming · esportsinsider · Hotspawn · THESPIKE.GG · 16–17 nov 2026", "Clips: anuncios oficiales de Sentinels · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 1225 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L4", "L5", "L6", "L7", "L9", "L10"}
HITS = []
def hits():
    if not HITS: HITS.extend([.05, .95, wt(0, "superequipo") - .2, wt(1, "fondo"), wt(2, "Champions") + .4, wt(3, "cuatro"), wt(4, "OXY"), wt(5, "brawk"), wt(5, "campeón"),
                              wt(6, "vuelve"), wt(7, "keiko"), wt(9, "brawk"), wt(10, "Zellsis")])
    return HITS
KICK = {"L1": "FONDO", "L2": "2026", "L3": "REBUILD", "L4": "OXY", "L5": "BRAWK", "L6": "CANEZERRA", "L7": "KEIKO", "L8": "KEIKO", "L9": "NRG", "L10": "ZELLSIS", "cta": "2027"}
_kc = {}
def kicker(img, name, dc):
    if name not in KICK or dc > 1.1: return
    col = WHITE if name in PURPLE_SC else PUR
    if name not in _kc:
        f = ANTON(300); txt = KICK[name]; w = int(f.getlength(txt)) + 40; lay = Image.new("RGBA", (w, 380)); ImageDraw.Draw(lay).text((20, 190), txt, font=f, fill=(0, 0, 0, 0), anchor="lm", stroke_width=6, stroke_fill=col + (255,)); _kc[name] = lay
    lay = _kc[name]; p = dc / 1.1; x = lerp(W + lay.width / 2, -lay.width / 2, eo(p) * .55 + p * .45)
    paste(img, lay, x, 640, .55 * (1 - p) ** .7)
def frame(T):
    name = [n for n in ORDER if T >= SEG[n]][-1]; idx = ORDER.index(name); img = scene(name, T); dc = T - SEG[name]
    nxt = SEG[ORDER[idx + 1]] if idx + 1 < len(ORDER) else DUR
    img = scale_about(img, 1 + .035 * clamp01(dc / max(1, nxt - SEG[name])), bg=WHITE + (255,))
    kicker(img, name, dc)
    particles(img, T + idx * 7, WHITE if name in PURPLE_SC else LIL, .3)
    if idx % 2 == 0: brackets(img, dc, WHITE if name in PURPLE_SC else PUR, .8)
    paste(img, text_layer("@DuplexDragon_", SANS(600, 18), WHITE if name in PURPLE_SC else PUR), 690, 60, .7, "rm")
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
        v = rd(os.path.join(SD, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    Sx = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "clink", "boom", "cheer", "braam", "hit808", "glitch", "swoosh", "riser", "crowd", "typing")}
    ev = [("braam", 0.0, .75), ("hit808", 0.0, .7)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("pop", wt(2, "Masters"), .45), ("pop", wt(2, "Masters") + .25, .45), ("pop", wt(2, "Champions"), .45)] + [("pop", wt(3, "fichajes") + j * .1, .4) for j in range(5)] + [
        ("shimmer", wt(5, "campeón"), .6), ("cheer", wt(5, "campeón"), .3), ("riser", wt(7, "keiko") - 1.6, .5), ("braam", wt(7, "keiko"), .7),
        ("pop", wt(8, "Liquid"), .5), ("pop", wt(8, "NRG"), .5), ("whoosh", wt(9, "brawk"), .5), ("crowd", wt(9, "compañero"), .3),
        ("pop", wt(11, "comentarios"), .6), ("pop", wt(12, "Sígueme") + .6, .7), ("whoosh", wt(12, "compártelo"), .5), ("pop", wt(12, "guárdalo") + .1, .6)]
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(SD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(SD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(SD, "sfx.wav"), "-filter_complex",
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
    out = a[0]; mix = os.path.join(SD, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
