from PIL import Image, ImageDraw
import render_dia1 as B
from render_dia1 import W, H, PUR, LILL, WHITE, INK, IT, ANTON, SANS, bg, tenz_orbit, text_layer, paste, brackets
import render_tenz_morado as R
im = bg("w", "T1")
rib = Image.new("RGBA", (620, 96), PUR + (255,)); ImageDraw.Draw(rib).text((310, 50), "SU PRIMER DÍA EN", font=ANTON(64), fill=WHITE, anchor="mm")
paste(im, rib, 360, 160)
t1 = R.tint(R.T1, PUR); t1 = t1.resize((380, int(t1.height * 380 / t1.width)), Image.LANCZOS); paste(im, t1, 360, 300)
pill = Image.new("RGBA", (360, 62), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, 359, 61), 31, fill=INK + (255,))
ImageDraw.Draw(pill).text((180, 32), "+1,2 M DE VISTAS", font=ANTON(36), fill=WHITE, anchor="mm"); paste(im, pill, 360, 420)
tenz_orbit(im, 99, 3.0, 360, 1470, 600, 3.0, crown_t0=0)
paste(im, text_layer("¿Lo logra?", IT(900, 104), PUR), 360, 1170)
brackets(im, 5, PUR, .9)
im.convert("RGB").resize((1080, 1920), Image.LANCZOS).save("../dia1/portada_primer_dia_T1.jpg", quality=95); print("ok")
