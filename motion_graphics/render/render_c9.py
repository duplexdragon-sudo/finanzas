#!/usr/bin/env python3
"""Cloud9 sin cupo de socio, roster nuevo y en playoffs — motion graphics morado.
Fuentes: @C9VAL, Liquipedia, esports.net, bo3.gg, Sheep Esports (oct-nov 2026)."""
import os, sys, math, wave, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
from render_smg import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, duo, shadow, clamp01, text_layer, paste, prog, eo, lerp, canvas,
                        scale_about, word, pop, ease_back, slam, ribbon, ring, counter, stripes, particles, confetti, brackets, U, R, clip, stamp)
import render_loud as L
import render_sen as SN
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "..", "c9"); FPS = 30
SONG = os.path.join(HERE, "..", "audio", "musica", "c9_ext.wav"); SONG_AT = 0.0; T1 = os.path.join(HERE, "..", "zek", "clips", "despedida.mp4")

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
NTZ = cut("nightz", 300); FBO = cut("fireballops", 300); GLY = cut("glyph", 300); ALY = cut("alym", 300); DER = cut("derrek", 300)
OXY = S.duo(Image.open(os.path.join(HERE, "..", "sen", "rec", "oxy.png")).convert("RGBA"), 1.08); OXY = OXY.crop(OXY.getchannel("A").getbbox()); OXY = S.fade_bottom(OXY.resize((300, int(OXY.height * 300 / OXY.width)), Image.LANCZOS), .18)
def logo_a(path, h, col=PUR):
    im = Image.open(path).convert("RGBA"); o = Image.new("RGBA", im.size, col + (255,)); o.putalpha(im.getchannel("A")); o = o.crop(o.getbbox())
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)
C9_P = logo_a(os.path.join(PD, "logos", "c9.webp"), 200); C9_W = logo_a(os.path.join(PD, "logos", "c9.webp"), 200, WHITE)
SEN_P = logo_a(os.path.join(HERE, "..", "sen", "logos", "sen_w.png"), 110)
C9_ICONS = [S.R.HAB[k] for k in ("sova_0", "omen_0", "jett_0", "killjoy_0", "sova_1", "omen_1", "jett_1", "killjoy_1") if k in S.R.HAB] or S.ICON_CY
def c9orb(im, logo, x, ybot, T, t_orb, a, size=60, col=WHITE, col2=LILL):
    pad = Image.new("RGBA", (int(logo.width * 1.7), int(logo.height * 1.35))); pad.alpha_composite(logo, ((pad.width - logo.width) // 2, 0))
    S.player_orbit(im, pad, x, ybot, T, t_orb, C9_ICONS, a, size, col, col2)
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

def calcard(top, mes, dia=None, w=400, h=440):
    c = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=WHITE + (255,), outline=PUR + (255,), width=6)
    d.rounded_rectangle((0, 0, w - 1, 120), 34, fill=PUR + (255,)); d.rectangle((0, 80, w - 1, 120), fill=PUR + (255,))
    d.text((w / 2, 62), top, font=ANTON(60), fill=WHITE, anchor="mm")
    for x in (110, w - 110): d.rounded_rectangle((x - 12, -24, x + 12, 34), 10, fill=(60, 10, 90, 255))
    if dia: d.text((w / 2, 245), dia, font=ANTON(170), fill=PUR, anchor="mm"); d.text((w / 2, 380), mes, font=ANTON(64), fill=INK, anchor="mm")
    else: d.text((w / 2, 280), mes, font=ANTON(170), fill=PUR, anchor="mm")
    return shadow(c, 18, 16, .35)
def calflip(im, T, t0, t1, cards, y=560):
    """Hojas de calendario que se voltean de cards[0] a cards[-1] entre t0 y t1, con rebote al final."""
    if T < t0: return
    a = eo(clamp01((T - t0) / .3)); f = eo(clamp01((T - t0) / max(.1, t1 - t0))) * (len(cards) - 1); i = int(f); fr = f - i
    if T >= t1: i, fr = len(cards) - 1, 0
    card = cards[i]
    if fr > 0 and i < len(cards) - 1:
        sy = abs(math.cos(math.pi * fr)); card = cards[i] if fr < .5 else cards[i + 1]; card = card.resize((card.width, max(1, int(card.height * sy))), Image.BICUBIC)
    b = 1 + .12 * math.exp(-(T - t1) * 7) if T >= t1 else 1
    if b != 1: card = card.resize((int(card.width * b), int(card.height * b)), Image.BICUBIC)
    paste(im, card, 360, y, a)
CAL_OCT = [calcard("2026", m) for m in ("JUL", "AGO", "SEP", "OCT")]
CAL_DIC = [calcard("2026", "NOVIEMBRE", "24"), calcard("2026", "NOVIEMBRE", "28"), calcard("2026", "DICIEMBRE", "1")]
_RI = {}
def roleicon(kind, sz=56):
    """Símbolo oficial de rol (recortado de la imagen que mandó Carlos), en morado."""
    if kind not in _RI: _RI[kind] = Image.open(os.path.join(HERE, "..", "roles", kind + ".png")).convert("RGBA")
    return _RI[kind].resize((sz, sz), Image.LANCZOS)
ROLE = {"alym": "duelista", "GLYPH": "controlador", "nightz": "controlador"}
CL = os.path.join(PD, "clips")
GP = {"alym": ("tk1", 3.0, (0, 350, 720, 740)), "GLYPH": ("tk2", 37.5, (0, 272, 576, 592)), "nightz": ("tk3", 1.5, (0, 360, 720, 760)), "FireBallOps": ("tk4", 0.6, (0, 350, 720, 760))}
PL = {"FireBallOps": (FBO, "FIREBALLOPS", "SIGUE · EL ÚNICO QUE QUEDA"), "GLYPH": (GLY, "GLYPH", "CONTROLADOR · IGL"), "alym": (ALY, "ALYM", "DUELISTA · DESDE FURIA"),
      "Derrek": (DER, "DERREK", "NUEVO"), "nightz": (NTZ, "NIGHTZ", "CONTROLADOR")}
_GC = {}
def gclip(name, ss, crop, t, size=(540, 570), dur=3.0):
    """Jugada real a color, con un leve tinte morado en las sombras."""
    key = (name, ss, crop)
    if key not in _GC:
        x, y, w, h = crop
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", os.path.join(CL, name + ".mp4"), "-vf",
                              f"fps=30,crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:flags=lanczos,eq=contrast=1.08:saturation=1.1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0], 3).astype(np.float32)
        l = a.mean(3, keepdims=True) / 255; sh = np.clip(.55 - l, 0, .55) / .55
        a = a * (1 - .25 * sh) + np.array(PUR, np.float32) * .25 * sh; _GC[key] = np.clip(a, 0, 255).astype(np.uint8)
    fr = _GC[key]; return Image.fromarray(fr[int(np.clip(t * 30, 0, len(fr) - 1))]).convert("RGBA")
def same(img, ar=1.15):
    """Recorta todas las fotos al mismo formato (cabeza y pecho) para que las tarjetas queden iguales."""
    w = img.width; h = int(w * ar)
    if img.height >= h: return img.crop((0, 0, w, h))
    c = Image.new("RGBA", (w, h)); c.alpha_composite(img, (0, h - img.height)); return c
_BD = {}
def badge(key, sz):
    """Colores invertidos: disco blanco con borde morado y el símbolo (rol o Cloud9) en morado."""
    if (key, sz) in _BD: return _BD[(key, sz)]
    k = 4; S_ = sz * k; c = Image.new("RGBA", (S_, S_)); d = ImageDraw.Draw(c)
    d.ellipse((0, 0, S_ - 1, S_ - 1), fill=WHITE + (255,), outline=PUR + (255,), width=4 * k)
    if key in ROLE:
        ri = roleicon(ROLE[key], S_); a = np.asarray(ri).astype(int)
        m = ((a[..., 0] > 200) & (a[..., 1] > 200) & (a[..., 2] > 200) & (a[..., 3] > 128)).astype(np.uint8) * 255
        g = Image.new("RGBA", (S_, S_), PUR + (255,)); g.putalpha(Image.fromarray(m)); c.alpha_composite(g)
    else:
        lw = int(S_ * .66); lg = C9_P.resize((lw, int(C9_P.height * lw / C9_P.width)), Image.LANCZOS); c.alpha_composite(lg, ((S_ - lg.width) // 2, (S_ - lg.height) // 2))
    _BD[(key, sz)] = c.resize((sz, sz), Image.LANCZOS); return _BD[(key, sz)]
def rolefly(im, T, t0, key, x, y, sz=58):
    """Símbolo de rol que vuela girando desde afuera y aterriza sobre el jugador (C9 si el rol no está confirmado)."""
    p = prog(T, t0, t0 + .32)
    if p <= 0: return
    e = ease_back(p, 1.6); ic = badge(key, sz)
    ic = ic.rotate((1 - eo(p)) * 300, resample=Image.BICUBIC, expand=True); sx = 1 if x > 360 else -1
    paste(im, shadow(ic, 6, 6, .3), lerp(x + sx * 420, x, e), lerp(y - 260, y, e) + 4 * math.sin(T * 5), clamp01(p * 3))
def pur(T, name):
    im = Image.new("RGBA", (W, H), PUR + (255,)); stripes(im, T, SEG[name], WHITE); ring(im, 360, 700, 330, T * 1.5, LILL, .35); ring(im, 360, 700, 280, -T * 1.6, WHITE, .3, 3, 24); return im
def scene(name, T):
    t = T - SEG[name]
    if name == "L0":                                  # gancho estilo referencia: 4 escenas de ~1 s, morado ↔ blanco con flash
        tB, tC, tD = wt(0, "afuera") - .08, wt(0, "Cloud9") - .1, wt(0, "decidió") - .1
        if T < tB:                                    # A · los jugadores entran grandes y se acomodan en cuadrícula
            im = pur(T, name); slam(im, "RIOT LOS DEJÓ", ANTON(110), 360, 150, T, .05, WHITE)
            for k, (img, x, y) in enumerate(((FBO, 220, 480), (GLY, 500, 480), (ALY, 220, 810), (DER, 500, 810))):
                pk = ease_back(prog(T, .1 + k * .1, .4 + k * .1), 1.5)
                if pk > 0:
                    c = card(same(img), max(10, int(185 * pk))); paste(im, c, x, y + bob(T, k) * .5, clamp01(pk * 2))
            for k, (x, y) in enumerate(((220, 480), (500, 480), (220, 810), (500, 810))):
                rolefly(im, T, .35 + k * .1, ("FireBallOps", "GLYPH", "alym", "Derrek")[k], x + 88, y - 112 + bob(T, k) * .5, 58)
        elif T < tC:                                  # B · AFUERA: logo tachado
            im = bg("w", "AFUERA"); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
            pop(im, C9_P.resize((340, int(C9_P.height * 340 / C9_P.width))), 360, 450, T, tB, .3)
            px = eo(prog(T, tB + .15, tB + .35))
            if px > 0:
                lay = canvas(); d = ImageDraw.Draw(lay); r = 190
                d.line((360 - r, SY(450) - r * .7, lerp(360 - r, 360 + r, px), lerp(SY(450) - r * .7, SY(450) + r * .7, px)), fill=(200, 30, 60, 255), width=22)
                im.alpha_composite(lay)
            stamp(im, "AFUERA", 360, 800, T, tB + .05, (200, 30, 60), -6, 150)
        elif T < tD:                                  # C · CLOUD9: dos jugadores grandes entrando por los lados
            im = pur(T, name); slam(im, "CLOUD9", ANTON(150), 360, 160, T, tC, WHITE)
            for k, (img, x0, x1) in enumerate(((GLY, -250, 220), (NTZ, 970, 500))):
                pk = ease_back(prog(T, tC + k * .08, tC + .3 + k * .08), 1.3)
                if pk > 0:
                    hd = img.resize((330, int(img.height * 330 / img.width))); paste(im, shadow(hd, 10, 10, .35), lerp(x0, x1, pk), 640 + bob(T, k) * .5, clamp01(pk))
                    rolefly(im, T, tC + .2 + k * .1, ("GLYPH", "nightz")[k], x1 + (-110 if k == 0 else 110), 640 - hd.height / 2 + 10, 76)
            if T > tC + .3: ribbon(im, "ROSTER NUEVO", 360, 1065, T, tC + .3, PUR, WHITE, 50, "mm")
        else:                                         # D · PELEA DESDE ABAJO: el logo sube desde abajo con las habilidades girando
            im = bg("w", "C9"); stripes(im, T, tD, PUR, .5)
            word(im, "decidió pelear", IT(900, 56), 360, 150, T, tD, INK); slam(im, "DESDE ABAJO", ANTON(130), 360, 265, T, wt(0, "desde") - .15, PUR)
            pu = ease_back(prog(T, tD + .05, tD + .55), 1.2)
            c9orb(im, C9_P.resize((300, int(C9_P.height * 300 / C9_P.width))), 360, lerp(1400, 920, pu) + 8 * math.sin(T * 2), T, max(0, T - tD), clamp01(pu), 78, PUR, LIL)
        tt = T - max([x for x in (0, tB, tC, tD) if x <= T])
        if 0 < tt < .12 and T > .3: im = Image.blend(im, canvas(LILL + (255,)), .75 * (1 - tt / .12))
        particles(im, T, WHITE, .35); return im
    if name == "L1":
        im = bg("w", "PARED"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "a veces te cierran", IT(400, 54), 360, 160, T, SEG[name] + .05, INK); slam(im, "LA PUERTA", ANTON(140), 360, 290, T, wt(1, "puerta") - .15, PUR)
        tp = wt(1, "tumbar") - .2
        if T > tp: ribbon(im, "Y TIENES QUE TUMBAR LA PARED", 360, 570, T, tp, WHITE, PUR, 50, "mm")
        ring(im, 360, 780, 200, T * 1.4, PUR, .4); return im
    if name == "L2":
        im = bg("w", "SOCIOS"); stripes(im, T, SEG[name], PUR, .5)
        t8 = wt(2, "ocho") - .25
        if T < t8:                                   # parte 1: calendario hasta OCTUBRE
            word(im, "Riot eligió a sus socios", IT(900, 46), 360, 160, T, SEG[name] + .05, INK)
            calflip(im, T, SEG[name] + .1, wt(2, "octubre") + .1, CAL_OCT, 600)
        else:                                        # parte 2: 8 socios y Cloud9 fuera
            ring(im, 360, 470, 170, T * 1.8, PUR, .35)
            counter(im, T, t8, t8 + .5, 0, 8, ANTON(220), 360, 470, PUR)
            word(im, "EQUIPOS SOCIOS", ANTON(66), 360, 680, T, t8 + .15, INK)
            word(im, "VCT Américas 2027-2028", IT(900, 38), 360, 760, T, t8 + .3, PUR)
            tc = wt(2, "estaba") - .5
            if T > tc: pop(im, chipx("CLOUD9", False, 440), 360, 880, T, tc, .3)
        return im
    if name == "L3":
        im = bg("w", "FUERA"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "tampoco quedaron", IT(900, 52), 360, 140, T, SEG[name] + .05, INK)
        for k, (tx, key) in enumerate((("FURIA · CAMPEÓN KICKOFF", "FURIA"), ("ENVY", "ENVY"))):
            t0 = wt(3, key) - .2; pp = ease_back(prog(T, t0, t0 + .3), 1.4)
            if pp > 0: paste(im, chipx(tx, False, 560), lerp(-300, 360, pp), SY(320) + k * 130, clamp01(pp))
        te = wt(3, "cerró") - .4
        if T > te: word(im, "y Evil Geniuses", IT(900, 46), 360, 690, T, te, INK); stamp(im, "CERRÓ", 360, 810, T, te + .15, (200, 30, 60), -6, 110)
        return im
    if name == "L4":
        im = pur(T, name)
        slam(im, "NO SE RINDIÓ", ANTON(120), 360, 200, T, wt(4, "rindió") - .3, WHITE)
        tp = wt(4, "pruebas") - .2
        if T > tp: pop(im, nchip("PRUEBAS ABIERTAS", WHITE, PUR, 50), 360, 380, T, tp, .3)
        p = ease_back(prog(T, SEG[name] + .2, SEG[name] + .6), 1.3); c9orb(im, C9_W.resize((240, int(C9_W.height * 240 / C9_W.width))), 360, 880 + 8 * math.sin(T * 2), T, max(0, t - .2), clamp01(p))
        return im
    if name == "L5":
        tI = wt(5, "coach") - .3
        seq = [k for k in ("FireBallOps", "GLYPH", "alym", "Derrek", "nightz")]
        ts = [SEG["L5"], wt(5, "Llegan") - .15, wt(5, "alym") - .15, wt(5, "Derrek") - .15, wt(5, "nightz") - .15]
        if T < tI:                                    # presentación jugador por jugador con SU jugada
            j = max([i for i, x in enumerate(ts) if x <= T] or [0]); key = seq[j]; t0 = ts[j]; tl = T - t0
            img, nm, tag = PL[key]; im = Image.new("RGBA", (W, H), PUR + (255,)) if j % 2 == 0 else bg("w", nm)
            if j % 2 == 0: stripes(im, T, t0, WHITE)
            fg, bgc = (WHITE, PUR) if j % 2 == 0 else (PUR, WHITE)
            slam(im, nm, ANTON(100), 360, 140, T, t0, fg)
            pop(im, nchip(tag, fg, bgc, 28), 360, 228, T, t0 + .1, .3)
            pc = ease_back(prog(T, t0, t0 + .3), 1.2)
            if key in GP:
                src, ss, crop = GP[key]; fr = gclip(src, ss, crop, tl)
            else:
                fr = same(img, 1.055).resize((540, 570), Image.LANCZOS); fr2 = Image.new("RGBA", fr.size, WHITE + (255,)); fr2.alpha_composite(fr); fr = fr2
            card_ = L.rcard(fr, 28, WHITE); card_ = card_.resize((int(card_.width * lerp(.85, 1, pc)), int(card_.height * lerp(.85, 1, pc))))
            card_ = card_.resize((int(card_.width * (1 + .03 * tl)), int(card_.height * (1 + .03 * tl)))); paste(im, card_, 360, 712, clamp01(pc * 2))
            ph = ease_back(prog(T, t0 + .15, t0 + .45), 1.4)
            if ph > 0 and key in GP:
                hd = img.resize((160, int(img.height * 160 / img.width))); paste(im, shadow(hd, 8, 8, .35), 110, 1020 - hd.height / 2, clamp01(ph * 2))
            rolefly(im, T, t0 + .2, key, 615, 975, 80)
            if tl < .1 and j > 0: im = Image.blend(im, canvas(LILL + (255,)), .7 * (1 - tl / .1))
            return im
        im = bg("w", "C9"); ring(im, 360, 640, 340, T * 1.4, PUR, .3)
        pop(im, C9_P.resize((int(C9_P.width * .5), int(C9_P.height * .5))), 360, 140, T, tI, .35)
        pos = [(FBO, "FIREBALLOPS", "FireBallOps", 130, 430, "SIGUE"), (GLY, "GLYPH", "GLYPH", 360, 430, "CONTROLADOR · IGL"), (NTZ, "NIGHTZ", "nightz", 590, 430, "CONTROLADOR"),
               (ALY, "ALYM", "alym", 240, 790, "DUELISTA"), (DER, "DERREK", "Derrek", 480, 790, "NUEVO")]
        for k, (img, nm, key, x, y, tag) in enumerate(pos):
            t0 = tI + k * .07
            if T > t0:
                pp = ease_back(prog(T, t0, t0 + .3), 1.4); hd = img.resize((150, int(img.height * 150 / img.width)))
                paste(im, shadow(hd, 8, 8, .3), x, SY(y) + bob(T, k), clamp01(pp))
                paste(im, shadow(badge(key, 50), 6, 6, .3), x + 66, SY(y) - hd.height / 2 + 30, clamp01(pp))
                paste(im, nchip(nm, PUR, WHITE, 28), x, SY(y) + hd.height / 2 + 6, clamp01(pp))
                f = 20 if len(tag) < 12 else 16; paste(im, nchip(tag, LIL, INK, f), x, SY(y) + hd.height / 2 + 46, clamp01(pp))
        ti = wt(5, "Immi") - .2
        if T > ti: pop(im, nchip("COACH: IMMI", INK, WHITE, 26), 360, 1150, T, ti, .3)
        return im
    if name == "L6":
        im = bg("w", "SEN"); stripes(im, T, SEG[name], PUR, .5)
        word(im, "mientras tanto", IT(900, 52), 360, 140, T, SEG[name] + .05, INK)
        p = eo(prog(T, SEG[name] + .2, SEG[name] + .6)); paste(im, OXY, 360, SY(480) + 50 * (1 - p) + bob(T), p)
        to = wt(6, "Sentinels") - .3
        if T > to: pop(im, nchip("OXY Y ZELLSIS", PUR, WHITE, 44), 360, 700, T, wt(6, "OXY") - .1, .3); word(im, "se fueron a", IT(900, 40), 360, 780, T, to, INK); pop(im, SEN_P, 360, 880, T, to + .1, .35)
        return im
    if name == "L7":
        im = pur(T, name)
        word(im, "su último internacional", IT(900, 50), 360, 170, T, SEG[name] + .05, WHITE)
        tt = wt(7, "dos") - .2
        counter(im, T, SEG[name] + .3, wt(7, "veintitrés"), 2026, 2023, ANTON(220), 360, 520, WHITE)
        tf = wt(7, "veintitrés")
        if T > tf: stamp(im, "HACE 3 AÑOS", 360, 780, T, tf, (255, 255, 255), -5, 80)
        return im
    if name == "L8":
        im = bg("w", "2-0"); stripes(im, T, SEG[name], PUR, .5); ring(im, 360, 560, 260, T * 1.5, PUR, .4)
        slam(im, "DEBUT PERFECTO", ANTON(96), 360, 150, T, SEG[name] + .05, PUR)
        for k, (tx, key) in enumerate((("2–0 COUNTERFEIT", "counterfeit"), ("2–0 MARYVILLE", "Maryville"))):
            t0 = wt(8, key) - .3; pp = ease_back(prog(T, t0, t0 + .3), 1.4)
            if pp > 0: paste(im, chipx(tx, True, 540, PUR), lerp(1000, 360, pp), SY(380) + k * 130, clamp01(pp))
        tp = wt(8, "playoffs") - .3
        if T > tp: stamp(im, "¡A PLAYOFFS!", 360, 760, T, tp, PUR, -5, 96); confetti(im, T, tp + .1)
        return im
    if name == "L9":
        im = pur(T, name)
        tq = wt(9, "QoR") - .2
        if T < tq:
            word(im, "playoffs", IT(900, 52), 360, 150, T, SEG[name] + .05, WHITE)
            calflip(im, T, SEG[name] + .1, wt(9, "diciembre") + .1, CAL_DIC, 600)
        else:
            ribbon(im, "1 DE DICIEMBRE · PLAYOFFS", 360, 160, T, tq, PUR, WHITE, 46, "mm")
            pop(im, C9_W.resize((int(C9_W.width * .6), int(C9_W.height * .6))), 200, 520, T, tq, .35); word(im, "VS", ANTON(80), 360, 520, T, tq + .1, WHITE)
            slam(im, "QOR", ANTON(110), 530, 520, T, tq + .15, WHITE)
            tk = wt(9, "Kickoff") - .3
            if T > tk: stamp(im, "RUMBO AL KICKOFF", 360, 760, T, tk, (255, 255, 255), -5, 64)
        return im
    return cta(T)

def cta(T):
    k = N - 1; t = T - SEG[f"L{k}"]; im = bg("w", "C9")
    word(im, "¿Cloud9 vuelve a", IT(400, 52), 360, 150, T, SEG[f"L{k}"] + .1, INK); slam(im, "LO MÁS ALTO?", ANTON(110), 360, 260, T, SEG[f"L{k}"] + .3, PUR)
    tc = wt(k, "comentarios") - .1
    tsh = wt(k, "compártelo") - .15
    if tc < T < tsh: pop(im, U.COMMENT, 150, 530 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 150, 615, T, tc + .05, PUR)
    if T >= tsh: pop(im, U.SHARE, 150, 530 + math.sin(T * 5) * 10, T, tsh, .35); word(im, "compártelo", IT(900, 38), 150, 615, T, tsh + .05, PUR)
    c9orb(im, C9_P.resize((200, int(C9_P.height * 200 / C9_P.width))), 480, 790 + 6 * math.sin(T * 2), T, max(0, t - .3), clamp01((t - .3) * 3), 56, PUR, LIL)
    for j, s_ in enumerate(("Fuentes: @C9VAL · Liquipedia · esports.net · bo3.gg · Sheep Esports · nov 2026", "Resultados: VCT Americas Kickoff NA Qualifier (Swiss)")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0:
            tl = text_layer(s_, SANS(500, 15), WHITE); band = Image.new("RGBA", (tl.width + 24, tl.height + 8), INK + (190,)); band.alpha_composite(tl, (12, 4)); paste(im, band, 360, 870 + j * 26, p)
    return im

PURPLE_SC = {"L0", "L4", "L7", "L9"}
SN.PURPLE_SC = PURPLE_SC
KICK = {"L0": "C9", "L1": "PARED", "L2": "8", "L3": "FUERA", "L4": "TRYOUTS", "L5": "2027", "L6": "SEN", "L7": "2023", "L8": "2–0", "L9": "QOR", f"L{N-1}": "C9"}
SN.KICK = KICK; SN._kc.clear()
HITS = []
def hits():
    if not HITS: HITS.extend([.15, wt(0, "afuera"), wt(0, "Cloud9"), wt(0, "decidió"), wt(0, "abajo"), SEG["L1"] + .1, wt(1, "tumbar"), wt(2, "ocho"), wt(2, "estaba"), wt(3, "cerró"), wt(4, "rindió"), wt(5, "GLYPH"), wt(5, "nightz"), wt(6, "Sentinels"), wt(7, "veintitrés"), wt(8, "counterfeit"), wt(8, "Maryville"), wt(8, "playoffs"), wt(9, "QoR")])
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
    ev = [("braam", 0.0, .7), ("hit808", 0.0, .6)] + [("swoosh", SEG[n] - .2, .55) for n in ORDER[1:]] + [("hit808", h0, .6) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [
        ("typing", SEG["L2"] + .3, .4), ("impact", wt(2, "estaba"), .5), ("impact", wt(3, "FURIA"), .5), ("impact", wt(3, "ENVY"), .5), ("clink", wt(3, "cerró"), .5),
        ("pop", wt(4, "pruebas"), .5), ("pop", wt(5, "FireBallOps"), .5), ("pop", wt(5, "GLYPH"), .5), ("pop", wt(5, "alym"), .5), ("pop", wt(5, "Derrek"), .5), ("pop", wt(5, "nightz"), .5),
        ("pop", wt(6, "OXY"), .5), ("typing", wt(7, "dos") - .2, .4), ("riser", SEG["L8"] - 1.0, .4), ("shimmer", wt(8, "counterfeit"), .5), ("shimmer", wt(8, "Maryville"), .5),
        ("cheer", wt(8, "playoffs"), .4), ("boom", wt(8, "playoffs"), .5), ("braam", wt(9, "QoR"), .5), ("pop", wt(k, "comentarios"), .6), ("pop", wt(k, "compártelo"), .6), ("shimmer", wt(k, "compártelo"), .4)]
    for k_, t0, g in ev:
        s = Sx[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .55)):
        w = wave.open(os.path.join(PD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(PD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(PD, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.34[m];"
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
