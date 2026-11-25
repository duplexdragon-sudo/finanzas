import os
from PIL import Image, ImageDraw
import render_smg as S
import plantilla_texto as T
B = os.path.abspath(".."); EV = os.path.join(B, "evento", "ref")
W, H = T.W, T.H
import grade_cine as G
def toma(ref, t, crop):
    return G.toma(os.path.join(EV, ref + ".mp4"), t, crop)
fr = []
# 1 · Gancho 0–2 s
a = toma("r3", 30.5, (300, 0, 324, 495)); T.titular(a, "MONSTER × GTA VI"); T.acento(a, "lo probé", color=T.LILL, y=T.TIT_Y - 85); T.etiqueta(a, "MONSTER · LANZAMIENTO", box=(255, 255, 255), fg=T.PUR); fr.append(("0–2 s · GANCHO", a))
# 2 · Contexto 2–8 s
a = toma("r1", 4.6, (222, 0, 324, 495)); T.titular(a, "TP GAMING ARENA", size=100); T.subtitulo(a, "Bogotá · 21 de noviembre · solo para mayores de 18"); fr.append(("2–8 s · CONTEXTO", a))
# 3 · Desarrollo 1 (plano medio)
a = toma("r3", 15.5, (350, 0, 324, 495)); T.etiqueta(a, "DATO 1", box=(255, 255, 255), fg=T.PUR, y=200); T.subtitulo(a, "Torneos de GTA en pantallas gigantes"); fr.append(("8–20 s · PLANO MEDIO", a))
# 4 · Desarrollo 2 (detalle: la lata real del póster sobre fondo morado)
a = Image.new("RGBA", (W, H), T.PUR + (255,))
lat = Image.open(os.path.join(B, "evento", "poster_lata.webp")).convert("RGBA"); lat = lat.crop((205, 160, 400, 580)); lat = lat.resize((int(lat.width * 600 / lat.height), 600), Image.LANCZOS)
m = Image.new("L", lat.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, lat.width - 1, lat.height - 1), 30, fill=255); lat.putalpha(m)
a.alpha_composite(lat, ((W - lat.width) // 2, 320))
T.titular(a, "SABE A GUAYABA", size=96, y=230); T.subtitulo(a, "cero azúcar · ultra vice guava", y=990); fr.append(("20–32 s · DETALLE", a))
# 5 · Giro / pregunta 40–55 s
a = toma("r3", 44.0, (300, 0, 324, 495)); T.titular(a, "¿VALE LA PENA?"); T.acento(a, "mi opinión", color=T.LILL, y=T.TIT_Y - 85); T.subtitulo(a, "Te digo la verdad al final"); fr.append(("40–55 s · GIRO", a))
# 6 · Cierre en bucle 55–60 s
a = Image.new("RGBA", (W, H), T.PUR + (255,)); T.titular(a, "MONSTER", y=420); T.etiqueta(a, "ULTRA VICE GUAVA", box=(255, 255, 255), fg=T.PUR, y=540)
T.subtitulo(a, "¿La probaste? Te leo en los comentarios", y=700); T.etiqueta(a, "@DUPLEXDRAGON_", y=820); fr.append(("55–60 s · CIERRE EN BUCLE", a))
sw, sh = W // 2, H // 2; out = Image.new("RGB", (sw * 3 + 40, (sh + 50) * 2 + 10), (255, 255, 255)); dd = ImageDraw.Draw(out)
for k, (lab, im) in enumerate(fr):
    x = (k % 3) * (sw + 20); y = (k // 3) * (sh + 60)
    out.paste(im.convert("RGB").resize((sw, sh)), (x, y + 40)); dd.text((x + sw / 2, y + 20), lab, font=T.OSW(24), fill=T.PUR, anchor="mm")
out.save(os.path.join(B, "evento", "STORYBOARD_monster_morado.jpg"), quality=92); print("ok")
