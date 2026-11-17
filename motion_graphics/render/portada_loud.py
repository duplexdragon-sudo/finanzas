import math, os
from PIL import Image, ImageDraw
import render_loud as L
from render_loud import *
T = 2.9
im = bg("p", "LOUD"); stripes(im, 5, 0, WHITE); ring(im, 360, 760, 330, T, LILL, .5)
flag_wave(im, 3.0, 0, 860, 260)
trophy_fx(im, 3.2, 1.6, 545, 720, 400)
ph = DARKER_H.resize((int(DARKER_H.width * 1.08), int(DARKER_H.height * 1.08)))
player_orbit(im, ph, 330, 1240, T, 1.2, ICON_DK, 1, 70, WHITE, LILL)
ribbon(im, "UN COLOMBIANO", 360, 235, 9, 0, WHITE, PUR, 74, "mm")
paste(im, text_layer("CAMPEÓN", ANTON(165), WHITE), 360, 420)
paste(im, text_layer("DEL MUNDO", ANTON(100), LILL), 360, 545)
pill = Image.new("RGBA", (470, 70)); d = ImageDraw.Draw(pill); d.rounded_rectangle((0, 0, 469, 69), 35, fill=WHITE + (255,))
d.text((235, 36), "LOUD · CHAMPIONS SHANGHAI 2026", font=ANTON(34), fill=PUR, anchor="mm"); paste(im, pill, 360, 1010)
particles(im, 4.0, WHITE, .5); brackets(im, 2, WHITE, .8)
paste(im, text_layer("@DuplexDragon_", SANS(600, 22), WHITE), 360, 1080, .9)
out = im.convert("RGB").resize((1080, 1920), Image.LANCZOS)
out.save(os.path.join(L.LD, "portada_loud_ig.jpg"), quality=95)
out.crop((0, 285, 1080, 1635)).save(os.path.join(L.LD, "portada_loud_ig_4x5.jpg"), quality=95)
print("ok")
