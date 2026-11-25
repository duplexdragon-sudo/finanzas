import os
from PIL import Image, ImageDraw
import render_xavi as A
from render_xavi import *
cf = clip(K1, 24.2, 1, CR, (720, 1280), .3); im = Image.blend(cf, canvas(PUR + (255,)), .62)
ring(im, 360, 980, 320, 1.0, WHITE, .4)
ph = XAVI.resize((int(XAVI.width * 1.15), int(XAVI.height * 1.15))); paste(im, ph, 360, 1300 - ph.height / 2)
paste(im, text_layer("Campeón de Pacific…", IT(900, 54), LILL), 360, 150)
paste(im, text_layer("SIN EQUIPO", ANTON(150), WHITE), 360, 270)
stamp(im, "ACUERDO ROTO", 360, 440, 9, 0, (230, 40, 70), -8, 84)
c = Image.new("RGBA", (560, 92)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 559, 91), 46, fill=WHITE + (255,))
d.text((280, 48), "XLG ELIGIÓ A OTRO EN 30 MIN", font=ANTON(42), fill=PUR, anchor="mm"); paste(im, shadow(c, 8, 8, .3), 360, 590)
pop(im, PH.resize((130, 87)), 600, 760, 9, 0, .3)
tag = Image.new("RGBA", (300, 70), INK + (255,)); ImageDraw.Draw(tag).text((150, 37), "XAVI8K", font=ANTON(50), fill=WHITE, anchor="mm"); paste(im, tag, 360, 1180)
brackets(im, 2, WHITE, .8); paste(im, text_layer("@DuplexDragon_", SANS(600, 18), WHITE), 690, 60, .8, "rm")
out = im.convert("RGB").resize((1080, 1920), Image.LANCZOS)
out.save(os.path.join(A.XD, "portada_xavi_ig.jpg"), quality=95); out.crop((0, 285, 1080, 1635)).save(os.path.join(A.XD, "portada_xavi_ig_4x5.jpg"), quality=95); print("ok")
