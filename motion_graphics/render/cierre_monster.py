#!/usr/bin/env python3
"""Cierre tipo portada para el vlog de Monster: lata al centro con habilidades de Valorant girando, 'VI' estilo GTA 6 arriba,
letra blanca sobre morado (plantilla de la guía). Salida: imagen fija + clip de 3,5 s."""
import os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_smg as S
import plantilla_texto as T
import demo_evento as D                     # sunset(): relleno degradado de cielo + borde blanco + contorno oscuro
B = os.path.abspath(".."); EV = os.path.join(B, "evento"); W, H, FPS = T.W, T.H, 30
LATA = Image.open(os.path.join(EV, "lata_rec.png")).convert("RGBA"); LATA = LATA.resize((int(LATA.width * 480 / LATA.height), 480), Image.LANCZOS)
PAD = Image.new("RGBA", (600, int(LATA.height * 1.45))); PAD.alpha_composite(LATA, ((600 - LATA.width) // 2, 0))     # lienzo ancho y alto → anillo amplio a la altura de la base
GTA = Image.open(os.path.join(EV, "gta6_logo.png")).convert("RGBA"); GTA = GTA.resize((580, int(GTA.height * 580 / GTA.width)), Image.LANCZOS)
ICONS = [S.R.HAB[k] for k in ("neon_0", "jett_0", "raze_0", "reyna_0", "neon_1", "jett_1", "raze_1", "reyna_1") if k in S.R.HAB]
def fondo(t):
    im = S.bg("w", "")                                 # fondo blanco con cuadrícula, como tus portadas
    S.ring(im, 360, 680, 330, t * 1.2, T.PUR, .3); S.ring(im, 360, 680, 280, -t * 1.4, T.LIL, .3, 3, 24)
    return im
def frame(t):
    im = fondo(t); e = lambda a, b: max(0, min(1, (t - a) / (b - a)))
    p = e(0, .35)
    if p > 0:
        sc = 1.12 - .12 * (1 - (1 - p) ** 3); g = GTA.resize((int(GTA.width * sc), int(GTA.height * sc)), Image.LANCZOS); g.putalpha(g.getchannel("A").point(lambda v: int(v * p * .95)))
        im.alpha_composite(g, (int(360 - g.width / 2), int(600 - g.height / 2)))          # logo oficial de GTA VI detrás de la lata        # 'VI' grande DETRÁS de la lata
    p2 = e(.15, .55); lat = LATA.copy()
    gl = Image.new("RGBA", (lat.width + 120, lat.height + 120)); g = Image.new("RGBA", lat.size, (255, 120, 220, 0)); g.putalpha(lat.getchannel("A")); gl.alpha_composite(g, (60, 60))
    gl = gl.filter(ImageFilter.GaussianBlur(30))
    ytop = 330 + 60 * (1 - p2) + 8 * math.sin(t * 2.2); yb = ytop + PAD.height
    im.alpha_composite(gl, (int(360 - gl.width / 2), int(ytop - 60)))
    S.player_orbit(im, PAD, 360, yb, t, max(0, t - .3), ICONS, p2, 72, T.PUR, T.LIL)            # habilidades girando (detrás y delante de la lata)
    if t > .7: T.etiqueta(im, "MONSTER × GTA VI · ULTRA VICE GUAVA", y=215, size=30, alpha=e(.7, .95))
    if t > 1.0: D.sunset(im, "¿LA PROBASTE?", T.ANTON, 104, 925, track=3, sc=1.2 - .2 * e(1.0, 1.25), alpha=e(1.0, 1.25))
    if t > 1.3: T.etiqueta(im, "@DUPLEXDRAGON_", y=1012, alpha=e(1.3, 1.5))
    return im.convert("RGB")
if __name__ == "__main__":
    frame(2.5).save(os.path.join(EV, "CIERRE_monster.jpg"), quality=94)
    DUR = 3.5; out = os.path.join(EV, "CIERRE_monster.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok")
