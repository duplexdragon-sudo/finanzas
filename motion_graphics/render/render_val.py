#!/usr/bin/env python3
"""Motion graphic morado de Valorant, 60 s, 9:16. Reutiliza el motor de render.py.
Arte oficial de Riot en ../val/art (fan edit, uso no comercial).
Uso: python3 render_val.py salida.mp4 [--audio cancion.mp3] | --preview t1,t2,...
"""
import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
import render as R
from render import (W, H, FPS, text_layer, paste, word_reveal, typed, wrap, para, rrect, circle, dashed_rect,
                    scale_about, motion_blur_x, motion_blur_y, offset, rotate_y, add_grain, DUST, prog, eo, eio,
                    lerp, SERIF, SANS, fit_cover, corner_frame, canvas, _safe_comp)

HERE = os.path.dirname(os.path.abspath(__file__)); ART = os.path.join(HERE, "..", "val", "art")
DUR = 60.0
NAME = "TU NOMBRE"; USER = "@tu_usuario"; DATE = "13 NOV 2026"; MONTH = "Nov 2026"

# ---------------- paleta morada ----------------
DEEP = (12, 6, 22); PD = (44, 20, 70); MID = (62, 30, 108); ACC = (124, 62, 230); PINK = (205, 80, 205)
LAV = (238, 232, 248); WHITE = (255, 255, 255); SOFT = (222, 214, 238)

def art(name, box=None):
    im = Image.open(os.path.join(ART, name)).convert("RGBA")
    bb = im.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if bb: im = im.crop(bb)
    if box: im.thumbnail(box, Image.LANCZOS)
    return im

def glow(im, color, radius=30, strength=1.0):
    """Halo de color detrás de un recorte."""
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    a = a.point(lambda v: min(255, int(v * 1.6 * strength)))
    pad = radius * 2
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    g = Image.new("RGBA", im.size, color + (255,)); g.putalpha(a)
    out.alpha_composite(g, (pad, pad)); out.alpha_composite(im, (pad, pad))
    return out

AG = {k: art(f"{k}_retrato.png", (620, 760)) for k in ["clove", "reyna", "omen", "fade", "vyse", "iso", "astra"]}
HAB = {k: [art(f"{k}_hab{i}.png", (54, 54)) for i in range(4) if os.path.exists(os.path.join(ART, f"{k}_hab{i}.png"))] for k in AG}
CARDS = [art(f"{k}_carta0.png") for k in ["astra", "clove", "fade", "iso", "omen", "reyna", "vyse"]]
WIDE = fit_cover(Image.open(os.path.join(ART, "omen_carta0_ancha.png")).convert("RGBA"), (392, 300)) \
    if os.path.exists(os.path.join(ART, "omen_carta0_ancha.png")) else fit_cover(CARDS[4], (392, 300))

def tint(im, color, amt):
    c = Image.new("RGBA", im.size, color + (255,)); c.putalpha(im.getchannel("A"))
    out = Image.blend(im, c, amt); out.putalpha(im.getchannel("A")); return out

LEAF_P = R.leaf(PD, 10, .9); LEAF_P2 = R.leaf(PD, 6, .7); LEAF_A = R.leaf(ACC, 14, 1.1)

def tl(s, f, fill=WHITE): return text_layer(s, f, fill)

# ================= 1. póster claro (0–7 s) =================
def bg_light():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .45) / H) ** 2)
    a = np.zeros((H, W, 3), np.float32)
    for i, c in enumerate(LAV): a[..., i] = c + 10 * (1 - np.clip(r * 1.6, 0, 1)) - 10 * np.clip(r - .4, 0, 1)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    grid = canvas(); gd = ImageDraw.Draw(grid)
    for x in range(80, 650, 22): gd.line((x, 360, x, 960), fill=(190, 175, 215, 255))
    for y in range(360, 970, 22): gd.line((80, y, 640, y), fill=(190, 175, 215, 255))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((40, 330, 680, 1000), fill=255)
    grid.putalpha(ImageChops.multiply(grid.getchannel("A"), m.filter(ImageFilter.GaussianBlur(70))))
    im.alpha_composite(grid); return im
BG1 = bg_light()
CLOVE = AG["clove"].copy(); CLOVE.thumbnail((440, 480))
CURSOR = tint(R.CURSOR, PD, 1)
def barcode():
    b = tint(R.BARCODE, PD, 1); return b

def scene1(t):
    im = BG1.copy(); d = ImageDraw.Draw(im)
    pts = [(-40 + 820 * u, 250 - 300 * math.sin(u * 1.2) + 40 * u) for u in [i / 60 for i in range(int(60 * eo(prog(t, .2, 2.0))) + 1)]]
    if len(pts) > 1: d.line(pts, fill=PD + (255,), width=2)
    pts = [(-40 + 820 * u, 1090 + 110 * math.sin(u * 2.4)) for u in [i / 60 for i in range(int(60 * eo(prog(t, 1.0, 3.0))) + 1)]]
    if len(pts) > 1: d.line(pts, fill=PD + (255,), width=2)
    bc = Image.new("RGBA", (130, 60), (0, 0, 0, 0)); bd = ImageDraw.Draw(bc); rr = random.Random(3); x = 4
    while x < 120:
        w = rr.choice([1, 1, 2, 3]); bd.rectangle((x, 22, x + w - 1, 46), fill=PD + (255,)); x += w + rr.choice([1, 2])
    bd.text((65, 10), DATE, font=SANS(400, 13), fill=PD, anchor="mm")
    paste(im, bc, 640, 70, 1, "rm")
    paste(im, tl(NAME, SANS(400, 15), PD), 70, 1195, prog(t, .3, .7), "lm")
    # título tipeado
    if t > .05:
        dashed_rect(ImageDraw.Draw(im), (130, 280, 590, 445), PD + (255,), 6, 4, 2)
        paste(im, tl(typed("un", t, .05, 16), SERIF(800, 34), PD), 150, 308, 1, "lm")
        s = typed("AGENTE", t, .2, 10)
        if s: paste(im, tl(s, SERIF(900, 86), PD), 148, 372, 1, "lm")
        if t > .85: paste(im, tl("de verdad", SERIF(700, 30, True), PD), 575, 420, prog(t, .85, 1.1), "rm")
    # agente: pixelado -> nítido, luego respira
    ps = eo(prog(t, .5, 1.3))
    if ps > 0:
        st = CLOVE
        if ps < 1:
            k = max(1, int(26 * (1 - ps)))
            st = st.resize((max(1, st.width // k), max(1, st.height // k)), Image.NEAREST).resize(st.size, Image.NEAREST)
        sc = 1 + .03 * math.sin(t * 1.3)
        st2 = st.resize((int(st.width * sc), int(st.height * sc)))
        paste(im, st2, 360, 945, ps, "mb")
    word_reveal(im, ["Además", "de", "su", "arma"], SERIF(500, 54), 360, 990, [2.0, 2.25, 2.45, 2.65], PD, t=t)
    pp = eo(prog(t, 3.3, 3.7))
    if pp > 0:
        pill = rrect((400, 48), 4, PD + (255,))
        ImageDraw.Draw(pill).text((200, 24), "¿QUÉ NECESITA UN AGENTE?", font=SERIF(500, 22, True), fill=WHITE, anchor="mm")
        paste(im, pill.crop((0, 0, max(1, int(400 * pp)), 48)), 160, 1052, 1, "lm")
    s = typed("Cada ronda se gana con puntería, pero se recuerda por el estilo. Lo que hace grande a un agente no es su arma: es cómo la usa cuando todo está en juego.", t, 2.4, 70)
    if s: para(im, s, SANS(400, 17), 360, 1100, 560, PD)
    path = [(0, (430, 150)), (.8, (560, 330)), (2.0, (520, 980)), (3.4, (540, 1060)), (7, (580, 1090))]
    for (t0, p0), (t1, p1) in zip(path, path[1:]):
        if t0 <= t <= t1: e = eio(prog(t, t0, t1)); paste(im, CURSOR, lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e), 1, "lt")
    sw = math.sin(t * 1.8) * 8
    paste(im, LEAF_P.rotate(150 + sw, expand=True), -150, -170, .9, "lt")
    paste(im, LEAF_P2.rotate(-30 - sw, expand=True), W + 130, H + 110, .9, "rb")
    return scale_about(im, 1 + .04 * t / 7, bg=LAV + (255,))

# ================= 2. tarjeta 3D (7–14 s) =================
def make_card():
    cw, ch = 430, 500
    c = rrect((cw, ch), 18, (250, 248, 253, 255)); d = ImageDraw.Draw(c)
    d.ellipse((18, 14, 46, 42), fill=(214, 41, 118)); d.ellipse((23, 19, 41, 37), fill=WHITE); d.ellipse((27, 23, 37, 33), fill=(214, 41, 118))
    u = USER.strip("@") + " · "; d.text((56, 28), u, font=SANS(500, 15), fill=(30, 30, 30), anchor="lm")
    d.text((56 + SANS(500, 15).getlength(u), 28), "Follow", font=SANS(600, 15), fill=(0, 149, 246), anchor="lm")
    c.alpha_composite(WIDE, (19, 52)); y = 52 + 300 + 26
    d.ellipse((22, y - 11, 44, y + 11), fill=(237, 73, 86)); d.ellipse((58, y - 11, 80, y + 11), outline=(30, 30, 30), width=2)
    d.polygon([(96, y - 10), (118, y - 2), (100, y + 10)], outline=(30, 30, 30)); d.rectangle((cw - 36, y - 11, cw - 22, y + 11), fill=(30, 30, 30))
    d.text((22, y + 34), "12.480 Likes", font=SANS(500, 16), fill=(30, 30, 30), anchor="lm")
    d.text((22, y + 64), "Clutch 1v4", font=SANS(500, 16), fill=(30, 30, 30), anchor="lm")
    d.text((130, y + 64), "#valorant #clutch", font=SANS(500, 16), fill=(0, 149, 246), anchor="lm")
    full = Image.new("RGBA", (cw + 14, ch + 14), (0, 0, 0, 0))
    full.alpha_composite(rrect((cw, ch), 18, (170, 160, 190, 255)), (12, 12)); full.alpha_composite(c, (0, 0))
    return full
CARD = make_card()
def bg_orbs():
    im = canvas(DEEP + (255,))
    paste(im, circle(170, ACC + (255,), 2), 70, 150); paste(im, circle(140, PINK + (255,), 30), 760, 40)
    paste(im, circle(230, ACC + (230,), 45), 640, 1240); paste(im, circle(150, MID + (255,), 40), 60, 1050)
    ImageDraw.Draw(im).arc((-330, 1060, 130, 1520), 280, 360, fill=(225, 215, 240, 255), width=3)
    return im
BG2 = bg_orbs()
def scene2(t):
    im = BG2.copy()
    corner_frame(ImageDraw.Draw(im), (80, 70, 640, 190), (180, 160, 210, int(255 * prog(t, .1, .5))))
    s = typed("El verdadero impacto no está en el marcador. Está en la jugada que nadie esperaba y en el server que se queda en silencio.", t, .2, 70)
    if s: para(im, s, SANS(400, 18), 360, 88, 520, SOFT)
    e = eo(prog(t, 0, .8)); ang = lerp(48, 6, e) + math.sin(t * 1.2) * 4
    card = CARD.rotate(lerp(-14, 0, e), expand=True, resample=Image.BICUBIC); card, _ = rotate_y(card, ang)
    paste(im, card, lerp(620, 360, e), lerp(1150, 545, e) + math.sin(t * 1.6) * 7)
    word_reveal(im, ["OBVIO,", "QUE", "RESPETEN"], SERIF(500, 36, True), 360, 1010, [1.2, 1.5, 1.8], WHITE, t=t)
    pb = eo(prog(t, 2.4, 2.7))
    if pb > 0: dashed_rect(ImageDraw.Draw(im), (110, 1040, 610, 1114), (235, 225, 245, int(255 * pb)), 9, 6, 2)
    word_reveal(im, ["SU", "JUEGO"], SERIF(900, 52), 360, 1077, [2.5, 2.8], WHITE, t=t)
    s = typed("NO IMPORTA EL RANGO NI EL MAPA. CUANDO LA JUGADA HABLA, TODO EL LOBBY ESCUCHA. CADA FLICK, CADA SMOKE, CADA CLUTCH CONSTRUYE UNA REPUTACIÓN.", t, 3.0, 80)
    if s: para(im, s, SANS(400, 12), 360, 1135, 470, SOFT)
    return im

# ================= 3. roles (14–30 s) =================
def bg_spot():
    im = canvas((8, 4, 16, 255))
    paste(im, circle(340, ACC + (255,), 95), 360, 600); paste(im, circle(170, PINK + (200,), 80), 360, 560)
    ImageDraw.Draw(im).arc((380, -260, 900, 260), 100, 200, fill=ACC + (255,), width=26)
    return im.filter(ImageFilter.GaussianBlur(4))
BG3 = bg_spot()
BUB = [(random.Random(i).randrange(40, 680), random.Random(i + 50).randrange(150, 1200), random.Random(i + 9).randrange(12, 42)) for i in range(10)]
ROLES = [("DUELISTA", "reyna", "REYNA"), ("CONTROLADOR", "omen", "OMEN"), ("INICIADOR", "fade", "FADE"), ("CENTINELA", "vyse", "VYSE")]
AGG = {k: glow(AG[k], ACC, 26, .8) for _, k, _ in ROLES}
def pill_label(txt):
    f = SANS(800, 40); w = int(f.getlength(txt)) + 70
    p = rrect((w, 74), 37, PD + (255,), (240, 232, 250, 255), 3)
    ImageDraw.Draw(p).text((w / 2, 38), txt, font=f, fill=WHITE, anchor="mm"); return p
PILLS = [pill_label(r[0]) for r in ROLES]
def scene3(t):
    im = BG3.copy()
    for i, (x, y, r) in enumerate(BUB):
        paste(im, circle(r, (ACC if i % 2 else PINK) + (255,), 0 if i % 3 else 6), x + math.sin(t + i) * 8, (y - t * (16 + i * 3)) % 1300 - 10, .85)
    word_reveal(im, ["Ya", "sea"], SERIF(900, 38), 360, 200, [.1, .3], WHITE, t=t)
    seg = 4.0; idx = min(3, int(t // seg)); lt = t - idx * seg
    e = eo(prog(lt, 0, .35)) if idx > 0 else eo(prog(t, 0, .5))
    ox = (1 - e) * 600
    if idx < 3 and lt > seg - .3: ox = -eo(prog(lt, seg - .3, seg)) * 600
    role, k, nm = ROLES[idx]
    sc = 1 + .05 * lt / seg; a = AGG[k]; a2 = a.resize((int(a.width * sc * .92), int(a.height * sc * .92)), Image.BILINEAR)
    layer = canvas(); paste(layer, a2, 360 + ox, 925, 1, "mb")
    paste(layer, PILLS[idx], 360 + ox * .7, 975)
    paste(layer, tl(nm, SERIF(700, 22, True), SOFT), 360 + ox * .5, 1030, prog(lt, .4, .7))
    if abs(ox) > 3: layer = motion_blur_x(layer, ox * .12)
    im.alpha_composite(layer)
    # íconos de habilidades, uno a uno
    hs = HAB[k]; n = len(hs)
    for j, h in enumerate(hs):
        p = eo(prog(lt, .7 + j * .18, 1.0 + j * .18))
        if p > 0 and abs(ox) < 5:
            paste(im, h, 360 + (j - (n - 1) / 2) * 78, 1095 + 14 * (1 - p), p)
    para(im, "Cada rol tiene su forma de ganar una ronda. Unos entran primero, otros cierran el mapa, otros leen al rival antes de que se mueva.", SANS(400, 16), 360, 1150, 600, SOFT, prog(t, .4, .8))
    return scale_about(im, 1 + .02 * lt, bg=(8, 4, 16, 255))

# ================= 4. panel de vidrio (30–42 s) =================
def bg_grad():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); k = np.clip((xx / W * .35 + yy / H * .9) - .25, 0, 1) ** 1.4
    a = np.zeros((H, W, 3), np.float32)
    for i, (c0, c1) in enumerate(zip((6, 3, 10), (90, 40, 150))): a[..., i] = c0 + (c1 - c0) * k
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    bgl = Image.open(os.path.join(ART, "reyna_fondo_letras.png")).convert("RGBA"); bgl.thumbnail((700, 1200))
    paste(im, tint(bgl, (190, 150, 255), .6), 360, 640, .14)
    paste(im, LEAF_A.rotate(140, expand=True), 600, 60, .9); paste(im, LEAF_A.rotate(-20, expand=True), 40, 1250, .6)
    return im
BG4 = bg_grad(); PANEL = (60, 400, 660, 860)
COMMENTS = [("Vale", "@vale.aim", "ese clutch 1v4 fue de otro planeta, el server quedó en silencio"),
            ("Diego", "@dg_smokes", "no sé cómo leíste esa rotación, jugada limpia de principio a fin"),
            ("Mar", "@mar.ttv", "este edit está demasiado bien hecho, todo se siente perfecto")]
def ccard(name, user, txt, face):
    c = rrect((520, 112), 28, (234, 228, 242, 245)); d = ImageDraw.Draw(c)
    av = face.copy(); av = fit_cover(av, (40, 40)); m = Image.new("L", (40, 40), 0); ImageDraw.Draw(m).ellipse((0, 0, 39, 39), fill=255)
    c.paste(av, (20, 16), m)
    d.text((72, 26), name, font=SANS(600, 17), fill=(25, 15, 35), anchor="lm"); d.text((72, 46), user, font=SANS(400, 12), fill=(100, 90, 115), anchor="lm")
    y = 72
    for ln in wrap(txt, SANS(400, 15), 450)[:2]: d.text((40, y), ln, font=SANS(400, 15), fill=(30, 20, 40), anchor="lm"); y += 21
    return c
FACES = [art("astra_icono.png"), art("iso_icono.png"), art("clove_icono.png")]
CC = [ccard(*COMMENTS[i], FACES[i]) for i in range(3)]
def glass(base, box):
    x0, y0, x1, y1 = box
    reg = ImageEnhance.Brightness(base.crop(box).filter(ImageFilter.GaussianBlur(22))).enhance(1.2)
    reg.alpha_composite(Image.new("RGBA", reg.size, (255, 255, 255, 14))); _safe_comp(reg, circle(170, (200, 160, 255, 70), 60), -180, -200)
    m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), 34, fill=255)
    base.paste(reg, (x0, y0), m); ImageDraw.Draw(base).rounded_rectangle(box, 34, outline=(225, 205, 250, 130), width=2)
def scene4(t):
    im = BG4.copy(); layer = im.copy(); glass(layer, PANEL)
    sp = prog(t, .1, .7)
    if 0 < sp < 1:
        sw = canvas(); x = lerp(-200, 900, sp)
        ImageDraw.Draw(sw).polygon([(x, 400), (x + 90, 400), (x - 60, 860), (x - 150, 860)], fill=(255, 255, 255, 50))
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(PANEL, 34, fill=255)
        sw.putalpha(ImageChops.multiply(sw.getchannel("A"), m)); layer.alpha_composite(sw.filter(ImageFilter.GaussianBlur(8)))
    im = Image.blend(im, layer, eo(prog(t, 0, .4)))
    word_reveal(im, ["Lo", "que", "dicen", "en", "el", "chat"], SANS(400, 22), 360, 360, [.6 + .12 * i for i in range(6)], SOFT, t=t)
    for i, st in enumerate([1.0, 2.6, 4.2]):
        e = eo(prog(t, st, st + .5))
        if e > 0:
            # cada comentario cae y los anteriores bajan
            push = sum(eo(prog(t, s2, s2 + .5)) for s2 in [1.0, 2.6, 4.2][i + 1:]) * 128
            y = lerp(330, 500, e) + push
            paste(im, CC[i], 360 + (1 - e) * 30, y, e * (1 - prog(t, 7.6, 8.1)))
    word_reveal(im, ["¿Pero", "quién", "soy", "yo?"], SANS(500, 46), 360, 630, [8.4, 8.8, 9.2, 9.6], WHITE, t=t, offs=[0, -6, 6, 26])
    return im

# ================= 5. muro de cartas (42–50 s) =================
def bg_cards():
    im = canvas(DEEP + (255,)); paste(im, circle(380, MID + (255,), 120), 360, 700); paste(im, circle(200, PINK + (160,), 110), 360, 760)
    return im
BG5 = bg_cards()
CARDS_S = [c.resize((200, 478), Image.LANCZOS) for c in CARDS]
def scene5(t):
    im = BG5.copy(); n = len(CARDS_S)
    order = sorted(range(n), key=lambda i: -abs(i - 3))
    for rank, i in enumerate(order):
        st = rank * .25; e = eo(prog(t, st, st + .7))
        if e <= 0: continue
        off = i - 3; fan = off * 13 * eo(prog(t, 2.2, 3.2)); spread = off * lerp(30, 88, eo(prog(t, 2.2, 3.2)))
        c = CARDS_S[i].rotate(-fan * (1 - .0) + (1 - e) * 40 * (1 if off >= 0 else -1), expand=True, resample=Image.BICUBIC)
        x = 360 + spread + (1 - e) * (300 if off >= 0 else -300)
        y = 690 + abs(off) * abs(off) * 6 * eo(prog(t, 2.2, 3.2)) + (1 - e) * 500
        paste(im, c, x, y + math.sin(t * 1.5 + i) * 5, e)
    word_reveal(im, ["CADA", "RONDA"], SERIF(900, 56), 360, 240, [.4, .7], WHITE, t=t)
    word_reveal(im, ["una", "historia", "distinta"], SERIF(500, 40, True), 360, 310, [1.1, 1.35, 1.6], SOFT, t=t)
    return scale_about(im, 1 + .03 * t / 8, bg=DEEP + (255,))

# ================= 6–7. SOY / RADIANTE (50–60 s) =================
def bg_end():
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32); k = np.clip((yy / H - .45) / .55, 0, 1) ** 1.6
    a = np.zeros((H, W, 3), np.float32)
    for i, (c0, c1) in enumerate(zip((5, 2, 9), (70, 28, 120))): a[..., i] = c0 + (c1 - c0) * k
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA"); paste(im, circle(260, (90, 40, 150, 255), 120), 600, 120, .8); return im
BGE = bg_end()
ISO_DARK = tint(AG["iso"], (40, 18, 70), .55); ISO_DARK = glow(ISO_DARK, ACC, 40, .7)
def scene6(t):  # SOY
    im = BGE.copy(); im.alpha_composite(DUST[int(t * 12) % 6])
    s = lerp(3.2, 1.0, eo(prog(t, 0, 2.0))); l = tl("SOY", SANS(800, int(130 * s)))
    if t < .3: l = l.filter(ImageFilter.GaussianBlur(10 * (1 - t / .3)))
    paste(im, l, 360, 640); return im
CORN = [(NAME, 70, 140, "lm"), ("FAN EDIT", 650, 140, "rm"), (USER.upper(), 70, 1140, "lm"), ("VALORANT", 650, 1140, "rm")]
def scene7(t):
    im = BGE.copy()
    pi = eo(prog(t, .2, 1.4)); paste(im, ISO_DARK, 360, 1280 + 40 * (1 - pi), .45 * pi, "mb")
    im.alpha_composite(DUST[int(t * 12) % 6])
    e = eo(prog(t, 0, .35)); ox = (1 - e) * 600; layer = canvas()
    paste(layer, tl("RADIANTE", SANS(800, 104)), 360 + ox, 600)
    paste(layer, tl("hecho con estilo", SERIF(400, 24)), 655 + ox, 528, prog(t, .3, .6), "rm")
    if ox > 3: layer = motion_blur_x(layer, ox * .15)
    im.alpha_composite(layer)
    for i, (s, x, y, a) in enumerate(CORN):
        tx = typed(s, t, .5 + i * .2, 26)
        if tx: paste(im, tl(tx, SERIF(400, 22, True), SOFT), x, y, 1, a)
    return im

def edge_text():
    im = canvas()
    for items, x in [((NAME.lower(), USER, MONTH), 30), (("fan edit · valorant", USER), 690)]:
        y = 240
        for s in items:
            l = tl(s, SANS(400, 14), (205, 195, 222)).rotate(90, expand=True); paste(im, l, x, y + l.height / 2); y += l.height + 70
    return im
EDGE = edge_text(); VIG = R.VIG

def push(a, b, e, axis, bg):
    img = canvas(bg + (255,))
    if axis == "y":
        img.alpha_composite(offset(b, 0, H * (1 - e))); _safe_comp(img, a.crop((0, int(H * e), W, H)), 0, 0)
    else:
        img.alpha_composite(offset(a, -W * e, 0)); img.alpha_composite(offset(b, W * (1 - e), 0))
    return img

def frame(T):
    if T < 6.6: img = scene1(T)
    elif T < 7.0:
        e = eio(prog(T, 6.6, 7.0)); img = motion_blur_y(push(scene1(T), scene2(T - 7.0), e, "y", DEEP), 28 * math.sin(math.pi * e), 12)
    elif T < 13.6: img = scene2(T - 7.0)
    elif T < 14.0:
        e = eio(prog(T, 13.6, 14.0)); img = motion_blur_x(push(scene2(T - 7.0), scene3(T - 14.0 + .5), e, "x", DEEP), 40 * math.sin(math.pi * e), 12)
    elif T < 29.6: img = scene3(T - 14.0 + .5 if T < 14.5 else T - 14.0)
    elif T < 30.0:
        e = eio(prog(T, 29.6, 30.0))
        a = offset(scale_about(scene3(T - 14.0), 1 + .3 * e), 0, -H * e); b = offset(scene4(T - 30.0), 0, H * (1 - e))
        img = canvas(DEEP + (255,)); img.alpha_composite(b); img.alpha_composite(a); img = motion_blur_y(img, 30 * math.sin(math.pi * e), 12)
    elif T < 41.6: img = scene4(T - 30.0)
    elif T < 42.0:
        e = eio(prog(T, 41.6, 42.0)); img = motion_blur_x(push(scene4(T - 30.0), scene5(T - 42.0), e, "x", DEEP), 40 * math.sin(math.pi * e), 12)
    elif T < 49.5: img = scene5(T - 42.0)
    elif T < 50.0:
        e = eio(prog(T, 49.5, 49.9))
        s = ImageEnhance.Color(scene5(T - 42.0).filter(ImageFilter.GaussianBlur(10 * e))).enhance(1 - .8 * e)
        img = scale_about(s, 1 - .3 * e, bg=(12, 8, 18, 255)); img = Image.blend(img, add_grain(img, 1, T), .5 * e)
        if 49.87 <= T: img = canvas((252, 248, 255, 255))  # flash blanco
    elif T < 53.2: img = scene6(T - 50.0)
    elif T < 53.55:
        e = eio(prog(T, 53.2, 53.55)); img = BGE.copy(); img.alpha_composite(offset(scene6(T - 50.0), -W * e, 0))
        img = motion_blur_x(img, 70 * math.sin(math.pi * e));
        if T >= 53.45: img = scene7(T - 53.45)
    else: img = scene7(T - 53.45)
    if 7.0 < T: img.alpha_composite(EDGE)
    img = add_grain(img, .10 if T < 6.6 else (.18 if T < 50 else .30), T)
    img.alpha_composite(VIG)
    if T > 58.6: img = Image.blend(img, canvas((0, 0, 0, 255)), prog(T, 58.6, 59.9))
    return img.convert("RGB")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--preview" in args:
        ts = [float(x) for x in args[args.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((W // 2, H // 2)) for t in ts]
        sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for i, x in enumerate(ims): sh.paste(x, (i * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview"); sys.exit()
    out = args[0]; audio = args[args.index("--audio") + 1] if "--audio" in args else None
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0: print(f"{i}/{n}", flush=True)
    p.stdin.close(); p.wait(); print("OK", out)
