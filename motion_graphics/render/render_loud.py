#!/usr/bin/env python3
"""CÓMO LOUD GANÓ EL MUNDIAL (Champions Shanghai 2026) — motion graphics, estética morada editorial.
Voz: Andrés (ElevenLabs eleven_v4) por frase con marcas de tiempo. Música: Deep End (Fousheé).
Uso: python3 render_loud.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, wave, json, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_tenz_morado as R
from render_tenz_morado import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, bg, obj, duo, card, brackets, puzzle_tile, shadow, clamp01,
                                text_layer, paste, prog, eo, lerp, SANS, canvas, scale_about, fade_bottom, LUT)
from render_motion import word, pop, ease_back
import render_dia1u as U
from render import rotate_y, motion_blur_x, eio
HERE = os.path.dirname(os.path.abspath(__file__)); LD = os.path.join(HERE, "..", "loud"); FPS = 30
SONG = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/f5663a40-Foushe__-_Deep_End_Lyrics.mp3"; SONG_AT = 29.3

# ---------------- voz y tiempos por palabra ----------------
N = 14; DL, WT = [], []
for i in range(N):
    w = wave.open(os.path.join(LD, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(LD, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
    for ch, a in zip(al["characters"], al["character_start_times_seconds"]):
        if ch.isspace():
            if cur: ws.append((cur, st)); cur = ""
        else:
            if not cur: st = a
            cur += ch
    if cur: ws.append((cur, st))
    WT.append(ws)
LS = []; t = .15
for d in DL: LS.append(t); t += d + .25
DUR = LS[-1] + DL[-1] + 1.4
SCN = list(range(13))                       # escena k = frase k; las frases 12 y 13 son el cierre
SEG = [0.0] + [LS[k] - .1 for k in range(1, 13)]
def wt(k, s, n=0):
    """momento absoluto en que se dice la palabra que contiene s (n-ésima coincidencia)."""
    hits = [st for w_, st in WT[k] if s.lower() in w_.lower()]
    return LS[k] + (hits[min(n, len(hits) - 1)] if hits else 0)

# ---------------- recursos ----------------
def cut(name, w):
    im = duo(Image.open(os.path.join(LD, "rec", name + ".png")).convert("RGBA"), 1.1); im = fade_bottom(im, .18)
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
DARKER = cut("darker2", 700); ERDE = cut("erde2", 640); TROFEO = cut("trofeo_beso", 560)
DARKER_H = cut("darker2", 660)
def facecrop(name):
    ph = cut(name, 480); w = ph.width; fw = int(w * (.5 if ph.width > ph.height else .62))
    a = np.asarray(ph.getchannel("A")) > 120; cols = np.where(a[: max(1, ph.height // 3)].any(0))[0]; cx = int(cols.mean()) if len(cols) else w // 2
    x0 = int(np.clip(cx - fw / 2, 0, w - fw)); return ph.crop((x0, 0, x0 + fw, int(fw * 1.15)))
TKZIN_S, ERDE_S, DARKER_S = facecrop("f8"), facecrop("erde2"), facecrop("darker2")
HOUR = obj("19_reloj_arena", 430); CHAIN = obj("31_cadena_rota", w=640); MEDAL = obj("29_medalla", 260); CUP = obj("45_copa", 330)
DIAM = obj("24_diamante", 120)
TROF = Image.open(os.path.join(LD, "rec", "trofeo_2026.png")).convert("RGBA"); TROF = TROF.resize((int(TROF.width * 420 / TROF.height), 420), Image.LANCZOS)
from PIL import ImageEnhance as _IE
_ta = TROF.getchannel("A"); TROF = _IE.Contrast(_IE.Brightness(TROF.convert("RGB")).enhance(1.45)).enhance(1.12).convert("RGBA"); TROF.putalpha(_ta)
CHB = Image.open(os.path.join(LD, "rec", "cadena.png")).convert("RGBA"); CHB = CHB.resize((int(CHB.width * 58 / CHB.height), 58), Image.LANCZOS).crop((0, 0, 1000, 58))
_g = Image.new("RGBA", (CHB.width, CHB.height + 24), (255, 255, 255, 0)); _gm = Image.new("L", _g.size, 0); _gm.paste(CHB.getchannel("A"), (0, 12))
_g.putalpha(_gm.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .7))); _g.alpha_composite(CHB, (0, 12)); CHB = _g
def chain_band(im, T, t0, tbreak, y, dirn=1):
    """Cadena que entra deslizándose y se rompe en dos al tiempo tbreak."""
    p = eo(prog(T, t0, t0 + .45))
    if p <= 0: return
    x = 360 + dirn * (1 - p) * 900 + dirn * (T - t0) * 25
    if T < tbreak: paste(im, CHB, x, y, p); return
    q = eo(prog(T, tbreak, tbreak + .6)); hw = CHB.width // 2
    for k, part in enumerate((CHB.crop((0, 0, hw, CHB.height)), CHB.crop((hw, 0, CHB.width, CHB.height)))):
        sg = -1 if k == 0 else 1; r = part.rotate(-sg * 25 * q, expand=True, resample=Image.BICUBIC)
        paste(im, r, x + sg * (hw / 2 + 420 * q), y + 260 * q * q, 1 - q * .9)
    if q < 1:   # esquirlas moradas en el punto de quiebre
        d = ImageDraw.Draw(im); rnd = random.Random(int(y))
        for k in range(12):
            ang = rnd.uniform(0, 2 * math.pi); dist = 30 + 160 * q * rnd.uniform(.5, 1.2); sz = rnd.uniform(8, 16) * (1 - q)
            cx, cy = x + math.cos(ang) * dist, y + math.sin(ang) * dist + 80 * q * q
            d.polygon([(cx, cy - sz), (cx + sz * .8, cy + sz * .6), (cx - sz * .7, cy + sz * .5)], fill=(150, 80, 220, int(255 * (1 - q))))
# ---------- trofeo de Shanghái con efectos ----------
def _rays(n=14, R_=520):
    im = Image.new("RGBA", (2 * R_, 2 * R_)); d = ImageDraw.Draw(im)
    for k in range(n):
        a0 = k * 360 / n; d.pieslice((0, 0, 2 * R_, 2 * R_), a0, a0 + 360 / n * .42, fill=(255, 245, 255, 120))
    m = Image.new("L", im.size, 0); md = ImageDraw.Draw(m)
    for r in range(R_, 0, -8): md.ellipse((R_ - r, R_ - r, R_ + r, R_ + r), fill=int(255 * (1 - r / R_) ** .6))
    im.putalpha(Image.fromarray(np.minimum(np.asarray(im.getchannel("A")), np.asarray(m)))); return im
RAYS = _rays()
def _star(s=40, col=WHITE):
    im = Image.new("RGBA", (s, s)); d = ImageDraw.Draw(im); c = s / 2
    d.polygon([(c, 0), (c + s * .1, c - s * .1), (s, c), (c + s * .1, c + s * .1), (c, s), (c - s * .1, c + s * .1), (0, c), (c - s * .1, c - s * .1)], fill=col + (255,))
    return im.filter(ImageFilter.GaussianBlur(.6))
STAR = _star()
_tg = {}
def trophy_fx(im, T, t0, x, y, h=330):
    """Trofeo que cae, aterriza con onda de luz, rayos que giran, resplandor que pulsa, brillo que barre y destellos."""
    if T < t0: return
    t = T - t0
    if h not in _tg:
        tr = TROF.resize((int(TROF.width * h / TROF.height), h), Image.LANCZOS)
        gl = Image.new("RGBA", (tr.width + 120, tr.height + 120), (245, 225, 255, 0)); m = Image.new("L", gl.size, 0); m.paste(tr.getchannel("A"), (60, 60))
        gl.putalpha(m.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(22))); _tg[h] = (tr, gl)
    tr, gl = _tg[h]
    p = clamp01(t / .45); yy = lerp(y - 700, y, ease_back(p, 1.2)) + math.sin(T * 2.2) * 8 if p < 1 else y + math.sin(T * 2.2) * 8
    land = t - .45
    # rayos detrás (giran y respiran)
    ra = clamp01(land * 2.5) * (.75 + .25 * math.sin(T * 3))
    if ra > 0:
        rr = RAYS.rotate(T * 18, resample=Image.BICUBIC); sc = .55 + .1 * math.sin(T * 1.7); rr = rr.resize((int(rr.width * sc), int(rr.height * sc)))
        paste(im, rr, x, yy - h * .05, ra)
    # onda de luz al aterrizar
    if 0 < land < .6:
        q = eo(land / .6); r = lerp(40, 330, q); d = ImageDraw.Draw(im)
        d.ellipse((x - r, yy + h * .3 - r * .35, x + r, yy + h * .3 + r * .35), outline=WHITE + (int(220 * (1 - q)),), width=6)
        d.ellipse((x - r * .7, yy - r * .7, x + r * .7, yy + r * .7), outline=LILL + (int(160 * (1 - q)),), width=4)
    # resplandor que pulsa
    paste(im, gl, x, yy, clamp01(p * 2) * (.8 + .2 * math.sin(T * 4))); paste(im, gl, x, yy, clamp01(land * 2) * (.4 + .3 * math.sin(T * 4)))
    # trofeo + brillo que barre
    tt = tr.copy()
    ph = (T - t0 - .5) % 1.8
    if T - t0 > .5 and ph < .6:
        sx = lerp(-tt.width * .6, tt.width * 1.6, ph / .6); band = Image.new("L", tt.size, 0)
        ImageDraw.Draw(band).polygon([(sx, 0), (sx + 46, 0), (sx - tt.height * .45 + 46, tt.height), (sx - tt.height * .45, tt.height)], fill=200)
        band = Image.fromarray(np.minimum(np.asarray(band.filter(ImageFilter.GaussianBlur(10))), np.asarray(tt.getchannel("A"))))
        white = Image.new("RGBA", tt.size, (255, 255, 255, 0)); white.putalpha(band); tt.alpha_composite(white)
    s_ = 1 + .08 * math.exp(-max(0, land) * 8) * (land > 0)
    if s_ != 1: tt = tt.resize((int(tt.width * s_), int(tt.height * s_)), Image.BICUBIC)
    paste(im, tt, x, yy, clamp01(p * 3))
    # destellos que titilan
    if land > 0:
        for k in range(9):
            rnd = random.Random(k * 31); ang = rnd.uniform(0, 2 * math.pi); rad = rnd.uniform(.45, .75) * h
            tw = math.sin(T * rnd.uniform(3, 6) + k * 1.7)
            if tw <= 0: continue
            sz = int(18 + 26 * tw * rnd.uniform(.6, 1)); st = STAR.resize((sz, sz)).rotate(T * 60 + k * 20)
            paste(im, st, x + math.cos(ang + T * .3) * rad * .8, yy + math.sin(ang + T * .3) * rad, tw * clamp01(land * 3))
# ---------- confeti ----------
CONF = [(random.Random(k).uniform(-60, W + 60), random.Random(k + 5).uniform(-900, -20), random.Random(k + 9).uniform(250, 520), random.Random(k + 2).uniform(0, 6.28),
         random.Random(k + 4).choice([PUR, LILL, WHITE, (252, 209, 22), (150, 80, 220)]), random.Random(k + 6).uniform(8, 16)) for k in range(70)]
def confetti(im, T, t0, dur=3.0):
    t = T - t0
    if t < 0 or t > dur: return
    d = ImageDraw.Draw(im); fa = 1 - clamp01((t - dur + .6) / .6)
    for x, y, vy, ph, col, sz in CONF:
        yy = y + vy * t + 120 * t * t * .3; xx = x + 30 * math.sin(t * 3 + ph)
        if -20 < yy < H + 20:
            w_ = sz * abs(math.cos(t * 6 + ph)) + 2; d.rectangle((xx - w_ / 2, yy - sz * .35, xx + w_ / 2, yy + sz * .35), fill=col + (int(255 * fa),))
# ---------- calendario que se rebobina (reemplaza el reloj) ----------
MESES = ["OCT", "SEP", "AGO", "JUL", "JUN", "MAY", "ABR", "MAR", "FEB", "ENE"]
def _cal_card(mes, w=400, h=440):
    c = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=WHITE + (255,), outline=PUR + (255,), width=6)
    d.rounded_rectangle((0, 0, w - 1, 120), 34, fill=PUR + (255,)); d.rectangle((0, 80, w - 1, 120), fill=PUR + (255,))
    d.text((w / 2, 62), "2026", font=ANTON(64), fill=WHITE, anchor="mm")
    for x in (110, w - 110): d.rounded_rectangle((x - 12, -24, x + 12, 34), 10, fill=(60, 10, 90, 255))
    d.text((w / 2, 280), mes, font=ANTON(170), fill=PUR, anchor="mm"); return shadow(c, 18, 16, .35)
CAL = {m: _cal_card(m) for m in MESES}
def calendar(im, T, t0, t1):
    if T < t0 - .3: return
    a = eo(clamp01((T - t0 + .3) / .3)); f = eio(clamp01((T - t0) / max(.1, t1 - t0))) * (len(MESES) - 1)
    i = int(f); fr = f - i
    if T >= t1: i, fr = len(MESES) - 1, 0
    card = CAL[MESES[i]]
    if fr > 0 and i < len(MESES) - 1:          # volteo de hoja
        sy = abs(math.cos(math.pi * fr)); card = CAL[MESES[i] if fr < .5 else MESES[i + 1]]
        card = card.resize((card.width, max(1, int(card.height * sy))), Image.BICUBIC)
    bounce = 1 + .12 * math.exp(-(T - t1) * 7) if T >= t1 else 1
    if bounce != 1: card = card.resize((int(card.width * bounce), int(card.height * bounce)), Image.BICUBIC)
    paste(im, card, 360, 800, a)
# ---------- anillo 3D de habilidades (como en el video de TenZ) ----------
def _ic(keys): return [R.HAB[k] for k in keys if k in R.HAB]
ICON_TK = _ic(["neon_0", "neon_1", "neon_2", "neon_3"] * 2)                              # tkzin: Neon en los 4 mapas
ICON_ER = _ic(["sage_0", "omen_0", "sage_1", "omen_1", "sage_2", "omen_2", "sage_3", "omen_3"])   # erde: Sage / Omen
ICON_DK = _ic(["omen_0", "vyse_0", "viper_0", "omen_1", "vyse_1", "viper_1", "omen_2", "vyse_2"])  # Darker: Omen / Vyse / Viper
def player_orbit(im, ph, x, ybottom, T, t_orb, icons, a=1.0, size=78, col=PUR, col2=LIL):
    """Foto del jugador con sus habilidades girando alrededor en un anillo 3D (las de atrás pasan detrás de la foto)."""
    cy = ybottom - ph.height / 2; al = np.asarray(ph.getchannel("A")) > 120; rows = np.where(al.any(1))[0]
    top = cy - ph.height / 2 + (rows.min() if len(rows) else 0)
    ox, oy = x, top + ph.height * .56; Rr = ph.width * .52; ap = clamp01(t_orb * 2.5) * a; pts = []
    for k, ic in enumerate(icons):
        ang = t_orb * 1.3 + k * 2 * math.pi / len(icons); z = math.sin(ang); sc = .7 + .4 * (z + 1) / 2
        i2 = R.tint(ic, col if z > 0 else col2).resize((int(size * sc), int(size * sc)), Image.LANCZOS)
        pts.append((z, i2, ox + Rr * math.cos(ang), oy + Rr * .26 * z + 30 * math.cos(ang * .5)))
    if ap > 0:
        ring_ = canvas(); ImageDraw.Draw(ring_).ellipse((ox - Rr, oy - Rr * .26, ox + Rr, oy + Rr * .26), outline=col + (110,), width=3); paste(im, ring_, 0, 0, ap, "lt")
        for z, i2, px, py in pts:
            if z <= 0: paste(im, i2, px, py, ap * .7)
    paste(im, ph, x, cy, a)
    if ap > 0:
        for z, i2, px, py in pts:
            if z > 0: paste(im, i2, px, py, ap)
TK2 = cut("f8", 520); ER2 = cut("erde2", 620); DK2 = cut("darker2", 620); KING = obj("17_rey_ajedrez", 520)
FLAGS = {"BR": [(0, 156, 59), (255, 223, 0)], "PT": [(0, 102, 0), (255, 0, 0)], "CL": [(0, 57, 166), (255, 255, 255), (213, 43, 30)],
         "CO": [(252, 209, 22), (0, 56, 147), (206, 17, 38)]}
def flag(code, w=54, h=36):
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im); cs = FLAGS[code]
    if code == "CO": d.rectangle((0, 0, w, h // 2), fill=cs[0] + (255,)); d.rectangle((0, h // 2, w, h * 3 // 4), fill=cs[1] + (255,)); d.rectangle((0, h * 3 // 4, w, h), fill=cs[2] + (255,))
    elif code == "BR": d.rectangle((0, 0, w, h), fill=cs[0] + (255,)); d.polygon([(w / 2, 4), (w - 5, h / 2), (w / 2, h - 4), (5, h / 2)], fill=cs[1] + (255,)); d.ellipse((w / 2 - 8, h / 2 - 8, w / 2 + 8, h / 2 + 8), fill=(0, 39, 118, 255))
    elif code == "PT": d.rectangle((0, 0, w * .4, h), fill=cs[0] + (255,)); d.rectangle((w * .4, 0, w, h), fill=cs[1] + (255,)); d.ellipse((w * .4 - 7, h / 2 - 7, w * .4 + 7, h / 2 + 7), fill=(255, 220, 0, 255))
    elif code == "CL": d.rectangle((0, 0, w, h), fill=cs[1] + (255,)); d.rectangle((0, h / 2, w, h), fill=cs[2] + (255,)); d.rectangle((0, 0, w * .38, h / 2), fill=cs[0] + (255,))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 7, fill=255); im.putalpha(m); return im
def chip(name, code, col=PUR, fg=WHITE):
    f = ANTON(54); tw = int(f.getlength(name.upper())); im = Image.new("RGBA", (tw + 120, 84)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, 83), 42, fill=col + (255,)); d.text((30, 42), name.upper(), font=f, fill=fg, anchor="lm")
    im.alpha_composite(flag(code), (tw + 46, 24)); return im
def check(s=56, col=WHITE):
    im = Image.new("RGBA", (s, s)); ImageDraw.Draw(im).line([(s * .18, s * .52), (s * .42, s * .76), (s * .84, s * .26)], fill=col + (255,), width=9, joint="curve"); return im
CHECK = check()
def logo(name, h=None, w=None, col=WHITE):
    im = Image.open(os.path.join(LD, "logos", name + ".png")).convert("RGBA"); sc = h / im.height if h else w / im.width
    return R.tint(im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS), col)
KICK = logo("kickoff", 210, col=LILL); VIT_W = logo("vitality_icono", 120, col=WHITE)
def map_card(name, s_, win):
    w, h = 600, 120; c = Image.new("RGBA", (w, h), (60, 30, 80, 255)); f = os.path.join(LD, "mapas", name.lower() + ".jpg")
    if os.path.exists(f):
        m = Image.open(f).convert("RGB"); r = max(w / m.width, h / m.height); m = m.resize((int(m.width * r) + 1, int(m.height * r) + 1), Image.LANCZOS)
        m = m.crop(((m.width - w) // 2, (m.height - h) // 2, (m.width - w) // 2 + w, (m.height - h) // 2 + h)); m = duo(m.convert("RGBA"), 1.0)
        c = Image.blend(m, Image.new("RGBA", (w, h), (PUR if win else (40, 20, 50)) + (255,)), .35 if win else .6)
    d = ImageDraw.Draw(c); d.text((30, h / 2), name, font=ANTON(58), fill=WHITE, anchor="lm"); d.text((w - 30, h / 2), s_, font=ANTON(58), fill=WHITE if win else LILL, anchor="rm")
    if win: d.rounded_rectangle((0, 0, 11, h), 0, fill=WHITE + (255,))
    m_ = Image.new("L", (w, h), 0); ImageDraw.Draw(m_).rounded_rectangle((0, 0, w - 1, h - 1), 24, fill=255); c.putalpha(m_)
    return shadow(c, 12, 12, .35)
PRX_P = logo("prx", h=70, col=PUR); NRG_P = logo("nrg", h=56, col=PUR); VIT_P = logo("vitality_icono", 92, col=PUR)

# ---------------- clips (gris → duotono morado) ----------------
LUTA = np.stack([np.array(l, np.uint8) for l in LUT], 1)
_cl = {}
def clip(name, t0, dur, crop, size, t, fps=30):
    """crop = (x,y,w,h) en px del original; devuelve RGBA morado del tamaño size."""
    key = (name, t0, crop, size)
    if key not in _cl:
        x, y, w, h = crop
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(dur), "-i", os.path.join(LD, "clips", name + ".mp4"), "-vf",
                              f"fps={fps},crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:force_original_aspect_ratio=increase,crop={size[0]}:{size[1]},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        _cl[key] = np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0])
    fr = _cl[key]; g = fr[int(np.clip(t * fps, 0, len(fr) - 1))].astype(np.float32)
    lo, hi = np.percentile(g[::4, ::4], (1, 99)); g = np.clip((g - lo) / max(1, hi - lo) * 255 * 1.05, 0, 255).astype(np.uint8)
    rgb = LUTA[g]; return Image.fromarray(np.dstack([rgb, np.full(g.shape, 255, np.uint8)]), "RGBA")
def rcard(im, r=26, border=PUR):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255); im = im.copy(); im.putalpha(m)
    if border: ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, outline=border + (255,), width=5)
    return shadow(im, 18, 16, .35)

# ---------------- piezas de motion graphics ----------------
def slam(im, s_, font, x, y, T, t0, col=WHITE, anchor="mm", dur=.22):
    """Texto que cae grande y se asienta (golpe)."""
    p = prog(T, t0, t0 + dur)
    if p <= 0: return
    l = text_layer(s_, font, col); sc = lerp(1.9, 1.0, eo(p)); l = l.resize((max(1, int(l.width * sc)), max(1, int(l.height * sc))), Image.BICUBIC)
    paste(im, l, x, y, clamp01(p * 3), anchor)
def ribbon(im, txt, x, y, T, t0, bgc=PUR, fg=WHITE, size=60, anchor="lm"):
    f = ANTON(size); tw = int(f.getlength(txt)) + 60; r = Image.new("RGBA", (tw, int(size * 1.5)), bgc + (255,))
    ImageDraw.Draw(r).text((30, r.height / 2 + 2), txt, font=f, fill=fg, anchor="lm"); p = eo(prog(T, t0, t0 + .35))
    if p > 0: paste(im, r.crop((0, 0, max(1, int(tw * p)), r.height)), x if anchor == "lm" else x - tw / 2, y, 1, "lm")
def ring(im, cx, cy, r, T, col=PUR, a=1.0, w=4, dash=18):
    lay = canvas(); d = ImageDraw.Draw(lay); off = T * 40
    for k in range(dash):
        a0 = k * 360 / dash + off; d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 360 / dash * .55, fill=col + (int(255 * a),), width=w)
    im.alpha_composite(lay)
def counter(im, T, t0, t1, v0, v1, font, x, y, col=WHITE, fmt="{:d}"):
    if T < t0: return
    v = int(round(lerp(v0, v1, eo(prog(T, t0, t1))))); paste(im, text_layer(fmt.format(v), font, col), x, y)
def stripes(im, T, t0, col, a=1.0, y=640):
    """Bandas diagonales que barren la pantalla."""
    p = eo(prog(T, t0, t0 + .5))
    if p <= 0: return
    lay = canvas(); d = ImageDraw.Draw(lay)
    for k in range(5):
        x = lerp(-900, 100, p) + k * 170; d.polygon([(x, y + 700), (x + 80, y + 700), (x + 680, y - 700), (x + 600, y - 700)], fill=col + (int(40 * a),))
    im.alpha_composite(lay)
SPARK = [(random.Random(k).uniform(0, W), random.Random(k + 99).uniform(0, H), random.Random(k + 7).uniform(2, 5), random.Random(k + 3).uniform(.3, 1)) for k in range(40)]
def particles(im, T, col=WHITE, a=.6):
    d = ImageDraw.Draw(im)
    for x, y, r, sp in SPARK:
        yy = (y - T * 60 * sp) % H; xx = x + math.sin(T * sp * 2 + x) * 12; aa = int(255 * a * (.4 + .6 * abs(math.sin(T * sp * 3 + y))))
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=col + (aa,))
def flag_wave(im, T, t0, y=640, h=300):
    """Bandera de Colombia ondeando detrás (tres cintas)."""
    p = eo(prog(T, t0, t0 + .6))
    if p <= 0: return
    lay = canvas(); d = ImageDraw.Draw(lay); cols = [(252, 209, 22), (0, 56, 147), (206, 17, 38)]; hs = [h / 2, h / 4, h / 4]; y0 = y - h / 2
    for c, hh in zip(cols, hs):
        pts = [(x, y0 + 26 * math.sin(x / 90 + T * 3)) for x in range(-20, int(W * p) + 30, 10)]
        pts2 = [(x, yy + hh) for x, yy in reversed(pts)]
        d.polygon(pts + pts2, fill=c + (235,)); y0 += hh
    im.alpha_composite(lay)

# ---------------- escenas ----------------
def scene(k, T):
    t = T - SEG[k]
    if k == 0:   # gancho: un colombiano campeón del mundo
        im = bg("p", "LOUD"); stripes(im, T, 0, WHITE); ring(im, 360, 900, 330, T, LILL, .5)
        flag_wave(im, T, wt(0, "colombiano"), 900, 240)
        trophy_fx(im, T, wt(0, "campeón") + .1, 530, 790, 390)
        ent = clamp01(t / .45); zs = lerp(1.3, 1.0, ease_back(ent, 1.4)) * (1 + .035 * t)
        ph = DARKER_H.resize((int(DARKER_H.width * zs), int(DARKER_H.height * zs)), Image.BICUBIC)
        player_orbit(im, ph, 360 + math.sin(T * 1.4) * 7, 1300 + 140 * (1 - eo(ent)) + math.sin(T * 2.1) * 5, T, max(0, t - .15), ICON_DK, clamp01(t * 5), 70, WHITE, LILL)
        ribbon(im, "UN COLOMBIANO", 360, 170, T, wt(0, "colombiano") - .1, WHITE, PUR, 70, "mm")
        word(im, "es", IT(400, 56), 360, 290, T, wt(0, "es"), LILL)
        slam(im, "CAMPEÓN", ANTON(150), 360, 390, T, wt(0, "campeón"), WHITE)
        slam(im, "DEL MUNDO", ANTON(96), 360, 505, T, wt(0, "mundo"), LILL)
        particles(im, T, WHITE, .5); return im
    if k == 1:   # volver a enero
        im = bg("w", "2026"); ring(im, 360, 790, 290, T, PUR, .6)
        calendar(im, T, SEG[1] + .15, wt(1, "enero") - .05)
        word(im, "para entender esta historia", IT(400, 46), 360, 200, T, wt(1, "entender"), INK)
        word(im, "hay que volver a", IT(400, 46), 360, 280, T, wt(1, "volver"), INK)
        slam(im, "ENERO", ANTON(190), 360, 420, T, wt(1, "enero"), PUR); return im
    if k == 2:   # 0–3 en el Kickoff
        im = bg("p"); stripes(im, T, SEG[2], WHITE)
        word(im, "LOUD arrancó el 2026", IT(400, 50), 330, 250, T, wt(2, "LOUD"), WHITE)
        chain_band(im, T, SEG[2] + .1, wt(2, "Kickoff") + .25, 400, 1); chain_band(im, T, SEG[2] + .2, wt(2, "Kickoff") + .3, 720, -1)
        puzzle_tile(im, T, wt(2, "perdiendo"), "0", 200, 560, 260, WHITE if False else (90, 10, 130))
        puzzle_tile(im, T, wt(2, "tres", 1), "3", 520, 560, 260, (90, 10, 130))
        slam(im, "–", ANTON(160), 360, 550, T, wt(2, "tres", 1) + .2, WHITE)
        word(im, "Kickoff · Américas", IT(900, 60), 360, 760, T, wt(2, "Kickoff"), LILL); pop(im, KICK.resize((int(KICK.width * 1.3), int(KICK.height * 1.3))), 360, 1000, T, wt(2, "Kickoff") + .1, .4)
        return im
    if k == 3:   # ni un titular de 2022
        im = bg("w"); ring(im, 360, 900, 250, T, PUR, .45); ring(im, 360, 900, 205, -T * 1.4, LIL, .35, 3, 26)
        for j, ch in enumerate("2022"):
            pj = ease_back(prog(t, .05 + j * .12, .4 + j * .12), 1.6)
            if pj > 0: paste(im, text_layer(ch, ANTON(300), (205, 198, 214)), 135 + j * 150, lerp(300, 520, pj) + math.sin(T * 2 + j) * 6, clamp01(pj * 2))
        p = eo(prog(T, wt(3, "quedaba"), wt(3, "quedaba") + .4)); d = ImageDraw.Draw(im)
        if p > 0: d.line((110, 560, lerp(110, 610, p), lerp(560, 470, p)), fill=PUR + (255,), width=22)
        word(im, "del equipo campeón de", IT(400, 46), 360, 230, T, wt(3, "equipo"), INK)
        tz = wt(3, "ni")
        if T > tz - 1.0:   # tragamonedas 5 → 0
            box = Image.new("RGBA", (220, 300)); dd = ImageDraw.Draw(box); f = clamp01((T - tz + 1.0) / 1.0); v = 5 * (1 - eo(f)); i0 = int(math.floor(v)); fr = v - i0
            for q, dig in ((0, i0), (1, i0 + 1)):
                if 0 <= dig <= 5: dd.text((110, 150 + (fr - q) * 300 * -1 + 0), str(dig), font=ANTON(260), fill=PUR, anchor="mm")
            paste(im, box, 170, 920, clamp01((T - tz + 1.0) * 4))
        word(im, "titulares", IT(900, 80), 450, 870, T, wt(3, "titular"), PUR, "mm")
        word(im, "siguen", IT(400, 52), 450, 950, T, wt(3, "titular") + .2, INK)
        return im
    if k == 4:   # equipo nuevo
        im = bg("w", "NUEVO"); stripes(im, T, SEG[4], PUR, .6)
        word(im, "equipo nuevo", IT(900, 76), 360, 150, T, wt(4, "Equipo"), PUR)
        rows = [("lukxo", "BR"), ("tkzin", "BR"), ("DaviH", "PT"), ("erde", "CL"), ("Darker", "CO")]
        for j in range(5):   # casillas vacías que entran al inicio y se llenan con cada jugador
            pj = eo(prog(T, SEG[4] + .05 + j * .09, SEG[4] + .35 + j * .09)); filled = T > wt(4, rows[j][0])
            if pj > 0 and not filled:
                slot = Image.new("RGBA", (260, 84)); ImageDraw.Draw(slot).rounded_rectangle((2, 2, 257, 81), 40, outline=PUR + (200,), width=4)
                ImageDraw.Draw(slot).text((130, 42), "?", font=ANTON(48), fill=PUR + (160,), anchor="mm")
                paste(im, slot, lerp(-300, 50, pj) + math.sin(T * 4 + j) * 4, 270 + j * 100, pj * .9, "lm")
        ring(im, 560, 820, 170, T, PUR, .4 * clamp01(t * 3) * (1 - prog(T, wt(4, "tkzin"), wt(4, "tkzin") + .3)))
        for j, (n, c) in enumerate(rows):
            t0 = wt(4, n); p = eo(prog(T, t0, t0 + .3))
            if p > 0: paste(im, chip(n, c, PUR if n != "Darker" else (252, 209, 22), WHITE if n != "Darker" else INK), lerp(-300, 50, p), 270 + j * 100, p, "lm")
        seq = [(TK2, "tkzin", 470), (ER2, "erde", 420), (DK2, "Darker", 420)]
        for q, (ph, n, x) in enumerate(seq):
            t0 = wt(4, n)
            if T <= t0: continue
            nxt = wt(4, seq[q + 1][1]) if q < 2 else 1e9; p = eo(prog(T, t0, t0 + .35)); a = p * (1 - .75 * prog(T, nxt, nxt + .25))
            if n == "Darker": flag_wave(im, T, t0, 1080, 150)
            ics = {"tkzin": ICON_TK, "erde": ICON_ER, "Darker": ICON_DK}[n]; act = T < nxt
            if act: player_orbit(im, ph, x + 60 * (1 - p), 1280, T, T - t0, ics, a, 66, WHITE if False else PUR)
            else: paste(im, ph, x + 60 * (1 - p), 1280 - ph.height / 2, a)
        return im
    if k == 5:   # el más joven: 20 años
        im = bg("p"); ring(im, 360, 680, 280, T, WHITE, .5); ring(im, 360, 680, 230, -T, LILL, .35, 3, 30)
        word(im, "el equipo más joven", IT(400, 50), 340, 260, T, wt(5, "joven") - .2, WHITE)
        word(im, "en ganar un Champions", IT(400, 46), 340, 330, T, wt(5, "Champions") - .2, LILL)
        counter(im, T, wt(5, "veinte") - .1, wt(5, "veinte") + .6, 0, 20, ANTON(300), 360, 680)
        word(im, "años de promedio", IT(900, 64), 360, 900, T, wt(5, "promedio"), WHITE)
        pop(im, MEDAL, 360, 1100, T, wt(5, "promedio") + .1, .4); particles(im, T, WHITE, .4); return im
    if k == 6:   # Shanghái 6–1
        im = bg("w", "上海"); cf = clip("c3", 18, 7, (0, 0, 576, 576), (600, 600), t)
        pop(im, rcard(cf), 360, 560, T, SEG[6], .4)
        ribbon(im, "SHANGHÁI", 60, 190, T, wt(6, "Shanghái") - .1, PUR, WHITE, 64)
        slam(im, "6", ANTON(200), 200, 1010, T, wt(6, "seis"), PUR); slam(im, "–", ANTON(160), 360, 1000, T, wt(6, "una"), INK)
        slam(im, "1", ANTON(200), 520, 1010, T, wt(6, "una"), PUR)
        if T > wt(6, "Vitality"): ribbon(im, "LA ÚNICA DERROTA: VS", 300, 1180, T, wt(6, "Vitality"), INK, WHITE, 44, "mm"); pop(im, R.tint(VIT_W, INK), 610, 1180, T, wt(6, "Vitality") + .2, .35)
        return im
    if k == 7:   # Paper Rex, NRG, Vitality
        im = bg("p"); cf = clip("c3", 66, 6, (0, 0, 576, 576), (720, 1280), t); im = Image.blend(im, cf, .25)
        word(im, "le ganaron a", IT(400, 54), 330, 250, T, wt(7, "ganaron"), WHITE)
        for j, (n, sc, key, lg) in enumerate((("PAPER REX", "2–0", "Paper", PRX_P), ("", "2–1", "NRG", NRG_P), ("VITALITY", "2–1", "Vitality", VIT_P))):
            t0 = wt(7, key); p = eo(prog(T, t0, t0 + .35))
            if p <= 0: continue
            c = Image.new("RGBA", (600, 150)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 599, 149), 30, fill=WHITE + (255,))
            x0 = 40
            if lg is not None: c.alpha_composite(lg, (36, int(75 - lg.height / 2))); x0 = 36 + lg.width + 18
            d.text((x0, 75), n, font=ANTON(66 if lg is None else 58), fill=PUR, anchor="lm"); d.text((450, 75), sc, font=ANTON(66), fill=INK, anchor="mm")
            cc = Image.new("RGBA", (64, 64)); ImageDraw.Draw(cc).ellipse((0, 0, 63, 63), fill=PUR + (255,)); cc.alpha_composite(check(64), (0, 0)); c.alpha_composite(cc, (520, 43))
            c = rotate_y(c, lerp(80, 0, p))[0] if p < 1 else c
            paste(im, shadow(c, 14, 12, .3), 360 + 400 * (1 - p) * (1 if j % 2 else -1), 400 + j * 210, p)
        word(im, "final de ganadores", IT(900, 52), 360, 1080, T, wt(7, "Vitality") + .3, LILL); return im
    if k == 8:   # la gran final 3–1
        tl = wt(8, "LOUD"); src = clip("c2", 1, 9, (0, 450, 720, 410), (720, 1280), t) if T < tl else clip("c2", 11, 7, (0, 0, 720, 840), (720, 1280), T - tl)
        im = Image.blend(src, canvas(PUR + (255,)), .35)
        ribbon(im, "GRAN FINAL", 360, 160, T, SEG[8], WHITE, PUR, 64, "mm")
        word(im, "otra vez Vitality", IT(900, 58), 360, 270, T, wt(8, "otra"), WHITE)
        maps = [("SUMMIT", "13–11", 1), ("LOTUS", "8–13", 0), ("SUNSET", "13–5", 1), ("HAVEN", "13–10", 1)]
        for j, (m, s_, win) in enumerate(maps):
            t0 = wt(8, "otra") + .35 + j * .3; p = eo(prog(T, t0, t0 + .3))
            if p <= 0 or T > tl + .1: continue
            paste(im, map_card(m, s_, win), lerp(-300, 360, p), 430 + j * 140, p)
        if T > tl:
            p = prog(T, tl, tl + .25); shake = (1 - p) * 14
            slam(im, "3–1", ANTON(330), 360 + random.uniform(-shake, shake), 700, T, tl + .1, WHITE)
            word(im, "LOUD", ANTON(110), 360, 960, T, tl + .3, LILL); particles(im, T, WHITE, .7)
            confetti(im, T, tl + .15)
        return im
    if k == 9:   # primer bicampeón
        im = bg("w"); x2 = text_layer("×2", ANTON(520), (226, 214, 236)); bt = 1 + .05 * math.sin(T * 5); x2 = x2.resize((int(x2.width * bt), int(x2.height * bt)))
        paste(im, x2, 360, 640, eo(clamp01(t * 2)))
        ring(im, 360, 760, 320, T, PUR, .5)
        zt = 1 + .04 * t; tf = TROFEO.resize((int(TROFEO.width * zt), int(TROFEO.height * zt)))
        paste(im, tf, 360 + math.sin(T * 1.3) * 6, 1280 - tf.height / 2 + 40 * (1 - eo(clamp01(t / .5))), clamp01(t * 3))
        confetti(im, T, wt(9, "dos"))
        word(im, "el primer equipo", IT(400, 52), 360, 170, T, wt(9, "primer"), INK)
        word(im, "de la historia", IT(400, 52), 360, 240, T, wt(9, "historia"), INK)
        ribbon(im, "2 VECES CAMPEÓN", 360, 350, T, wt(9, "dos"), PUR, WHITE, 66, "mm")
        for j, x in enumerate((140, 580)): pop(im, DIAM, x, 520 + 20 * math.sin(T * 3 + j), T, wt(9, "Champions") + j * .1, .3)
        return im
    if k == 10:  # erde MVP
        im = bg("p"); paste(im, text_layer("MVP", ANTON(400), (140, 50, 190)), 360, 560, eo(clamp01(t * 2)))
        ring(im, 360, 700, 300, T, WHITE, .4)
        player_orbit(im, ERDE, 360, 1280 + 40 * (1 - eo(clamp01(t / .5))), T, max(0, T - wt(10, "MVP")), ICON_ER, clamp01(t * 3), 84, WHITE, LILL)
        slam(im, "ERDE", ANTON(130), 360, 180, T, wt(10, "erde"), WHITE)
        ch = chip("Chile · 18", "CL", WHITE, PUR); pop(im, ch, 360, 300, T, wt(10, "chileno"), .35)
        slam(im, "MVP", ANTON(170), 360, 440, T, wt(10, "MVP"), LILL)
        cf = clip("c4", 20, 4, (0, 200, 576, 380), (320, 212), T - wt(10, "torneo")) if T > wt(10, "torneo") else None
        if cf is not None: pop(im, rcard(cf, 20, WHITE), 545, 1130, T, wt(10, "torneo"), .35)
        particles(im, T, WHITE, .5); return im
    if k == 11:  # Darker campeón del mundo
        im = bg("w"); flag_wave(im, T, SEG[11] + .1, 820, 380)
        player_orbit(im, DARKER, 360, 1290 + 40 * (1 - eo(clamp01(t / .5))), T, max(0, t - .3), ICON_DK, clamp01(t * 3), 84)
        slam(im, "DARKER", ANTON(140), 360, 180, T, wt(11, "Darker"), PUR)
        pop(im, chip("Colombia", "CO", (252, 209, 22), INK), 360, 300, T, wt(11, "colombiano"), .35)
        ribbon(im, "CAMPEÓN DEL MUNDO", 360, 420, T, wt(11, "campeón"), PUR, WHITE, 70, "mm")
        cf = clip("c2", 19, 3, (0, 200, 720, 700), (300, 290), T - wt(11, "campeón")) if T > wt(11, "campeón") else None
        if cf is not None: pop(im, rcard(cf, 20), 560, 640, T, wt(11, "campeón") + .2, .35)
        confetti(im, T, wt(11, "campeón") + .1); particles(im, T, PUR, .5); return im
    return cta(T)

def cta(T):
    t = T - SEG[12]; im = bg("w", "LOUD")
    word(im, "¿Quién fue el mejor", IT(400, 54), 360, 150, T, wt(12, "Quién"), INK)
    slam(im, "DE LA FINAL?", ANTON(110), 360, 260, T, wt(12, "final"), PUR)
    for j, (ph, n) in enumerate(((TKZIN_S, "tkzin"), (ERDE_S, "erde"), (DARKER_S, "Darker"))):
        f = ph.resize((190, int(ph.height * 190 / ph.width))).crop((0, 0, 190, 220)); bgc = Image.new("RGBA", f.size, LILL + (255,)); bgc.alpha_composite(f); c = rcard(bgc, 22)
        x = 140 + j * 220; hl = (int((T - wt(12, "mejor")) * 1.6) % 3 == j) and T > wt(12, "mejor") + .6
        if hl: c = c.resize((int(c.width * 1.1), int(c.height * 1.1))); ring(im, x, 470, 140, T * 2, PUR, .8, 4, 14)
        pop(im, c, x, 470 + (math.sin(T * 3 + j) * 6), T, wt(12, "mejor") + j * .12, .35)
        word(im, n, IT(900, 40), x, 610, T, wt(12, "mejor") + j * .12 + .1, PUR)
    tc = wt(12, "comentarios")
    if T > tc: pop(im, U.COMMENT, 600, 720 + math.sin(T * 5) * 10, T, tc, .35); word(im, "comenta", IT(900, 40), 600, 810, T, tc + .05, PUR)
    ts = wt(13, "Sígueme")
    if T > ts:
        clicked = T > wt(13, "historias"); pop(im, U.follow_btn(clicked), 360, 930, T, ts, .35)
        cp = eo(prog(T, ts + .1, wt(13, "historias"))); paste(im, R.CURSOR, lerp(650, 420, cp), lerp(1150, 950, cp), clamp01(cp * 3), "lt")
    tsh = wt(13, "compártelo")
    if T > tsh:
        p = eo(prog(T, tsh + .2, tsh + .6)); pop(im, U.SHARE, 200, 1100, T, tsh, .35)
        if p > 0: paste(im, U.SHARE.resize((70, 70)), lerp(200, 330, p), lerp(1100, 980, p), 1 - p)
        word(im, "comparte", IT(900, 36), 200, 1190, T, tsh + .1, PUR)
    tg = wt(13, "guárdalo")
    if T > tg:
        f = eo(prog(T, tg + .1, tg + .6)); pop(im, U.icon_save(150, f), 520, 1100, T, tg, .35); word(im, "guárdalo", IT(900, 36), 520, 1190, T, tg + .1, PUR)
    for j, s_ in enumerate(("Fuentes: Strafe · esportnow · vlr.gg · valorant-spind · 18 oct 2026", "Clips e imágenes: VCT / Riot Games y sus autores · fan edit")):
        p = prog(t, 1 + j * .2, 1.4 + j * .2)
        if p > 0: paste(im, text_layer(s_, SANS(400, 15), (110, 100, 125)), 360, 1240 + j * 22, p)
    return im

HITS = []
def hits():
    if not HITS: HITS.extend([wt(0, "campeón"), wt(1, "enero"), wt(2, "tres", 1), wt(3, "ni"), wt(5, "veinte") + .6, wt(6, "una"), wt(8, "LOUD") + .1,
                              wt(9, "dos"), wt(10, "MVP"), wt(11, "campeón")])
    return HITS
def impact_fx(img, T):
    """Sacudida de cámara + separación RGB + destello en cada golpe fuerte."""
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
def vhs(img, T, t0, t1):
    """Líneas y desfase tipo cinta VHS mientras se rebobina."""
    if not (t0 <= T < t1): return img
    lay = canvas(); d = ImageDraw.Draw(lay); off = int(T * 900) % 8
    for y in range(off, H, 8): d.line((0, y, W, y), fill=(20, 0, 40, 40))
    for k in range(3):
        y = int((T * 700 + k * 430) % H); d.rectangle((0, y, W, y + 14), fill=(255, 255, 255, 50))
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    if int(T * 4) % 2 == 0: d.text((40, 1150), "◀◀ REW", font=ANTON(48), fill=WHITE + (230,), anchor="lm") if False else None
    tri = [(60, 1130), (30, 1150), (60, 1170)]; d.polygon(tri, fill=PUR + (230,)); d.polygon([(x + 30, y) for x, y in tri], fill=PUR + (230,))
    d.text((100, 1150), "REW", font=ANTON(44), fill=PUR + (230,), anchor="lm")
    return img
def frame(T):
    k = max(i for i in range(len(SEG)) if T >= SEG[i]); img = scene(k, T); dc = T - SEG[k]
    if k == 1: img = vhs(img, T, SEG[1] + .15, wt(1, "enero") - .05)
    nxt = SEG[k + 1] if k + 1 < len(SEG) else DUR; img = scale_about(img, 1 + .035 * clamp01(dc / max(1, nxt - SEG[k])), bg=WHITE + (255,))
    particles(img, T + k * 7, WHITE if k in (0, 2, 5, 7, 8, 10) else LIL, .35)
    if k % 2 == 0: brackets(img, dc, WHITE if k in (0, 2, 8, 10) else PUR, .8)
    mark = text_layer("@DuplexDragon_", SANS(600, 18), WHITE if k in (0, 2, 5, 7, 8, 10) else PUR); paste(img, mark, 690, 60, .7, "rm")
    if k > 0 and dc < .18:   # cortinilla: barrido diagonal morado
        p = dc / .18; lay = canvas(); d = ImageDraw.Draw(lay); x = lerp(-200, W + 900, p)
        d.polygon([(x - 900, 0), (x, 0), (x - 500, H), (x - 1400, H)], fill=PUR + (255,)); img.alpha_composite(lay)
    s = 1 + .06 * (1 - eo(clamp01(dc / .35))) if k > 0 else 1; img = scale_about(img, s, bg=WHITE + (255,)); img = impact_fx(img, T)
    if T < .08: img = Image.blend(img, canvas(WHITE + (255,)), .7 * (1 - T / .08))
    if T > DUR - .8: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, DUR - .8, DUR - .1))
    return img.convert("RGB")

def audio(out):
    SR = 48000; Ns = int(DUR * SR); vox = np.zeros((Ns, 2), np.float32)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    for i, s in enumerate(LS):
        v = rd(os.path.join(LD, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    S = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "clink", "boom", "cheer", "braam", "hit808", "glitch", "rewind", "swoosh", "riser", "crowd", "typing")}
    ev = [("braam", 0.0, .75), ("hit808", 0.0, .7)] + [("swoosh", c - .2, .55) for c in SEG[1:]] + [("hit808", h0, .65) for h0 in hits()] + [
        ("glitch", h0, .35) for h0 in hits()[::2]] + [("rewind", SEG[1] + .15, .6), ("riser", wt(8, "LOUD") - 2.0, .55), ("braam", wt(8, "LOUD") + .1, .7),
        ("crowd", wt(8, "LOUD") + .2, .5), ("typing", wt(3, "ni") - 1.0, .4), ("shimmer", wt(9, "dos"), .6), ("cheer", wt(9, "dos"), .3), ("shimmer", wt(11, "campeón") + .1, .5), ("braam", wt(11, "campeón"), .6), ("braam", wt(10, "MVP"), .5)] + [
        ("punch", wt(0, "campeón"), .6), ("whoosh", wt(0, "campeón") + .1, .4), ("impact", wt(0, "campeón") + .55, .45), ("shimmer", wt(0, "campeón") + .6, .7), ("punch", wt(1, "enero"), .6), ("pop", wt(2, "perdiendo"), .5), ("punch", wt(2, "tres", 1), .6),
        ("clink", wt(2, "Kickoff") + .25, .8), ("impact", wt(2, "Kickoff") + .25, .4), ("punch", wt(3, "quedaba"), .5), ("pop", wt(3, "titular"), .5)] + [("pop", wt(4, n), .5) for n in ("lukxo", "tkzin", "DaviH", "erde", "Darker")] + [
        ("shimmer", wt(5, "veinte"), .5), ("pop", wt(5, "promedio"), .5), ("punch", wt(6, "seis"), .5), ("punch", wt(6, "una"), .5)] + [("pop", wt(7, n), .55) for n in ("Paper", "NRG", "Vitality")] + [
        ("pop", wt(8, "otra") + .35 + j * .3, .45) for j in range(4)] + [("boom", wt(8, "LOUD") + .1, .8), ("cheer", wt(8, "LOUD") + .1, .45), ("shimmer", wt(9, "dos"), .6),
        ("punch", wt(10, "erde"), .6), ("impact", wt(10, "MVP"), .6), ("punch", wt(11, "Darker"), .6), ("shimmer", wt(11, "campeón"), .6),
        ("pop", wt(12, "comentarios"), .6), ("pop", wt(13, "historias"), .7), ("whoosh", wt(13, "compártelo") + .2, .5), ("pop", wt(13, "guárdalo") + .1, .6)]
    for k_, t0, g in ev:
        s = S[k_]; j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .6)):
        w = wave.open(os.path.join(LD, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(LD, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(LD, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(LD, "voz_pro.wav"), "-i", SONG, "-i", os.path.join(LD, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.2[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[md];"
                    f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=longest,atrim=0:{DUR},afade=t=out:st={DUR - 1.5}:d=1.5,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(x).resize((W // 2, H // 2)) for x in ts]; sh = Image.new("RGB", (W // 2 * min(6, len(ims)), H // 2 * ((len(ims) + 5) // 6)))
        for k, x in enumerate(ims): sh.paste(x, ((k % 6) * W // 2, (k // 6) * H // 2))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=85); print("preview", [round(c, 2) for c in SEG], round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(LD, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
