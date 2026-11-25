#!/usr/bin/env python3
"""xavi8k: campeón de Pacific, sin equipo y con el acuerdo roto (XLG eligió a Zeus) — motion graphics morado.
Voz: Andrés (eleven_v4, 1.1x). Fuentes: Sheep Esports, Philstar, pley.gg, talkesport, vct.today, globalesports.com (sep–nov 2026).
Clip: recap oficial de VCT Pacific sobre Global Esports. Uso: python3 render_xavi.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, wave, json, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_smg as S
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, player_orbit,
                        rcard, brackets, U, R, clip, stamp, cutp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); XD = os.path.join(HERE, "..", "xavi"); FPS = 30
SONG = L.SONG; SONG_AT = 29.3; K1 = os.path.join(XD, "clips", "k1.mp4"); CR = (0, 0, 1080, 1330)   # recorte sin los subtítulos del clip

N = 13; DL, WT = [], []
for i in range(N):
    w = wave.open(os.path.join(XD, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(XD, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
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

# ---------- zona segura TikTok / Instagram ----------
# arriba (barra de búsqueda, flecha) ~0–330 px y abajo (usuario, descripción) ~900–1280 px en el lienzo 720x1280
def SY(y): return y + 110 if y < 400 else (y - 170 if y > 900 else y)
_word, _slam, _ribbon, _stamp, _pop, _counter = word, slam, ribbon, stamp, pop, counter
def word(im, s_, f, x, y, *a, **k): return _word(im, s_, f, x, SY(y), *a, **k)
def slam(im, s_, f, x, y, *a, **k): return _slam(im, s_, f, x, SY(y), *a, **k)
def ribbon(im, txt, x, y, *a, **k): return _ribbon(im, txt, x, SY(y), *a, **k)
def stamp(im, txt, x, y, *a, **k): return _stamp(im, txt, x, SY(y), *a, **k)
def pop(im, img, x, y, *a, **k): return _pop(im, img, x, SY(y), *a, **k)
def counter(im, T, t0, t1, v0, v1, font, x, y, *a, **k): return _counter(im, T, t0, t1, v0, v1, font, x, SY(y), *a, **k)
RC = os.path.join(XD, "rec")
XAVI = cutp(os.path.join(RC, "f1_bren.png"), 560); XAVI_S = cutp(os.path.join(RC, "f1_bren.png"), 380)
ZEUS = cutp(os.path.join(RC, "f2_oasis.png"), 460); ZMJ = cutp(os.path.join(RC, "zmjjkk.png"), 330); D4V = cutp(os.path.join(RC, "d4v41.png"), 330)
_ge = Image.open(os.path.join(XD, "logos", "ge.png")).convert("RGBA")
def ge_logo(h, col=WHITE):
    a = np.asarray(_ge).astype(float); m = np.clip((255 - a[..., :3].min(2) - 30) * 3, 0, 255) * (a[..., 3] / 255)
    im = Image.new("RGBA", _ge.size, col + (255,)); im.putalpha(Image.fromarray(m.astype(np.uint8))); im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
GE_W = ge_logo(150); GE_P = ge_logo(150, PUR)
def flag_ph(w=180, h=120):
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im); d.rectangle((0, 0, w, h / 2), fill=LIL + (255,)); d.rectangle((0, h / 2, w, h), fill=PUR + (255,))
    d.polygon([(0, 0), (h * .87, h / 2), (0, h)], fill=LILL + (255,)); cx, cy, r = h * .3, h / 2, h * .12
    for k in range(8):
        a = k * math.pi / 4; d.line((cx, cy, cx + math.cos(a) * r * 1.9, cy + math.sin(a) * r * 1.9), fill=PUR + (255,), width=max(2, h // 30))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=PUR + (255,))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=255); im.putalpha(m); return shadow(im, 10, 10, .3)
PH = flag_ph()
def chipx(txt, ok, w=520, col=None):
    c = Image.new("RGBA", (w, 100)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, w - 1, 99), 30, fill=(col or (PUR if ok else (200, 30, 60))) + (255,))
    f = ANTON(50)
    while f.getlength(txt) > w - 130: f = ANTON(f.size - 2)
    d.text((32, 50), txt, font=f, fill=WHITE, anchor="lm")
    if ok: c.alpha_composite(L.check(56), (w - 82, 22))
    else: d.line((w - 78, 28, w - 34, 72), fill=WHITE, width=9); d.line((w - 34, 28, w - 78, 72), fill=WHITE, width=9)
    return shadow(c, 10, 10, .3)
def vbg(t0, dur, t, a=.55):
    return Image.blend(clip(K1, t0, dur, CR, (720, 1280), t), canvas(PUR + (255,)), a)

def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # gancho
        im = vbg(23.0, 2.6, t * .8, .6); stripes(im, T, 0, WHITE); ring(im, 360, 1000, 320, T * 1.5, LILL, .45)
        paste(im, XAVI, 360, 1300 - XAVI.height / 2 + 140 * (1 - eo(clamp01(t / .45))), clamp01(t * 5))
        for k, (tx, ok, t0) in enumerate((("1 TÍTULO", True, .15), ("2 INTERNACIONALES", True, .45))):
            p = ease_back(prog(T, t0, t0 + .3), 1.5)
            if p > 0: paste(im, chipx(tx, ok, 560), lerp(-300, 360, p), 240 + k * 100, p)
        if T > wt(0, "mes") - .2:
            slam(im, "Y EN UN MES…", ANTON(84), 360, 440, T, wt(0, "mes") - .2, WHITE)
            stamp(im, "SIN NADA", 360, 590, T, wt(0, "nada"), (255, 255, 255), -9, 110)
        particles(im, T, WHITE, .45); return im
    if name == "L1":     # motivacional
        im = bg("w", "XAVI8K"); SN.graph(im, T, SEG["L1"] + .05, SEG["L1"] + DL[1])
        word(im, "a veces el", IT(400, 52), 360, 150, T, SEG["L1"] + .05, INK); slam(im, "TALENTO", ANTON(130), 360, 250, T, SEG["L1"] + .1, PUR)
        word(im, "no es suficiente…", IT(900, 52), 360, 360, T, wt(1, "suficiente") - .2, INK)
        word(im, "y aun así", IT(400, 52), 360, 970, T, wt(1, "aun"), INK); slam(im, "NO TE RINDES", ANTON(110), 360, 1080, T, wt(1, "rindes") - .2, PUR); return im
    if name == "L2":     # filipino, 5 años
        im = bg("p", "TIER 1"); ring(im, 360, 980, 300, T, WHITE, .4)
        paste(im, XAVI, 360, 1300 - XAVI.height / 2 + 100 * (1 - eo(clamp01(t / .4))), clamp01(t * 4))
        word(im, "Xavier", IT(400, 52), 360, 120, T, SEG["L2"] + .05, LILL); slam(im, "XAVI8K", ANTON(160), 360, 230, T, SEG["L2"] + .1, WHITE)
        word(im, "Juan", IT(400, 52), 360, 340, T, SEG["L2"] + .2, LILL)
        pop(im, PH, 360, 565, T, wt(2, "filipino"), .35)
        counter(im, T, wt(2, "cinco") - .1, wt(2, "años"), 0, 5, ANTON(170), 230, 730); word(im, "años para llegar", IT(900, 40), 470, 700, T, wt(2, "años"), WHITE)
        word(im, "al Tier 1", IT(900, 40), 470, 750, T, wt(2, "Tier"), WHITE); return im
    if name == "L3":     # remontada 0-2 → 3-2
        im = vbg(23.6, 2.0, t * .4, .72); ribbon(im, "FINAL VCT PACIFIC STAGE 2", 360, 120, T, SEG["L3"] + .05, WHITE, PUR, 46, "mm")
        maps = [("SUNSET 11–13", False), ("SPLIT 2–13", False), ("ABYSS 13–10", True), ("LOTUS 13–5", True), ("HAVEN 13–10", True)]
        t_zero = wt(3, "cero"); t_rem = wt(3, "remontaron")
        for k, (tx, ok) in enumerate(maps):
            t0 = (t_zero - .1 + k * .25) if k < 2 else (t_rem - .3 + (k - 2) * .3); p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0: paste(im, chipx(tx, ok, 520), lerp(-300, 360, p), 320 + k * 95, p)
        if T > t_zero: slam(im, "0–2" if T < t_rem else "3–2", ANTON(220), 360, 1035, T, t_zero if T < t_rem else wt(3, "tres", 0), WHITE)
        if T > wt(3, "tres"): confetti(im, T, wt(3, "tres"))
        particles(im, T, WHITE, .4); return im
    if name == "L4":     # primer título + internacionales
        im = vbg(23.0, 2.6, t * .5, .5); ribbon(im, "PRIMER TÍTULO DE SU HISTORIA", 360, 150, T, SEG["L4"] + .05, WHITE, PUR, 50, "mm")
        pop(im, GE_W, 360, 300, T, SEG["L4"] + .15, .35)
        for k, (tx, t0) in enumerate((("MASTERS LONDON", wt(4, "Masters")), ("CHAMPIONS", wt(4, "Champions")))):
            p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p > 0: paste(im, chipx(tx, True, 520), lerp(W + 300, 360, p), 700 + k * 115, p)
        confetti(im, T, SEG["L4"] + .1); return im
    if name == "L5":     # GE cerró
        im = vbg(30.6, 2.0, t * .5, .75); paste(im, GE_W, 360, 400, clamp01(t * 4) * (1 - .5 * prog(T, wt(5, "cerró"), wt(5, "cerró") + .3)))
        word(im, "octubre", IT(900, 56), 360, 120, T, SEG["L5"] + .05, LILL)
        stamp(im, "CERRÓ SU EQUIPO", 360, 280, T, wt(5, "cerró"), (255, 255, 255), -8, 80)
        slam(im, "TODOS A LA CALLE", ANTON(96), 360, 1000, T, wt(5, "Todos") - .1, WHITE)
        word(im, "19 de octubre · ahora es un estudio de IA", SANS(600, 26), 360, 1090, T, wt(5, "Todos"), LILL); return im
    if name == "L6":     # XLG lo quería como líder
        im = bg("w", "CHINA"); stripes(im, T, SEG["L6"], PUR, .6); ring(im, 360, 700, 300, T * 1.6, PUR, .45); ring(im, 360, 700, 250, -T * 1.6, LIL, .35, 3, 26)
        word(im, "entonces llegó China", IT(900, 50), 360, 140, T, SEG["L6"] + .05, PUR)
        pop(im, SN.namechip("XI LAI GAMING", PUR, WHITE, 64), 360, 250 + 6 * math.sin(T * 3), T, SEG["L6"] + .3, .35)
        for ph, x, nm, key in ((ZMJ, 175, "ZmjjKK", "ZmjjKK"), (D4V, 545, "d4v41", "d4v41")):
            t0 = min(wt(6, key) - .1, SEG["L6"] + (.6 if key == "ZmjjKK" else .8)); p = ease_back(prog(T, t0, t0 + .4), 1.4)
            if p > 0:
                paste(im, ph, x, 1150 - ph.height / 2 + 150 * (1 - p), clamp01(p * 2)); pop(im, SN.namechip(nm, INK, WHITE, 34), x, 1010, T, t0 + .2, .3)
        p = ease_back(prog(T, wt(6, "líder") - .2, wt(6, "líder") + .2), 1.4)
        if p > 0: paste(im, XAVI_S, 360, 1250 - XAVI_S.height / 2 + 150 * (1 - p), clamp01(p * 2)); stamp(im, "LÍDER", 360, 760, T, wt(6, "líder"), PUR, -8, 80)
        return im
    if name == "L7":     # superequipo
        im = bg("p", "XLG"); ring(im, 360, 900, 300, T * 1.5, WHITE, .45)
        for ph, x in ((ZMJ, 150), (D4V, 570)): paste(im, ph, x, 1250 - ph.height / 2, .85)
        paste(im, XAVI_S, 360, 1290 - XAVI_S.height / 2, 1)
        slam(im, "SUPEREQUIPO", ANTON(130), 360, 220, T, SEG["L7"] + .1, WHITE); word(im, "con xavi8k al mando", IT(900, 52), 360, 350, T, wt(7, "mando") - .2, LILL)
        particles(im, T, WHITE, .5); return im
    if name == "L8":     # 16 nov: XLG rompe el acuerdo
        im = bg("w", "16 NOV"); L.chain_band(im, T, SEG["L8"] + .05, wt(8, "rompió"), 560, 1); L.chain_band(im, T, SEG["L8"] + .15, wt(8, "rompió") + .05, 880, -1)
        paste(im, XAVI_S, 360, 1300 - XAVI_S.height / 2, clamp01(t * 3))
        slam(im, "16 DE NOVIEMBRE", ANTON(90), 360, 160, T, SEG["L8"] + .1, PUR)
        stamp(im, "ACUERDO ROTO", 360, 720, T, wt(8, "rompió"), (200, 30, 60), -8, 100); return im
    if name == "L9":     # 30 minutos después: Zeus
        im = bg("p", "ZEUS"); ring(im, 360, 390, 170, T * 2, WHITE, .5)
        mins = int(lerp(0, 30, eo(prog(T, SEG["L9"] + .05, wt(9, "después") + .1)))); paste(im, text_layer(f"+{mins} MIN", ANTON(130), WHITE), 360, 390)
        p = ease_back(prog(T, wt(9, "Zeus") - .2, wt(9, "Zeus") + .25), 1.4)
        if p > 0: paste(im, ZEUS, 360, 1300 - ZEUS.height / 2 + 200 * (1 - p), clamp01(p * 2))
        slam(im, "ZEUS", ANTON(170), 360, 560, T, wt(9, "Zeus") - .1, WHITE)
        pop(im, SN.namechip("FILIPINAS · EX TEAM SECRET", WHITE, PUR, 38), 360, 690, T, wt(9, "Zeus") + .2, .35); particles(im, T, WHITE, .45); return im
    if name == "L10":    # xavi8k confirma
        im = bg("w", "LFT"); paste(im, XAVI, 360, 1300 - XAVI.height / 2, clamp01(t * 3))
        c = Image.new("RGBA", (620, 230)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 619, 229), 30, fill=INK + (240,))
        d.text((310, 60), "xavi8k confirmó:", font=SANS(700, 30), fill=LILL, anchor="mm"); d.text((310, 120), "el trato se cayó", font=IT(900, 48), fill=WHITE, anchor="mm")
        d.text((310, 185), "y pronto tendrá equipo nuevo", font=IT(400, 34), fill=LILL, anchor="mm")
        p = eo(prog(T, SEG["L10"] + .1, SEG["L10"] + .5)); paste(im, shadow(c, 12, 12, .3), 360, 420 + 40 * (1 - p), p)
        pop(im, SN.namechip("BUSCANDO EQUIPO", PUR, WHITE, 52), 360, 640, T, wt(10, "pronto"), .35); return im
    return cta(T)

def cta(T):
    t = T - SEG["cta"]; im = bg("w", "XAVI8K")
    word(im, "¿Qué equipo debería", IT(400, 56), 360, 150, T, SEG["cta"] + .1, INK); slam(im, "FICHARLO?", ANTON(130), 360, 260, T, SEG["cta"] + .3, PUR)
    tc = wt(11, "comentarios")
    if T > tc: pop(im, U.COMMENT, 360, 500 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 360, 585, T, tc + .05, PUR)
    ts = wt(12, "Sígueme")
    if T > ts:
        clicked = T > ts + .6; pop(im, U.follow_btn(clicked), 360, 690, T, ts, .35)
        cp = eo(prog(T, ts + .1, ts + .6)); paste(im, R.CURSOR, lerp(620, 420, cp), lerp(900, 710, cp), clamp01(cp * 3), "lt")
    tsh = wt(12, "compártelo")
    if T > tsh: pop(im, U.SHARE.resize((110, 110)), 140, 820, T, tsh, .35); word(im, "comparte", IT(900, 32), 140, 885, T, tsh + .1, PUR)
    tg = wt(12, "guárdalo")
    if T > tg: f = eo(prog(T, tg + .1, tg + .6)); pop(im, U.icon_save(120, f), 560, 820, T, tg, .35); word(im, "guárdalo", IT(900, 32), 560, 895, T, tg + .1, PUR)
    q = XAVI_S.resize((int(XAVI_S.width * .8), int(XAVI_S.height * .8))); paste(im, q, 360, 1215 - q.height / 2 + 6 * math.sin(T * 2), clamp01((t - .2) * 3))
    for j, s_ in enumerate(("Fuentes: Sheep Esports · Philstar · pley.gg · talkesport · vct.today · nov 2026", "Clip: recap oficial de VCT Pacific · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 945 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L3", "L4", "L5", "L7", "L9"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L1": "TALENTO", "L2": "XAVI8K", "L3": "3–2", "L4": "BUSAN", "L5": "CERRADO", "L6": "XLG", "L7": "SUPERTEAM", "L8": "ROTO", "L9": "30 MIN", "L10": "LFT", "cta": "XAVI8K"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, .45, wt(0, "nada"), SEG["L1"] + .1, wt(1, "rindes") - .2, SEG["L2"] + .1, wt(3, "cero"), wt(3, "tres"), wt(5, "cerró"),
                              wt(6, "líder"), SEG["L7"] + .1, wt(8, "rompió"), wt(9, "Zeus") - .1])
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
        v = rd(os.path.join(XD, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    Sx = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "clink", "boom", "cheer", "braam", "hit808", "glitch", "swoosh", "riser", "crowd", "typing")}
    ev = [("braam", 0.0, .75), ("hit808", 0.0, .7)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("pop", .15, .45), ("pop", .45, .45), ("typing", wt(2, "cinco") - .1, .35), ("pop", wt(3, "cero") - .1, .45), ("pop", wt(3, "cero") + .15, .45),
        ("riser", wt(3, "remontaron") - 1.2, .45), ("braam", wt(3, "tres"), .6), ("crowd", wt(3, "tres"), .4), ("shimmer", SEG["L4"] + .1, .6), ("cheer", SEG["L4"] + .1, .3),
        ("pop", wt(4, "Masters"), .5), ("pop", wt(4, "Champions"), .5), ("clink", wt(8, "rompió"), .8), ("impact", wt(8, "rompió"), .5), ("typing", SEG["L9"] + .05, .4),
        ("braam", wt(9, "Zeus") - .1, .6), ("pop", wt(10, "pronto"), .5),
        ("pop", wt(11, "comentarios"), .6), ("pop", wt(12, "Sígueme") + .6, .7), ("whoosh", wt(12, "compártelo"), .5), ("pop", wt(12, "guárdalo") + .1, .6)]
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(XD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(XD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(XD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(XD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(XD, "sfx.wav"), "-filter_complex",
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
    out = a[0]; mix = os.path.join(XD, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
