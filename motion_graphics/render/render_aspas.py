#!/usr/bin/env python3
"""ASPAS RECHAZÓ CHINA Y SE VA A TURQUÍA (FUT Esports, VCT EMEA 2027) — motion graphics morado.
Voz: Andrés (eleven_v4, 1.1x). Fuentes: THESPIKE.GG, Sheep Esports, Strafe, esportnow (10–16 nov 2026).
Uso: python3 render_aspas.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, wave, json, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_smg as S
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, fade_bottom, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, player_orbit,
                        rcard, chip, flag, brackets, puzzle_tile, U, R, clip, stamp, cutp, side_fade, AGC, AGI)
import render_loud as L
HERE = os.path.dirname(os.path.abspath(__file__)); AD = os.path.join(HERE, "..", "aspas"); FPS = 30
MOV = os.path.join(AD, "ref", "fut.mov"); SONG = L.SONG; SONG_AT = 52.0

# ---------------- voz ----------------
N = 15; DL, WT = [], []   # 14 = mención a creadores (va antes del cierre)
for i in range(N):
    w = wave.open(os.path.join(AD, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(AD, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
    for ch, a in zip(al["characters"], al["character_start_times_seconds"]):
        if ch.isspace():
            if cur: ws.append((cur, st)); cur = ""
        else:
            if not cur: st = a
            cur += ch
    if cur: ws.append((cur, st))
    WT.append(ws)
LS = [0.0] * N; t = .15
for i in list(range(12)) + [14, 12, 13]: LS[i] = t; t += DL[i] + .22
DUR = t + 1.2
SEG = {f"L{i}": (LS[i] - .1 if i else 0.0) for i in range(12)}; SEG["L14"] = LS[14] - .1; SEG["cta"] = LS[12] - .1
ORDER = sorted(SEG, key=SEG.get)
def wt(k, s, n=0):
    hits = [st for w_, st in WT[k] if s.lower() in w_.lower()]
    return LS[k] + (hits[min(n, len(hits) - 1)] if hits else 0)

# ---------------- recursos ----------------
RC = os.path.join(AD, "rec")
ASP_M = cutp(os.path.join(RC, "aspas_mibr.png"), 520); ASP_F = cutp(os.path.join(RC, "aspas_fut.png"), 600)
ASP_L = cutp(os.path.join(RC, "aspas_loud.png"), 600, .12); K4 = os.path.join(AD, "clips", "k4.mp4")
ASP_FS = cutp(os.path.join(RC, "aspas_fut.png"), 440); ASP_MS = cutp(os.path.join(RC, "aspas_mibr.png"), 380)
def logo(name, h=None, w=None, col=WHITE, tint=True):
    im = Image.open(os.path.join(AD, "logos", name)).convert("RGBA"); sc = h / im.height if h else w / im.width
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS); return R.tint(im, col) if tint else im
FUT = logo("fut.png", h=260, tint=False); FUT_S = logo("fut.png", h=120, tint=False)
MIBR_W = logo("mibr_w.png", w=360); EMEA_W = logo("emea_w.png", h=300)
PERDO = Image.open(os.path.join(AD, "fotos", "perdomix_cam.png")).convert("RGBA")
SHEEP = Image.open(os.path.join(AD, "fotos", "tuit_sheep.png")).convert("RGBA"); ROSTER = Image.open(os.path.join(AD, "fotos", "tuit_roster.png")).convert("RGBA")
AGJ = None
ICONS = [R.HAB[k] for k in ("jett_0", "raze_0", "neon_0", "jett_1", "raze_1", "neon_1", "jett_2", "raze_2") if k in R.HAB]
CUP = L.CUP if hasattr(L, "CUP") else None

def flag_tr(w=300, h=200):
    im = Image.new("RGBA", (w, h), (227, 10, 23, 255)); d = ImageDraw.Draw(im); cx, cy, r = w * .38, h / 2, h * .25
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE + (255,)); r2 = r * .8; d.ellipse((cx - r2 + r * .25, cy - r2, cx + r2 + r * .25, cy + r2), fill=(227, 10, 23, 255))
    sx, sy, sr = w * .6, h / 2, h * .12; pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5 + math.pi / 2 * 0; rr = sr if k % 2 == 0 else sr * .42; pts.append((sx + rr * math.cos(ang - math.pi / 2 + math.pi / 2), sy + rr * math.sin(ang)))
    d.polygon(pts, fill=WHITE + (255,)); return im
def flag_cn(w=300, h=200):
    im = Image.new("RGBA", (w, h), (222, 41, 16, 255)); d = ImageDraw.Draw(im)
    def star(cx, cy, r):
        pts = [(cx + (r if k % 2 == 0 else r * .4) * math.cos(-math.pi / 2 + k * math.pi / 5), cy + (r if k % 2 == 0 else r * .4) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
        d.polygon(pts, fill=(255, 222, 0, 255))
    star(w * .17, h * .27, h * .16)
    for (fx, fy) in ((.33, .1), (.4, .2), (.4, .35), (.33, .45)): star(w * fx, h * fy, h * .055)
    return im
def flag_card(fl, r=22):
    b = max(4, fl.width // 40); c = Image.new("RGBA", (fl.width + 2 * b, fl.height + 2 * b)); ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), r + b, fill=WHITE + (255,))
    m = Image.new("L", fl.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fl.width - 1, fl.height - 1), r, fill=255); f = fl.copy(); f.putalpha(m); c.alpha_composite(f, (b, b)); return shadow(c, 14, 14, .35)
_FL = {n: Image.open(os.path.join(AD, "rec", f"flag_{n}.png")).convert("RGBA") for n in ("tr", "cn", "br")}
def flag_tr(w=300, h=200): return _FL["tr"].resize((w, h), Image.LANCZOS)
def flag_cn(w=300, h=200): return _FL["cn"].resize((w, h), Image.LANCZOS)
def flag_br(w=300, h=200): return _FL["br"].resize((w, h), Image.LANCZOS)
TR = flag_card(flag_tr()); CN = flag_card(flag_cn())

def wave_flag(im, T, t0, fl, y=640, hgt=280, a=1.0):
    """Bandera ondeando a todo el ancho (se deforma por columnas)."""
    p = eo(prog(T, t0, t0 + .6))
    if p <= 0: return
    big = fl.resize((W + 40, hgt)); arr = np.asarray(big); out = np.zeros((hgt + 60, W + 40, 4), np.uint8)
    for x in range(0, int((W + 40) * p), 4):
        dy = int(22 + 22 * math.sin(x / 90 + T * 3)); out[dy:dy + hgt, x:x + 4] = arr[:, x:x + 4]
    paste(im, Image.fromarray(out), 360, y, a)

_b = Image.open(os.path.join(AD, "rec", "billete.png")).convert("RGBA"); BILL = shadow(_b.resize((150, int(_b.height * 150 / _b.width)), Image.LANCZOS), 6, 6, .3)
def money(im, T, t0, x, y):
    """Fajos de billetes que caen."""
    if T < t0: return
    d = ImageDraw.Draw(im)
    for k in range(14):
        rnd = random.Random(k); tt = T - t0 - k * .06
        if tt < 0: continue
        bx = x + rnd.uniform(-280, 280) + 30 * math.sin(tt * 4 + k); by = -80 + tt * rnd.uniform(900, 1300); ang = rnd.uniform(-25, 25) + tt * 90 * (1 if k % 2 else -1)
        if by > H + 80: continue
        paste(im, BILL.rotate(ang, expand=True, resample=Image.BICUBIC), bx, by)

def pen_sign(im, T, t0, x, y, w=440):
    """Línea de firma que se dibuja sola."""
    p = clamp01((T - t0) / 1.2)
    if p <= 0: return
    d = ImageDraw.Draw(im); pts = [(x - w / 2 + w * u, y + 26 * math.sin(u * 14) * (1 - u * .4)) for u in np.linspace(0, p, 80)]
    if len(pts) > 1: d.line(pts, fill=PUR + (255,), width=7, joint="curve")
    d.line((x - w / 2, y + 48, x + w / 2, y + 48), fill=INK + (120,), width=3)

def roster_chip(name, code, tag=None, col=PUR):
    f = ANTON(52); tw = int(f.getlength(name.upper())); c = Image.new("RGBA", (tw + 150, 86)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, c.width - 1, 85), 43, fill=col + (255,)); d.text((28, 43), name.upper(), font=f, fill=WHITE, anchor="lm")
    fl = flag_tr(54, 36) if code == "TR" else flag_br(54, 36); fb = Image.new("RGBA", (60, 42)); ImageDraw.Draw(fb).rounded_rectangle((0, 0, 59, 41), 6, fill=WHITE + (255,)); fb.alpha_composite(fl, (3, 3)); c.alpha_composite(fb, (tw + 47, 22))
    if tag:
        t_ = text_layer(tag, SANS(700, 24), (90, 70, 110)); c2 = Image.new("RGBA", (max(c.width, t_.width + 50), c.height + 30)); c2.alpha_composite(c, (0, 0)); c2.alpha_composite(t_, (30, 88)); c = c2
    return c

# ---------------- escenas ----------------
def scene(name, T):
    t = T - SEG[name]
    if name == "L0":     # gancho: rechazó millones de China… para irse a Turquía
        im = bg("p", "$$$"); stripes(im, T, 0, WHITE); ring(im, 360, 1000, 320, T, LILL, .45)
        player_orbit(im, ASP_F, 360, 1300 + 120 * (1 - eo(clamp01(t / .45))), T, max(0, t - .2), ICONS, clamp01(t * 5), 66, WHITE, LILL)
        slam(im, "RECHAZÓ MILLONES", ANTON(66), 345, 280, T, .05, WHITE)
        pop(im, CN.resize((180, 120)), 180, 395, T, wt(0, "China"), .35); stamp(im, "NO", 180, 395, T, wt(0, "China") + .35, (255, 255, 255), -12, 78)
        word(im, "para irse a", IT(400, 44), 360, 490, T, wt(0, "irse"), LILL)
        pop(im, TR.resize((180, 120)), 540, 395, T, wt(0, "Turquía") - .05, .35); slam(im, "TURQUÍA", ANTON(92), 360, 575, T, wt(0, "Turquía"), WHITE)
        money(im, T, .1, 360, 600); particles(im, T, WHITE, .4); return im
    if name == "L1":     # frase motivacional: cambias de tablero
        im = bg("w", "GG"); d = ImageDraw.Draw(im); n = 6; s = 90; ox, oy = 360 - n * s / 2, 620 - n * s / 2
        for i in range(n):
            for j in range(n):
                pp = eo(prog(T, SEG["L1"] + (i + j) * .04, SEG["L1"] + .3 + (i + j) * .04))
                if (i + j) % 2 == 0 and pp > 0: d.rectangle((ox + i * s, oy + j * s + 30 * (1 - pp), ox + (i + 1) * s, oy + (j + 1) * s + 30 * (1 - pp)), fill=PUR + (int(60 * pp),))
        k = L.KING if hasattr(L, "KING") else None
        if k is not None:
            kk = k.resize((int(k.width * .55), int(k.height * .55))); flip = math.cos(min(math.pi, max(0, T - wt(1, "cambias")) * 6))
            kk2 = kk.resize((max(1, int(kk.width * abs(flip))), kk.height)); paste(im, kk2, 360, 640 + math.sin(T * 2) * 6)
        word(im, "cuando todos te dan por", IT(400, 52), 360, 170, T, wt(1, "cuando"), INK)
        slam(im, "ACABADO", ANTON(130), 360, 280, T, wt(1, "acabado"), PUR)
        word(im, "cambias de", IT(400, 56), 360, 1000, T, wt(1, "cambias"), INK)
        slam(im, "TABLERO", ANTON(150), 360, 1110, T, wt(1, "tablero"), PUR); return im
    if name == "L2":     # campeón del mundo 2022 con LOUD (foto real con el trofeo 2022)
        cf = clip(K4, 1.5, 6, (394, 0, 236, 420), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .55)
        ring(im, 360, 900, 320, T, WHITE, .4)
        ph = ASP_L.resize((int(ASP_L.width * (1 + .03 * t)), int(ASP_L.height * (1 + .03 * t))))
        paste(im, ph, 360 + math.sin(T * 1.3) * 5, 1300 - ph.height / 2 + 120 * (1 - eo(clamp01(t / .45))), clamp01(t * 4))
        word(im, "Erick", IT(400, 56), 360, 140, T, wt(2, "Erick"), LILL); slam(im, "ASPAS", ANTON(170), 360, 260, T, wt(2, "aspas"), WHITE)
        word(im, "Santos", IT(400, 56), 360, 380, T, wt(2, "Santos"), LILL)
        ribbon(im, "CAMPEÓN DEL MUNDO 2022", 360, 500, T, wt(2, "Campeón"), WHITE, PUR, 58, "mm")
        ribbon(im, "CON LOUD", 360, 600, T, wt(2, "LOUD"), INK, WHITE, 52, "mm")
        if T > wt(2, "Campeón"): confetti(im, T, wt(2, "Campeón"))
        return im
    if name == "L3":     # 2026 peor año, 0 internacionales
        cf = clip(MOV, 24, 8, (0, 340, 500, 680), (720, 1280), t); im = Image.blend(cf, canvas(PUR + (255,)), .55)
        slam(im, "2026", ANTON(200), 360, 230, T, wt(3, "2026"), WHITE); ribbon(im, "SU PEOR AÑO", 360, 380, T, wt(3, "peor"), WHITE, PUR, 70, "mm")
        pop(im, MIBR_W, 360, 560, T, wt(3, "MIBR"), .35)
        counter(im, T, wt(3, "ni"), wt(3, "solo"), 9, 0, ANTON(260), 360, 820)
        word(im, "torneos internacionales", IT(900, 52), 360, 990, T, wt(3, "torneo"), WHITE); return im
    if name == "L4":     # sin Champions por primera vez
        im = bg("w", "CHAMPIONS"); word(im, "por primera vez", IT(400, 56), 360, 170, T, wt(4, "primera"), INK)
        for j, yr in enumerate(("2022", "2023", "2024", "2025", "2026")):
            t0 = SEG["L4"] + .2 + j * .25; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p <= 0: continue
            ok = yr != "2026"; c = Image.new("RGBA", (520, 110)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 519, 109), 30, fill=(PUR if ok else (200, 30, 60)) + (255,))
            d.text((40, 55), "CHAMPIONS " + yr, font=ANTON(54), fill=WHITE, anchor="lm")
            if ok: c.alpha_composite(L.check(60), (440, 25))
            else: d.line((445, 30, 495, 80), fill=WHITE, width=10); d.line((495, 30, 445, 80), fill=WHITE, width=10)
            paste(im, shadow(c, 10, 10, .3), lerp(-300, 360, p), 330 + j * 135, p)
        slam(im, "SIN CHAMPIONS", ANTON(110), 360, 1090, T, wt(4, "Champions"), (200, 30, 60)); return im
    if name == "L5":     # a la banca
        im = bg("p", "BANCA"); cf = clip(MOV, 60, 6, (0, 340, 500, 680), (600, 520), t)
        paste(im, rcard(cf, 26, WHITE), 360, 560, clamp01(t * 3))
        pop(im, MIBR_W.resize((260, int(MIBR_W.height * 260 / MIBR_W.width))), 360, 210, T, wt(5, "MIBR"), .35)
        stamp(im, "A LA BANCA", 360, 900, T, wt(5, "banca"), (255, 255, 255), -8, 110)
        particles(im, T, WHITE, .4); return im
    if name == "L6":     # oferta de China: 7 cifras
        im = bg("w", "CHINA"); wave_flag(im, T, SEG["L6"] + .1, flag_cn(720, 480), 330, 300, .9)
        word(im, "entonces llegó", IT(400, 52), 360, 600, T, wt(6, "Entonces"), INK); slam(im, "CHINA", ANTON(150), 360, 710, T, wt(6, "China"), (200, 30, 60))
        if T >= wt(6, "oferta"):
            v = int(round(lerp(0, 1000000, eo(prog(T, wt(6, "oferta"), wt(6, "cifras")))))); paste(im, text_layer("$" + f"{v:,}".replace(",", "."), ANTON(110), PUR), 360, 900)
        ribbon(im, "7 CIFRAS", 360, 1040, T, wt(6, "siete"), PUR, WHITE, 70, "mm"); money(im, T, wt(6, "cifras"), 360, 1200); return im
    if name == "L7":     # y aspas dijo que no
        im = bg("p", "NO"); paste(im, CN.resize((420, 280)), 360, 520, clamp01(t * 4) * (1 - .5 * prog(T, wt(7, "no"), wt(7, "no") + .3)))
        word(im, "y aspas dijo que", IT(400, 60), 360, 200, T, wt(7, "aspas"), LILL)
        stamp(im, "NO", 360, 520, T, wt(7, "no") - .05, (255, 255, 255), -12, 260); particles(im, T, WHITE, .5); return im
    if name == "L8":     # FUT Esports, Estambul, Turquía
        im = bg("w", "FUT"); wave_flag(im, T, SEG["L8"] + .05, flag_tr(720, 480), 1020, 320, .95)
        pop(im, R.tint(FUT, PUR), 360, 330, T, wt(8, "FUT"), .4)
        slam(im, "FUT ESPORTS", ANTON(100), 360, 560, T, wt(8, "Esports"), PUR)
        ribbon(im, "ESTAMBUL · TURQUÍA", 360, 670, T, wt(8, "Estambul"), INK, WHITE, 52, "mm")
        ribbon(im, "MEJOR PROYECTO PARA COMPETIR", 360, 770, T, wt(8, "proyecto"), PUR, WHITE, 42, "mm"); return im
    if name == "L9":     # primera temporada en EMEA, único no turco
        im = bg("p", "EMEA"); ring(im, 360, 420, 230, T, WHITE, .45)
        pop(im, EMEA_W.resize((int(EMEA_W.width * 220 / EMEA_W.height), 220)), 360, 370, T, wt(9, "EMEA"), .4)
        word(im, "primera temporada en", IT(400, 40), 300, 215, T, wt(9, "primera"), LILL)
        names = ["aspas", "", "", "", ""]
        for j in range(5):
            t0 = wt(9, "único") + j * .1; p = ease_back(prog(T, t0, t0 + .3), 1.4)
            if p <= 0: continue
            fl = flag_br(150, 100) if j == 0 else flag_tr(150, 100); c = flag_card(fl, 16)
            paste(im, c.resize((int(c.width * .85), int(c.height * .85))), 110 + j * 125, 610 + (20 if j == 0 else 0) * math.sin(T * 4), p)
        player_orbit(im, ASP_FS, 360, 1330, T, t, ICONS, clamp01((T - wt(9, "único")) * 3), 60, WHITE, LILL)
        slam(im, "EL ÚNICO NO TURCO", ANTON(80), 360, 770, T, wt(9, "turco"), WHITE); return im
    if name == "L10":    # compañeros
        im = bg("w", "2027"); word(im, "sus compañeros", IT(900, 60), 360, 140, T, wt(10, "compañeros"), PUR)
        rows = [("aspas", "BR", "ex-MIBR", wt(10, "compañeros") + .2), ("Wo0t", "TR", "ex-Heretics · oficial", wt(10, "Woot")), ("yetujey", "TR", "renovó · oficial", wt(10, "yetujey")),
                ("hezacoil", "TR", "según reportes", wt(10, "hezacoil")), ("batujnax", "TR", "según reportes", wt(10, "batujnax"))]
        for j, (n, c_, tag, t0) in enumerate(rows):
            p = eo(prog(T, t0, t0 + .3))
            if p > 0: paste(im, roster_chip(n, c_, tag, PUR if j < 3 else (130, 90, 160)), lerp(-300, 60, p), 270 + j * 150, p, "lm")
        rr = ROSTER.resize((220, int(ROSTER.height * 220 / ROSTER.width))); paste(im, rcard(rr, 18), 585, 1000, clamp01((T - wt(10, "reportes")) * 3)); return im
    if name == "L11":    # falta la firma, FUT ya lo dejó ver
        im = bg("w", "FIRMA"); sh = SHEEP.resize((540, int(SHEEP.height * 540 / SHEEP.width)))
        paste(im, rcard(sh, 22), 360, 265, eo(clamp01(t * 3)))
        word(im, "todavía falta", IT(400, 52), 360, 570, T, wt(11, "falta"), INK); slam(im, "LA FIRMA", ANTON(110), 360, 670, T, wt(11, "firma"), PUR)
        pen_sign(im, T, wt(11, "firma") + .1, 360, 790)
        pop(im, FUT_S, 360, 960, T, wt(11, "FUT"), .35); ribbon(im, "FUT YA LO INSINUÓ EN REDES", 360, 1090, T, wt(11, "redes") - .2, PUR, WHITE, 40, "mm"); return im
    if name == "L14":    # mención: creadores de contenido como Perdomix
        im = bg("p", "TIKTOK"); ring(im, 360, 640, 300, T, WHITE, .4)
        word(im, "varios creadores", IT(900, 52), 330, 200, T, wt(14, "creadores"), WHITE); word(im, "de contenido", IT(400, 46), 330, 265, T, wt(14, "contenido"), LILL)
        cam = duo(PERDO, 1.0); cam = rcard(cam.resize((420, int(cam.height * 420 / cam.width))), 26, WHITE)
        pop(im, cam, 360, 560, T, wt(14, "como"), .4)
        ribbon(im, "@perdomixx", 360, 820, T, wt(14, "Perdomix"), WHITE, PUR, 64, "mm")
        for j, txt in enumerate(("¿aspas en Turquía? 🤯".replace(" 🤯", ""), "el fichaje más random", "¿farmear o ganar?")):
            t0 = wt(14, "hablando") + j * .2; p = eo(prog(T, t0, t0 + .3))
            if p <= 0: continue
            b = text_layer(txt, SANS(600, 30), INK); c = Image.new("RGBA", (b.width + 50, b.height + 30)); ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 24, fill=WHITE + (255,)); c.alpha_composite(b, (25, 15))
            paste(im, shadow(c, 8, 8, .3), (210, 470, 290)[j], 960 + j * 95 + 20 * (1 - p), p)
        particles(im, T, WHITE, .4); return im
    return cta(T)

def cta(T):
    t = T - SEG["cta"]; im = bg("w", "FUT")
    player_orbit(im, ASP_FS, 360, 1300, T, t, ICONS, clamp01(t * 3), 56, PUR, LIL)
    word(im, "¿Le irá bien a aspas", IT(400, 54), 360, 140, T, wt(12, "irá"), INK)
    slam(im, "EN TURQUÍA?", ANTON(110), 360, 250, T, wt(12, "Turquía"), PUR); pop(im, TR.resize((120, 80)), 360, 350, T, wt(12, "Turquía") + .1, .3)
    tc = wt(12, "comentarios")
    if T > tc: pop(im, U.COMMENT, 360, 460 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 360, 550, T, tc + .05, PUR)
    ts = wt(13, "Sígueme")
    if T > ts:
        clicked = T > ts + .6; pop(im, U.follow_btn(clicked), 360, 650, T, ts, .35)
        cp = eo(prog(T, ts + .1, ts + .6)); paste(im, R.CURSOR, lerp(620, 420, cp), lerp(860, 670, cp), clamp01(cp * 3), "lt")
    tsh = wt(13, "compártelo")
    if T > tsh: pop(im, U.SHARE.resize((110, 110)), 110, 790, T, tsh, .35); word(im, "comparte", IT(900, 32), 110, 860, T, tsh + .1, PUR)
    tg = wt(13, "guárdalo")
    if T > tg: f = eo(prog(T, tg + .1, tg + .6)); pop(im, U.icon_save(120, f), 610, 790, T, tg, .35); word(im, "guárdalo", IT(900, 32), 610, 870, T, tg + .1, PUR)
    for j, s_ in enumerate(("Fuentes: THESPIKE.GG · Sheep Esports · Strafe · esportnow · 10–16 nov 2026", "Acuerdo verbal reportado; falta la firma oficial · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 1225 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L2", "L3", "L5", "L7", "L9", "L14"}
HITS = []
def hits():
    if not HITS: HITS.extend([.05, wt(0, "China") + .35, wt(0, "Turquía"), wt(1, "acabado"), wt(1, "tablero"), wt(2, "aspas"), wt(3, "peor"), wt(4, "Champions"), wt(5, "banca"),
                              wt(6, "China"), wt(7, "no") - .05, wt(8, "FUT"), wt(9, "turco"), wt(11, "firma")])
    return HITS
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
        v = rd(os.path.join(AD, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    Sx = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "clink", "boom", "cheer", "braam", "hit808", "glitch", "swoosh", "riser", "crowd", "typing")}
    ev = [("braam", 0.0, .75), ("hit808", 0.0, .7)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("clink", wt(0, "Turquía"), .5), ("shimmer", wt(2, "Campeón"), .6), ("typing", wt(3, "ni"), .35), ("pop", SEG["L4"] + .2, .4), ("pop", SEG["L4"] + .45, .4), ("pop", SEG["L4"] + .7, .4),
        ("pop", SEG["L4"] + .95, .4), ("impact", SEG["L4"] + 1.2, .5), ("typing", wt(6, "oferta"), .35), ("braam", wt(7, "no") - .05, .7), ("shimmer", wt(8, "FUT"), .5),
        ("pop", wt(10, "Woot"), .5), ("pop", wt(10, "yetujey"), .5), ("pop", wt(10, "hezacoil"), .5), ("pop", wt(10, "batujnax"), .5), ("typing", wt(11, "firma") + .1, .4),
        ("pop", wt(14, "como"), .5), ("pop", wt(14, "hablando"), .4), ("pop", wt(14, "hablando") + .2, .4), ("pop", wt(14, "hablando") + .4, .4), ("pop", wt(12, "comentarios"), .6), ("pop", wt(13, "Sígueme") + .6, .7), ("whoosh", wt(13, "compártelo"), .5), ("pop", wt(13, "guárdalo") + .1, .6)]
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(AD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(AD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(AD, "sfx.wav"), "-filter_complex",
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
    out = a[0]; mix = os.path.join(AD, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
