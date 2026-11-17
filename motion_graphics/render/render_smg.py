#!/usr/bin/env python3
"""SMG: 4 DUELISTAS POR ERROR (Game Changers Championship 2023) — motion graphics, estética morada.
Abre con la voz original del narrador (clip oficial VCT), luego frase motivacional y narración de Andrés (eleven_v4, 1.1x).
Uso: python3 render_smg.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, wave, json, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_loud as L
from render_loud import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                         scale_about, fade_bottom, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, player_orbit,
                         rcard, chip, flag, brackets, puzzle_tile, CHB, LUTA, eio, U, R, chain_band)
HERE = os.path.dirname(os.path.abspath(__file__)); DD = os.path.join(HERE, "..", "duel"); FPS = 30
REF2 = os.path.join(DD, "ref", "r2.mp4"); REF1 = os.path.join(DD, "ref", "r1.mp4")
SONG = L.SONG; SONG_AT = 82.0

# ---------------- línea de tiempo: clips originales + frases ----------------
N = 15; DL, WT = [], []   # 0-13 guion, 14 = gancho (va primero)
for i in range(N):
    w = wave.open(os.path.join(DD, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(DD, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
    for ch, a in zip(al["characters"], al["character_start_times_seconds"]):
        if ch.isspace():
            if cur: ws.append((cur, st)); cur = ""
        else:
            if not cur: st = a
            cur += ch
    if cur: ws.append((cur, st))
    WT.append(ws)
ORIG_A = [(0.0, 3.3, "¡Espera, espera, espera!"), (8.4, 10.4, "¿Solo los marcaron… o los bloquearon?"), (11.6, 13.7, "¿Qué diablos es esto?")]
ORIG_B = [(13.7, 16.7, "Fue un error honesto de nuestra parte."), (16.7, 19.5, "Pensamos que era una prueba de ping, como un ensayo.")]
TL = []; t = .1
for s, e, sub in ORIG_A: TL.append(("orig", s, e, sub, t)); t += e - s
t += .15
LS = [0.0] * N
for i in [14] + list(range(14)):
    if i == 7:
        t += .1
        for s, e, sub in ORIG_B: TL.append(("orig", s, e, sub, t)); t += e - s
        t += .2
    LS[i] = t; t += DL[i] + .22
DUR = t + 1.2
B0 = [x[4] for x in TL if x[1] == ORIG_B[0][0]][0]; B1 = B0 + sum(e - s for s, e, _ in ORIG_B)
# escenas: 0 intro (clips del narrador), 1..12 = frases 0..11, 13 = prensa de enerii (entre frase 6 y 7), cierre = frases 12-13
SEG = {"intro": 0.0, "H": LS[14] - .1}
for i in range(12): SEG[f"L{i}"] = LS[i] - .1
SEG["prensa"] = B0 - .1; SEG["cta"] = LS[12] - .1
ORDER = sorted(SEG, key=SEG.get)
def wt(k, s, n=0):
    hits = [st for w_, st in WT[k] if s.lower() in w_.lower()]
    return LS[k] + (hits[min(n, len(hits) - 1)] if hits else 0)

# ---------------- recursos ----------------
def cutp(path, w, fade=.16):
    im = duo(Image.open(path).convert("RGBA"), 1.08); im = fade_bottom(im, fade); return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
RC = os.path.join(DD, "rec")
def side_fade(im, frac=.1):
    a = np.asarray(im).copy().astype(np.float32); w = a.shape[1]; x = np.arange(w)[None, :]
    a[..., 3] *= np.clip(np.minimum(x, w - 1 - x) / (w * frac), 0, 1); return Image.fromarray(a.astype(np.uint8))
def _teamph(n, hh=440):
    im = cutp(os.path.join(RC, n + ".png"), 330); sc = hh / im.height
    if sc < 1: im = im.resize((int(im.width * sc), hh), Image.LANCZOS)
    return side_fade(im)
TEAM = {n: _teamph(n) for n in ("kamiyu", "kohaibi", "enerii", "alexy", "shirazi")}
ENERII = cutp(os.path.join(RC, "enerii.png"), 600); ENERII_S = cutp(os.path.join(RC, "enerii.png"), 420)
def logo(name, h=None, w=None, col=WHITE):
    im = Image.open(os.path.join(DD, "logos", name)).convert("RGBA"); sc = h / im.height if h else w / im.width
    return R.tint(im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS), col)
GCC = logo("gcc_w.png", w=520, col=WHITE); SMG_W = logo("smg_w.png", h=260); SMG_I = logo("smg_icono.png", h=200)
EG_W = logo("eg_w.png", h=220); SMG_P = logo("smg_icono.png", h=90, col=PUR); EG_P = logo("eg_w.png", h=90, col=PUR)
AG = {n: duo(Image.open(os.path.join(DD, "agentes", n + ".png")).convert("RGBA"), 1.05) for n in ("neon", "raze", "reyna", "phoenix", "cypher")}
AGI = {n: Image.open(os.path.join(DD, "agentes", n + "_icon.png")).convert("RGBA") for n in AG}
LOTUS = Image.open(os.path.join(L.LD, "mapas", "lotus.jpg")).convert("RGBA")
def _agcrop(n, hh=430):
    a = AG[n]; a = a.crop(a.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox()); return a.resize((int(a.width * hh / a.height), hh), Image.LANCZOS)
AGC = {n: _agcrop(n) for n in ("neon", "raze", "reyna", "phoenix")}
ICON_CY = [R.HAB[k] for k in ("cypher_0", "cypher_1", "cypher_2", "cypher_3") * 2 if k in R.HAB]

# ---------------- clips (duotono morado) ----------------
_cl = {}
def clip(path, t0, dur, crop, size, t, fps=30):
    key = (path, t0, crop, size)
    if key not in _cl:
        x, y, w, h = crop
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(dur), "-i", path, "-vf",
                              f"fps={fps},crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:force_original_aspect_ratio=increase,crop={size[0]}:{size[1]},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        _cl[key] = np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0])
    fr = _cl[key]; g = fr[int(np.clip(t * fps, 0, len(fr) - 1))].astype(np.float32)
    lo, hi = np.percentile(g[::4, ::4], (1, 99)); g = np.clip((g - lo) / max(1, hi - lo) * 255 * 1.05, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([LUTA[g], np.full(g.shape, 255, np.uint8)]), "RGBA")

def subtitle(im, txt, y=1120, a=1.0):
    f = ANTON(46); lines = []; cur = ""
    for w_ in txt.split():
        if f.getlength((cur + " " + w_).strip()) > 600: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    lines.append(cur)
    for j, ln in enumerate(lines):
        l = text_layer(ln.upper(), f, WHITE); b = Image.new("RGBA", (l.width + 36, l.height + 18), INK + (215,)); b.alpha_composite(l, (18, 9))
        paste(im, b, 360, y + j * 70, a)

GROUP = cutp(os.path.join(RC, "equipo.png"), 600, .14)
def lineup(im, T, t0, y=1280, names=True, a=1.0):
    """Foto oficial del equipo SMG (Game Changers Championship São Paulo) que sube con rebote."""
    p = ease_back(prog(T, t0, t0 + .5), 1.3)
    if p <= 0: return
    g = GROUP; zs = 1 + .02 * max(0, T - t0); g2 = g.resize((int(g.width * zs), int(g.height * zs)))
    paste(im, g2, 360 + math.sin(T * 1.2) * 4, y - g2.height / 2 + 220 * (1 - p), clamp01(p * 2) * a)
    if names and T > t0 + .5:
        tg = text_layer("enerii · Kohaibi · Alexy · shirazi · Kamiyu", IT(900, 30), WHITE); b = Image.new("RGBA", (tg.width + 30, tg.height + 10), PUR + (225,)); b.alpha_composite(tg, (15, 5))
        paste(im, b, 360, min(y - 40, 1225), clamp01((T - t0 - .5) * 4))

def ping_meter(im, T, t0, x, y):
    p = clamp01((T - t0) * 3)
    if p <= 0: return
    c = Image.new("RGBA", (300, 120)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 299, 119), 30, fill=WHITE + (255,))
    for k in range(4):
        on = (int(T * 4) + k) % 5 != 0; hh = 20 + k * 16
        d.rectangle((30 + k * 26, 90 - hh, 48 + k * 26, 90), fill=(PUR if on else LILL) + (255,))
    ms = 12 + int(6 * abs(math.sin(T * 3))); d.text((210, 60), f"{ms} ms", font=ANTON(48), fill=PUR, anchor="mm")
    paste(im, shadow(c, 12, 12, .3), x, y, p)

def stamp(im, txt, x, y, T, t0, col=(200, 30, 60), rot=-12, size=120):
    p = prog(T, t0, t0 + .18)
    if p <= 0: return
    f = ANTON(size); tw = int(f.getlength(txt)) + 60; s = Image.new("RGBA", (tw, int(size * 1.4))); d = ImageDraw.Draw(s)
    d.rounded_rectangle((4, 4, tw - 5, s.height - 5), 18, outline=col + (255,), width=10); d.text((tw / 2, s.height / 2 + 4), txt, font=f, fill=col, anchor="mm")
    s = s.rotate(rot, expand=True, resample=Image.BICUBIC); sc = lerp(2.2, 1, eo(p)); s = s.resize((int(s.width * sc), int(s.height * sc)))
    paste(im, s, x, y, clamp01(p * 3))

def flag_br(im, T, t0, y=640, h=260):
    p = eo(prog(T, t0, t0 + .6))
    if p <= 0: return
    lay = canvas(); d = ImageDraw.Draw(lay); y0 = y - h / 2
    pts = [(x, y0 + 22 * math.sin(x / 90 + T * 3)) for x in range(-20, int(W * p) + 30, 10)]
    d.polygon(pts + [(x, yy + h) for x, yy in reversed(pts)], fill=(0, 156, 59, 230))
    cx = W * p / 2; d.polygon([(cx - 260, y), (cx, y - h * .42), (cx + 260, y), (cx, y + h * .42)], fill=(255, 223, 0, 235))
    d.ellipse((cx - 85, y - 85, cx + 85, y + 85), fill=(0, 39, 118, 240)); lay = lay.filter(ImageFilter.GaussianBlur(.6)); im.alpha_composite(lay)

# ---------------- escenas ----------------
def scene(name, T):
    t = T - SEG[name]
    if name == "intro":   # todo el equipo + la voz original del narrador
        im = bg("p", "SMG"); stripes(im, T, 0, WHITE); ring(im, 360, 1000, 330, T, LILL, .5)
        slam(im, "4 DUELISTAS…", ANTON(84), 340, 120, T, .05, WHITE)
        lineup(im, T, .05, 1340)
        cur = [x for x in TL if x[4] <= T][-1] if T >= TL[0][4] else TL[0]
        cf = clip(REF2, cur[1], cur[2] - cur[1] + .2, (0, 300, 576, 420), (560, 410), T - cur[4])
        sc = 1 + .06 * math.exp(-(T - cur[4]) * 8); c = rcard(cf, 26, WHITE); c = c.resize((int(c.width * sc), int(c.height * sc)))
        paste(im, c, 360 + random.Random(int(T * 30)).uniform(-3, 3) * (T - cur[4] < .25), 410, clamp01(t * 4))
        ribbon(im, "EN VIVO · GAME CHANGERS 2023", 360, 660, T, .2, WHITE, PUR, 40, "mm")
        subtitle(im, cur[3], 750); stamp(im, "POR ERROR", 470, 540, T, .7, (255, 255, 255), -9, 54); particles(im, T, WHITE, .4); return im
    if name == "H":      # gancho: eligieron 4 duelistas por error y aun así ganaron
        im = bg("w", "4"); stripes(im, T, SEG["H"], PUR, .5)
        word(im, "este equipo eligió", IT(400, 56), 360, 160, T, wt(14, "equipo"), INK)
        slam(im, "4 DUELISTAS", ANTON(120), 360, 270, T, wt(14, "cuatro"), PUR)
        for j, n in enumerate(("neon", "raze", "reyna", "phoenix")):
            t0 = SEG["H"] + .1 + j * .12; p = ease_back(prog(T, t0, t0 + .35), 1.4)
            if p > 0: paste(im, AGC[n], 110 + j * 167, 640 + 200 * (1 - p) + math.sin(T * 2 + j) * 5, clamp01(p * 2))
        stamp(im, "POR ERROR", 360, 640, T, wt(14, "error"), (200, 30, 60), -10, 110)
        ribbon(im, "Y AUN ASÍ GANÓ", 360, 980, T, wt(14, "ganó") - .1, PUR, WHITE, 76, "mm")
        if T > wt(14, "ganó"): confetti(im, T, wt(14, "ganó"))
        return im
    if name == "L0":     # frase motivacional
        im = bg("p"); stripes(im, T, SEG["L0"], WHITE); ring(im, 360, 1050, 330, T, WHITE, .45); ring(im, 360, 1050, 280, -T, LILL, .3, 3, 30)
        g = text_layer("ERROR", ANTON(200), (140, 50, 190)); jit = 6 * (int(T * 12) % 2)
        paste(im, g, 360 + jit, 410, eo(clamp01(t * 2)))
        word(im, "A veces", IT(400, 60), 360, 190, T, wt(0, "veces"), LILL)
        slam(im, "EL PEOR ERROR", ANTON(100), 360, 300, T, wt(0, "peor"), WHITE)
        word(im, "termina siendo", IT(400, 56), 360, 520, T, wt(0, "termina"), LILL)
        slam(im, "TU MEJOR JUGADA", ANTON(94), 360, 625, T, wt(0, "mejor"), WHITE)
        lineup(im, T, SEG["L0"] + .1, 1320)
        particles(im, T, WHITE, .5); return im
    if name == "L1":     # Game Changers Championship 2023 · São Paulo
        im = bg("w", "2023"); flag_br(im, T, SEG["L1"] + .2, 900, 300)
        pop(im, R.tint(GCC, PUR), 360, 470, T, wt(1, "Game"), .4)
        ribbon(im, "SÃO PAULO · BRASIL", 360, 1160, T, wt(1, "São"), PUR, WHITE, 56, "mm")
        slam(im, "2023", ANTON(130), 360, 220, T, wt(1, "2023"), PUR); return im
    if name == "L2":     # 34 partidas sin perder
        im = bg("p", "34"); ring(im, 360, 520, 260, T, WHITE, .5)
        pop(im, SMG_W.resize((200, int(SMG_W.height * 200 / SMG_W.width))), 360, 190, T, wt(2, "Team"), .35)
        word(im, "llegaba con una racha de", IT(400, 50), 360, 330, T, wt(2, "llegaba"), LILL)
        counter(im, T, wt(2, "treinta") - .1, wt(2, "partidas"), 0, 34, ANTON(280), 360, 540)
        word(im, "partidas seguidas", IT(900, 60), 360, 760, T, wt(2, "partidas"), WHITE)
        slam(im, "SIN PERDER", ANTON(90), 360, 850, T, wt(2, "perder"), LILL)
        particles(im, T, WHITE, .4); return im
    if name == "L3":     # VS Evil Geniuses
        im = bg("w", "VS"); stripes(im, T, SEG["L3"], PUR, .6)
        p1 = eo(prog(T, SEG["L3"], SEG["L3"] + .4)); p2 = eo(prog(T, SEG["L3"] + .35, SEG["L3"] + .75))
        paste(im, R.tint(SMG_I, PUR).resize((160, int(SMG_I.height * 160 / SMG_I.width))), lerp(-200, 130, p1), 520, p1)
        if p2 > 0: paste(im, R.tint(EG_W, INK).resize((int(EG_W.width * 180 / EG_W.height), 180)), lerp(W + 200, 575, p2), 520, p2)
        slam(im, "VS", ANTON(150), 360, 520, T, min(wt(3, "contra"), SEG["L3"] + .6), PUR)
        word(im, "primer partido", IT(400, 56), 360, 230, T, wt(3, "Primer"), INK)
        ribbon(im, "EVIL GENIUSES", 360, 800, T, wt(3, "Evil"), INK, WHITE, 64, "mm")
        ribbon(im, "#1 DE NORTEAMÉRICA", 360, 920, T, wt(3, "número"), PUR, WHITE, 52, "mm"); return im
    if name == "L4":     # 4 duelistas
        im = bg("p", "4"); cf = clip(REF1, 12, 8, (0, 740, 576, 284), (720, 360), t); im = Image.blend(im, Image.new("RGBA", (W, H), PUR + (255,)), 0)
        paste(im, rcard(cf.resize((620, 300)), 24, WHITE), 360, 1130, clamp01(t * 3) * .9)
        word(im, "en la selección de agentes", IT(400, 46), 360, 160, T, wt(4, "selección"), WHITE)
        slam(im, "4 DUELISTAS", ANTON(120), 360, 270, T, wt(4, "cuatro"), WHITE)
        for j, n in enumerate(("neon", "raze", "reyna", "phoenix")):
            t0 = wt(4, n.capitalize()); p = ease_back(prog(T, t0, t0 + .35), 1.4)
            if p <= 0: continue
            a = AGC[n]; x = 110 + j * 167
            paste(im, a, x, 600 + 200 * (1 - p), clamp01(p * 2))
            ic = R.tint(AGI[n], WHITE).resize((60, 60)); pop(im, ic, x, 860, T, t0 + .1, .3)
            word(im, n.upper(), ANTON(34), x, 920, T, t0 + .1, LILL)
        particles(im, T, WHITE, .4); return im
    if name == "L5":     # enerii en Cypher
        im = bg("w", "CYPHER"); cy = AG["cypher"]; cy = cy.resize((620, int(cy.height * 620 / cy.width)))
        paste(im, cy, 470 + math.sin(T) * 6, 640, .35 * clamp01(t * 2))
        player_orbit(im, ENERII_S, 300, 1290, T, max(0, T - wt(5, "Cypher")), ICON_CY, clamp01(t * 3), 72)
        word(im, "su duelista estrella", IT(400, 52), 360, 170, T, wt(5, "duelista"), INK)
        slam(im, "ENERII", ANTON(140), 360, 290, T, wt(5, "enerii"), PUR)
        stamp(im, "EN CYPHER", 520, 470, T, wt(5, "Cypher"), PUR, 10, 70); return im
    if name == "L6":     # ¿estrategia? no: prueba de ping
        im = bg("p", "?")
        if T < wt(6, "No."): puzzle_tile(im, T, SEG["L6"] + .05, "?", 360, 420, 300, (90, 10, 130))
        word(im, "¿estrategia secreta?", IT(900, 60), 360, 170, T, wt(6, "Estrategia"), WHITE)
        stamp(im, "NO", 360, 430, T, wt(6, "No."), (255, 255, 255), -10, 190)
        word(im, "pensaban que era una", IT(400, 50), 360, 720, T, wt(6, "Pensaban"), LILL)
        slam(im, "PRUEBA DE PING", ANTON(96), 360, 820, T, wt(6, "prueba"), WHITE)
        ping_meter(im, T, wt(6, "ping"), 360, 1010); particles(im, T, WHITE, .4); return im
    if name == "prensa":  # enerii en rueda de prensa (voz original)
        im = bg("w", "ERROR"); cur = [x for x in TL if x[4] <= T][-1]
        cf = clip(REF2, ORIG_B[0][0], ORIG_B[-1][1] - ORIG_B[0][0] + .2, (60, 230, 456, 400), (600, 526), T - B0)
        paste(im, rcard(cf, 28), 360, 560, clamp01(t * 4))
        ribbon(im, "ENERII · RUEDA DE PRENSA", 360, 230, T, SEG["prensa"] + .1, PUR, WHITE, 44, "mm")
        subtitle(im, cur[3], 940); return im
    if name == "L7":     # ya no había vuelta atrás
        im = bg("p", "LOCKED"); L.chain_band(im, T, SEG["L7"] + .05, 1e9, 470, 1); L.chain_band(im, T, SEG["L7"] + .15, 1e9, 820, -1)
        slam(im, "LOCKED IN", ANTON(140), 360, 640, T, wt(7, "vuelta") - .2, WHITE)
        word(im, "sin vuelta atrás", IT(900, 58), 360, 290, T, wt(7, "vuelta"), LILL)
        word(im, "así que jugaron con eso", IT(400, 52), 360, 1000, T, wt(7, "jugaron"), WHITE)
        particles(im, T, WHITE, .4); return im
    if name == "L8":     # 13-3 en Lotus
        cf = clip(REF1, 40, 6, (0, 80, 576, 560), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .35)
        m = LOTUS.resize((600, int(LOTUS.height * 600 / LOTUS.width))); m = duo(m, 1.0)
        paste(im, rcard(m.crop((0, 0, 600, 260)), 26, WHITE), 360, 300, eo(clamp01(t * 3)))
        ribbon(im, "LOTUS", 360, 300, T, SEG["L8"] + .2, WHITE, PUR, 70, "mm")
        slam(im, "13", ANTON(260), 200, 700, T, wt(8, "trece"), WHITE); slam(im, "–", ANTON(200), 360, 690, T, wt(8, "tres"), LILL)
        slam(im, "3", ANTON(260), 520, 700, T, wt(8, "tres"), WHITE)
        paste(im, SMG_P.resize((90, int(SMG_P.height * 90 / SMG_P.width))) if False else R.tint(SMG_I, WHITE).resize((110, int(SMG_I.height * 110 / SMG_I.width))), 200, 900, clamp01((T - wt(8, "trece")) * 3))
        paste(im, R.tint(EG_W, WHITE).resize((80, int(EG_W.height * 80 / EG_W.width))), 520, 900, clamp01((T - wt(8, "tres")) * 3))
        confetti(im, T, wt(8, "tres")); return im
    if name == "L9":     # enerii la mejor del servidor
        im = bg("p", "MVP"); ring(im, 360, 900, 300, T, WHITE, .4)
        player_orbit(im, ENERII_S, 360, 1300, T, t, ICON_CY, clamp01(t * 3), 76, WHITE, LILL)
        word(im, "la mejor del servidor", IT(900, 56), 360, 160, T, wt(9, "mejor"), WHITE)
        slam(im, "ENERII", ANTON(120), 360, 270, T, wt(9, "enerii"), LILL)
        counter(im, T, wt(9, "veintiún") - .1, wt(9, "bajas"), 0, 21, ANTON(170), 200, 470)
        word(im, "bajas", IT(900, 52), 200, 590, T, wt(9, "bajas"), WHITE)
        pop(im, R.tint(AGI["cypher"], WHITE).resize((120, 120)), 540, 470, T, wt(9, "Cypher"), .35)
        word(im, "con Cypher", IT(900, 46), 540, 590, T, wt(9, "Cypher"), WHITE); return im
    if name == "L10":    # técnico de EG + segundo mapa 13-7
        im = bg("w", "2-0"); q = Image.new("RGBA", (640, 230)); d = ImageDraw.Draw(q); d.rounded_rectangle((0, 0, 639, 229), 30, fill=INK + (255,))
        d.text((40, 70), "“Ese mapa fue nuestro", font=IT(900, 44), fill=WHITE, anchor="lm"); d.text((40, 130), "calentamiento”", font=IT(900, 44), fill=WHITE, anchor="lm")
        d.text((40, 192), "— Técnico de Evil Geniuses", font=SANS(600, 24), fill=LILL, anchor="lm")
        p = eo(prog(T, wt(10, "técnico"), wt(10, "técnico") + .4)); paste(im, shadow(q, 14, 14, .3), 360, 330 + 40 * (1 - p), p)
        slam(im, "HAVEN 13–7", ANTON(96), 360, 620, T, wt(10, "segundo"), PUR)
        if T > wt(10, "trece"):
            p = eo(prog(T, wt(10, "trece"), wt(10, "trece") + .4))
            paste(im, R.tint(SMG_I, PUR).resize((150, int(SMG_I.height * 150 / SMG_I.width))), 105, 880, p); paste(im, R.tint(EG_W, INK).resize((100, int(EG_W.height * 100 / EG_W.width))), 620, 880, p)
            slam(im, "2–0", ANTON(170), 360, 880, T, wt(10, "trece") + .1, PUR)
        return im
    if name == "L11":    # cuarto del mundo
        im = bg("p", "4°"); ring(im, 360, 600, 300, T, WHITE, .5)
        paste(im, GCC.resize((380, int(GCC.height * 380 / GCC.width))), 360, 200, clamp01(t * 3))
        slam(im, "4°", ANTON(330), 360, 620, T, wt(11, "cuarto"), WHITE)
        slam(im, "DEL MUNDO", ANTON(100), 360, 860, T, wt(11, "mundo"), LILL)
        lineup(im, T, SEG["L11"] + .1, 1400, False, .85); confetti(im, T, wt(11, "cuarto")); return im
    return cta(T)

def cta(T):
    t = T - SEG["cta"]; im = bg("w", "SMG")
    word(im, "¿Tú jugarías con", IT(400, 56), 360, 150, T, wt(12, "jugarías"), INK)
    slam(im, "4 DUELISTAS?", ANTON(110), 360, 260, T, wt(12, "cuatro"), PUR)
    for j, n in enumerate(("neon", "raze", "reyna", "phoenix")):
        ic = duo(AGI[n], 1.0).resize((110, 110)); c = Image.new("RGBA", (130, 130)); ImageDraw.Draw(c).rounded_rectangle((0, 0, 129, 129), 26, fill=PUR + (255,)); c.alpha_composite(ic, (10, 10))
        hl = int((T - SEG["cta"]) * 2) % 4 == j; c = c.resize((150, 150)) if hl else c
        pop(im, shadow(c, 10, 10, .3), 135 + j * 150, 440 + math.sin(T * 3 + j) * 6, T, wt(12, "cuatro") + j * .1, .3)
    tc = wt(12, "comentarios")
    if T > tc: pop(im, U.COMMENT, 600, 640 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 600, 730, T, tc + .05, PUR)
    ts = wt(13, "Sígueme")
    if T > ts:
        clicked = T > ts + .6; pop(im, U.follow_btn(clicked), 360, 860, T, ts, .35)
        cp = eo(prog(T, ts + .1, ts + .6)); paste(im, R.CURSOR, lerp(650, 420, cp), lerp(1080, 880, cp), clamp01(cp * 3), "lt")
    tsh = wt(13, "compártelo")
    if T > tsh:
        p = eo(prog(T, tsh + .2, tsh + .6)); pop(im, U.SHARE, 200, 1040, T, tsh, .35)
        if p > 0: paste(im, U.SHARE.resize((70, 70)), lerp(200, 330, p), lerp(1040, 920, p), 1 - p)
        word(im, "comparte", IT(900, 36), 200, 1130, T, tsh + .1, PUR)
    tg = wt(13, "guárdalo")
    if T > tg:
        f = eo(prog(T, tg + .1, tg + .6)); pop(im, U.icon_save(150, f), 520, 1040, T, tg, .35); word(im, "guárdalo", IT(900, 36), 520, 1130, T, tg + .1, PUR)
    for j, s_ in enumerate(("Fuentes: vlr.gg · Dexerto · Sportskeeda · VALO2ASIA · ge.globo · 28 nov 2023", "Clips: VCT / Riot Games · SPIN Esports · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0: paste(im, text_layer(s_, SANS(400, 15), (110, 100, 125)), 360, 1235 + j * 22, p)
    particles(im, T, LIL, .35); return im

PURPLE_SC = {"intro", "L0", "L2", "L4", "L6", "L7", "L8", "L9", "L11"}
HITS = []
def hits():
    if not HITS: HITS.extend([TL[1][4], TL[2][4], wt(14, "cuatro"), wt(14, "error"), wt(14, "ganó"), wt(0, "peor"), wt(0, "mejor"), wt(2, "perder"), wt(3, "contra"), wt(4, "cuatro"), wt(5, "Cypher"),
                              wt(6, "No."), wt(7, "vuelta") - .2, wt(8, "tres"), wt(9, "bajas"), wt(10, "trece") + .1, wt(11, "cuarto")])
    return HITS
def impact_fx(img, T):
    for h0 in hits():
        dt = T - h0
        if 0 <= dt < .32:
            amp = 18 * (1 - dt / .32) ** 2; rnd = random.Random(int(T * 1000)); dx, dy = rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)
            big = img.resize((int(W * 1.05), int(H * 1.05)), Image.BILINEAR); ox, oy = (big.width - W) / 2 + dx, (big.height - H) / 2 + dy
            img = big.crop((int(ox), int(oy), int(ox) + W, int(oy) + H))
            if dt < .12:
                r, g, b, a = img.split(); sh = int(10 * (1 - dt / .12)) + 2
                r = r.transform(img.size, Image.AFFINE, (1, 0, -sh, 0, 1, 0)); b = b.transform(img.size, Image.AFFINE, (1, 0, sh, 0, 1, 0)); img = Image.merge("RGBA", (r, g, b, a))
            if dt < .05: img = Image.blend(img, canvas(WHITE + (255,)), .45)
            break
    return img

def frame(T):
    name = [n for n in ORDER if T >= SEG[n]][-1]; idx = ORDER.index(name); img = scene(name, T); dc = T - SEG[name]
    nxt = SEG[ORDER[idx + 1]] if idx + 1 < len(ORDER) else DUR
    img = scale_about(img, 1 + .035 * clamp01(dc / max(1, nxt - SEG[name])), bg=WHITE + (255,))
    particles(img, T + idx * 7, WHITE if name in PURPLE_SC else LIL, .3)
    if idx % 2 == 0: brackets(img, dc, WHITE if name in PURPLE_SC else PUR, .8)
    paste(img, text_layer("@DuplexDragon_", SANS(600, 18), WHITE if name in PURPLE_SC else PUR), 690, 60, .7, "rm")
    if idx > 0 and dc < .18:
        p = dc / .18; lay = canvas(); d = ImageDraw.Draw(lay); x = lerp(-200, W + 900, p)
        d.polygon([(x - 900, 0), (x, 0), (x - 500, H), (x - 1400, H)], fill=PUR + (255,)); img.alpha_composite(lay)
    s = 1 + .06 * (1 - eo(clamp01(dc / .35))) if idx > 0 else 1; img = scale_about(img, s, bg=WHITE + (255,)); img = impact_fx(img, T)
    if T > DUR - .8: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, DUR - .8, DUR - .1))
    return img.convert("RGB")

def audio(out):
    SR = 48000; Ns = int(DUR * SR); vox = np.zeros((Ns, 2), np.float32)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    for i, s in enumerate(LS):
        v = rd(os.path.join(DD, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REF2, "-vn", "-ar", "48000", "-ac", "2", os.path.join(DD, "r2.wav")], check=True)
    orig = rd(os.path.join(DD, "r2.wav")); og = np.zeros((Ns, 2), np.float32)
    for _, s, e, _, t0 in TL:
        seg = orig[int(s * SR):int(e * SR)].copy(); fl = int(.03 * SR); seg[:fl] *= np.linspace(0, 1, fl)[:, None]; seg[-fl:] *= np.linspace(1, 0, fl)[:, None]
        j = int(t0 * SR); n = min(len(seg), Ns - j); og[j:j + n] += seg[:n] * 1.6
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    S = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "clink", "boom", "cheer", "braam", "hit808", "glitch", "swoosh", "riser", "crowd", "typing")}
    ev = [("glitch", 0.0, .5)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [("glitch", x[4], .4) for x in TL] + [
        ("braam", LS[14], .7), ("riser", LS[14] - 1.2, .4), ("cheer", wt(14, "ganó"), .35), ("shimmer", LS[0], .4), ("pop", wt(1, "Game"), .5), ("typing", wt(2, "treinta") - .1, .35)] + [("pop", wt(4, n), .55) for n in ("Neon", "Raze", "Reyna", "Phoenix")] + [
        ("clink", SEG["L7"] + .1, .6), ("braam", wt(8, "tres"), .55), ("crowd", wt(8, "tres") + .1, .4), ("shimmer", wt(9, "bajas"), .5), ("pop", wt(10, "técnico"), .5),
        ("shimmer", wt(11, "cuarto"), .5), ("pop", wt(12, "comentarios"), .6), ("pop", wt(13, "Sígueme") + .6, .7), ("whoosh", wt(13, "compártelo") + .2, .5), ("pop", wt(13, "guárdalo") + .1, .6)]
    for k_, t0, g in ev:
        s = S[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox + og), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(DD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(DD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(DD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(DD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(DD, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.2,aloop=loop=-1:size=2e9[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[md];"
                    f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=first,atrim=0:{DUR},afade=t=out:st={DUR - 1.5}:d=1.5,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(x).resize((W // 2, H // 2)) for x in ts]; sh = Image.new("RGB", (W // 2 * min(6, len(ims)), H // 2 * ((len(ims) + 5) // 6)))
        for k, x in enumerate(ims): sh.paste(x, ((k % 6) * W // 2, (k // 6) * H // 2))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=85); print("preview", {k: round(v, 2) for k, v in SEG.items()}, round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(DD, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
