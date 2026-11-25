#!/usr/bin/env python3
"""EOS — invitación animada al lanzamiento de la Estrategia de Seguros (horizontal 1920x1080).
Colores del logo: azul marino + dorado sobre fondo claro. Uso: python3 render_eos.py salida.mp4 | --preview t1,t2,..."""
import os, sys, math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ED = os.path.join(HERE, "..", "eos"); FONTS = os.path.join(HERE, "..", "fonts")
W, H, FPS = 1920, 1080, 30
NAVY, BLUE, GOLD, GOLD2, BG, INK, WHITE = (10, 42, 110), (12, 84, 190), (247, 180, 20), (255, 214, 70), (246, 247, 251), (20, 28, 48), (255, 255, 255)
# ---- datos del evento (cambiar cuando lleguen) ----
FECHA, HORA, LUGAR = "Lunes 23 de Noviembre", "9:00 a.m. – 10:00 a.m.", "Mezzanine – Dirección General"
DUR = 16.0

def F(name, s): return __import__("PIL.ImageFont", fromlist=["x"]).truetype(os.path.join(FONTS, name + ".ttf"), s)
SANS = lambda w, s: F(f"poppins-{w}-normal", s); SERIF = lambda w, s, it=False: F(f"playfair-display-{w}-{'italic' if it else 'normal'}", s)
def clamp01(x): return max(0., min(1., x))
def prog(t, a, b): return clamp01((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eback(x, s=1.6): x = clamp01(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x
def canvas(c=(0, 0, 0, 0)): return Image.new("RGBA", (W, H), c)
def paste(dst, src, x, y, a=1.0, anchor="mm"):
    if a <= 0: return
    if a < 1: src = src.copy(); src.putalpha(src.getchannel("A").point(lambda v: int(v * a)))
    ox = {"mm": src.width / 2, "lm": 0, "rm": src.width}[anchor]; dst.alpha_composite(src, (int(x - ox), int(y - src.height / 2))) if 0 else _comp(dst, src, int(x - ox), int(y - src.height / 2))
def _comp(dst, src, x, y):
    l, t = max(0, x), max(0, y); r, b = min(dst.width, x + src.width), min(dst.height, y + src.height)
    if r > l and b > t: dst.alpha_composite(src.crop((l - x, t - y, r - x, b - y)), (l, t))
def text(s, font, col, spacing=0):
    if spacing:
        ws = [font.getlength(c) for c in s]; w = int(sum(ws) + spacing * (len(s) - 1)) + 10; hgt = font.size + 30
        im = Image.new("RGBA", (w, hgt)); d = ImageDraw.Draw(im); x = 5
        for c, cw in zip(s, ws): d.text((x, hgt / 2), c, font=font, fill=col, anchor="lm"); x += cw + spacing
        return im
    bb = font.getbbox(s); im = Image.new("RGBA", (bb[2] - bb[0] + 20, bb[3] - bb[1] + 30)); ImageDraw.Draw(im).text((10 - bb[0], 15 - bb[1]), s, font=font, fill=col); return im
def reveal(dst, layer, x, y, T, t0, dur=.5, dy=30, a=1.0):
    p = eo(prog(T, t0, t0 + dur))
    if p <= 0: return
    l = layer
    if p < 1: l = layer.filter(ImageFilter.GaussianBlur(6 * (1 - p)))
    paste(dst, l, x, y + dy * (1 - p), p * a)
def wipe_text(dst, layer, x, y, T, t0, dur=.6, a=1.0):
    p = eio(prog(T, t0, t0 + dur))
    if p <= 0: return
    paste(dst, layer.crop((0, 0, max(1, int(layer.width * p)), layer.height)), x - layer.width / 2, y, a, "lm")

# ---------- recursos ----------
L = {n: Image.open(os.path.join(ED, n + ".png")).convert("RGBA") for n in "EOS"}
LOGO = Image.open(os.path.join(ED, "logo_alpha.png")).convert("RGBA")
def scale(im, s): return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
SC = 900 / LOGO.width; LS = {n: scale(im, SC) for n, im in L.items()}
# posiciones de cada letra dentro del logo armado (en px del logo original 1589 de ancho, letras recortadas en x 190/700/1300)
LX0 = Image.open(os.path.join(ED, "logo.webp")).getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()[0]
LX = {"E": (190 + L["E"].width / 2 - LX0) * SC, "O": (700 + L["O"].width / 2 - LX0) * SC, "S": (1300 + L["S"].width / 2 - LX0) * SC}
LOGO_W = LOGO.width * SC
def bg(T):
    im = canvas(BG + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(232, 235, 243, 255), width=1)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(232, 235, 243, 255), width=1)
    # cintas curvas azul/dorado que se mueven lento (eco del logo)
    lay = canvas(); dl = ImageDraw.Draw(lay)
    for k, (col, a0, yoff) in enumerate(((NAVY, 30, 860), (GOLD, 26, 900), (BLUE, 18, 940))):
        pts = [(x, yoff + 70 * math.sin(x / 420 + T * .5 + k) + k * 10) for x in range(-40, W + 60, 20)]
        dl.line(pts, fill=col + (a0 + 20,), width=14 - k * 3, joint="curve")
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2)))
    return im
SPARK = [(random.Random(k).uniform(0, W), random.Random(k + 3).uniform(0, H), random.Random(k + 7).uniform(2, 5), random.Random(k + 9).uniform(.3, 1)) for k in range(60)]
def sparkles(im, T, a=.7):
    d = ImageDraw.Draw(im)
    for x, y, r, sp in SPARK:
        yy = (y - T * 40 * sp) % H; tw = abs(math.sin(T * 2 * sp + x)); d.ellipse((x - r, yy - r, x + r, yy + r), fill=GOLD2 + (int(200 * a * tw),))
def shine(img, T, t0, dur=.7):
    """Brillo diagonal que barre el logo (solo dentro de su forma)."""
    p = prog(T, t0, t0 + dur)
    if not 0 < p < 1: return img
    w, h = img.size; band = Image.new("L", (w, h), 0); sx = lerp(-w * .4, w * 1.4, p)
    ImageDraw.Draw(band).polygon([(sx, 0), (sx + 90, 0), (sx - h * .5 + 90, h), (sx - h * .5, h)], fill=220)
    band = band.filter(ImageFilter.GaussianBlur(18)); band = Image.fromarray(np.minimum(np.asarray(band), np.asarray(img.getchannel("A"))))
    wl = Image.new("RGBA", (w, h), (255, 255, 255, 0)); wl.putalpha(band); out = img.copy(); out.alpha_composite(wl); return out
def logo_frame(T, cx, cy, s=1.0):
    """Logo armado por piezas: O gira y crece, E entra por la izquierda, S por la derecha."""
    lay = canvas()
    pO = eback(prog(T, .35, 1.05), 1.4); pE = eo(prog(T, .75, 1.25)); pS = eo(prog(T, .85, 1.35))
    for n, p, dx in (("E", pE, -900), ("S", pS, 900), ("O", pO, 0)):
        if p <= 0: continue
        im = LS[n]
        if n == "O":
            ang = lerp(-220, 0, eo(prog(T, .35, 1.1))); im = scale(im, max(.01, p)).rotate(ang, resample=Image.BICUBIC, expand=True)
        if s != 1: im = scale(im, s)
        x = cx - LOGO_W * s / 2 + LX[n] * s + dx * (1 - p); paste(lay, im, x, cy, clamp01(p * 2.5))
    # brillo y halo dorado al quedar armado
    lay = shine(lay, T, 1.55, .8)
    return lay

# ---------- composición ----------
def frame(T):
    im = bg(T)
    # anillo dorado de apertura
    if T < 1.6:
        p = eo(prog(T, .05, .9)); d = ImageDraw.Draw(im); r = lerp(20, 700, p)
        d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=GOLD + (int(255 * (1 - p)),), width=10)
    # el logo: centrado grande, luego sube y se achica
    up = eio(prog(T, 2.6, 3.4)); s = lerp(1.0, .55, up); cy = lerp(H / 2, 250, up)
    glow = clamp01((T - 1.3) * 2) * (1 - clamp01((T - 2.6) * 2))
    if glow > 0:
        g = Image.new("RGBA", (W, H)); ImageDraw.Draw(g).ellipse((W / 2 - 560, H / 2 - 260, W / 2 + 560, H / 2 + 260), fill=GOLD2 + (int(55 * glow),)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))
    if T < 10.3: im.alpha_composite(logo_frame(T, W / 2, cy, s))
    # invitación
    if 3.0 <= T < 10.6:
        a = 1 - clamp01((T - 10.0) * 3)
        reveal(im, text("Te Invitamos al Lanzamiento de la", SANS(500, 44), BLUE), W / 2, 470, T, 3.1, a=a)
        wipe_text(im, text("Estrategia de Seguros", SANS(800, 120), NAVY), W / 2, 580, T, 3.5, .7, a)
        pl = eo(prog(T, 4.2, 4.9)); d = ImageDraw.Draw(im)
        if pl > 0: d.rounded_rectangle((W / 2 - 330 * pl, 675, W / 2 + 330 * pl, 685), 5, fill=GOLD + (int(255 * a),))
        # datos del evento: tres tarjetas
        for k, (lab, val) in enumerate((("Fecha", FECHA), ("Hora", HORA), ("Lugar", LUGAR))):
            t0 = 5.4 + k * .25; p = eback(prog(T, t0, t0 + .45), 1.3)
            if p <= 0: continue
            c = Image.new("RGBA", (540, 150)); dc = ImageDraw.Draw(c); dc.rounded_rectangle((0, 0, 539, 149), 26, fill=WHITE + (255,), outline=(220, 226, 238, 255), width=3)
            dc.rounded_rectangle((0, 0, 14, 149), 7, fill=GOLD + (255,))
            dc.text((277, 48), lab, font=SANS(700, 30), fill=BLUE, anchor="mm"); vf = SANS(600, 36)
            while vf.getlength(val) > 480: vf = SANS(600, vf.size - 2)
            dc.text((277, 100), val, font=vf, fill=INK, anchor="mm")
            sh = Image.new("RGBA", (c.width + 60, c.height + 60)); sm = Image.new("L", sh.size, 0); sm.paste(c.getchannel("A").point(lambda v: 50 if v else 0), (30, 42)); sh.putalpha(sm.filter(ImageFilter.GaussianBlur(14))); sh.alpha_composite(c, (30, 30))
            paste(im, sh, W / 2 + (k - 1) * 580, 880 + 60 * (1 - p), clamp01(p * 2) * a)
    # cierre: panel azul marino con firma
    if T >= 10.0:
        p = eio(prog(T, 10.0, 10.7)); lay = canvas(); d = ImageDraw.Draw(lay); x = lerp(-W * .2, W * 1.25, p)
        d.polygon([(-200, 0), (x, 0), (x - 300, H), (-200, H)], fill=NAVY + (255,)); im.alpha_composite(lay)
        if p >= 1:
            im = canvas(NAVY + (255,)); d = ImageDraw.Draw(im)
            for k in range(3):
                pts = [(xx, 900 + 60 * math.sin(xx / 380 + T * .6 + k) + k * 14) for xx in range(-40, W + 60, 20)]
                d.line(pts, fill=((GOLD, BLUE, GOLD2)[k]) + (90,), width=10 - k * 2, joint="curve")
            # logo sobre tarjeta blanca
            pc = eback(prog(T, 10.7, 11.2), 1.3); card = Image.new("RGBA", (720, 300)); ImageDraw.Draw(card).rounded_rectangle((0, 0, 719, 299), 40, fill=WHITE + (255,))
            lg = scale(LOGO, 560 / LOGO.width); card.alpha_composite(lg, ((720 - lg.width) // 2, (300 - lg.height) // 2)); card = shine(card, T, 11.4, .8)
            paste(im, scale(card, max(.01, .6 + .4 * pc)), W / 2, 300, clamp01(pc * 2))
            reveal(im, text("Invita", SERIF(700, 56, True), GOLD2), W / 2, 530, T, 11.2)
            reveal(im, text("Dirección de Estrategia y Desarrollo Comercial", SANS(700, 56), WHITE), W / 2, 620, T, 11.5)
            pl = eo(prog(T, 11.8, 12.4))
            reveal(im, text("Convenio Banca Seguros", SERIF(700, 66, True), WHITE), W / 2, 730, T, 12.0)
            sparkles(im, T, .8)
    else:
        sparkles(im, T, .45 * clamp01((T - 1.3) * 2))
    if T < .2: im = Image.blend(im, canvas(WHITE + (255,)), 1 - T / .2)
    if T > DUR - .7: im = Image.blend(im, canvas(NAVY + (255,)), prog(T, DUR - .7, DUR - .05))
    return im.convert("RGB")

def audio(out):
    SR = 48000; N = int(DUR * SR); A = os.path.join(HERE, "..", "audio") + "/"
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    fx = np.zeros((N, 2), np.float32); S = {k: rd(A + k + ".48.wav") for k in ("whoosh", "swoosh", "pop", "shimmer", "clink")}; S["rise"] = rd(os.path.join(ED, "rise.wav"))
    ev = [("rise", 0.0, .7), ("swoosh", .75, .5), ("swoosh", .85, .5), ("shimmer", 1.5, .6), ("whoosh", 2.6, .4), ("pop", 3.1, .35), ("swoosh", 3.5, .45), ("clink", 4.5, .4),
          ("pop", 5.4, .4), ("pop", 5.65, .4), ("pop", 5.9, .4), ("swoosh", 10.0, .6), ("rise", 10.6, .5), ("shimmer", 11.4, .6), ("clink", 12.0, .4)]
    for k, t0, g in ev:
        s = S[k]; j = int(t0 * SR); n = min(len(s), N - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    fxp = os.path.join(ED, "sfx.wav"); w = wave.open(fxp, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(fx * .7, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ED, "bed.wav"), "-i", fxp, "-filter_complex",
                    f"[0:a]atrim=0:{DUR},asetpts=PTS-STARTPTS,volume=0.55,afade=t=in:d=0.6,afade=t=out:st={DUR - 1.5}:d=1.5[m];[m][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:{DUR},loudnorm=I=-16:TP=-1.5,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(x).resize((W // 4, H // 4)) for x in ts]; cols = 3; sh = Image.new("RGB", (W // 4 * cols, H // 4 * ((len(ims) + cols - 1) // cols)))
        for k, x in enumerate(ims): sh.paste(x, ((k % cols) * W // 4, (k // cols) * H // 4))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("ok"); sys.exit()
    out = a[0]; mix = os.path.join(ED, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix, "-map", "0:v", "-map", "1:a",
           "-c:a", "aac", "-b:a", "256k", "-t", str(DUR), "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out)
