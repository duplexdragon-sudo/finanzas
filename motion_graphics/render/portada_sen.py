import os, math
from PIL import Image, ImageDraw
import render_sen as A
from render_sen import *
im = canvas(PUR + (255,)); M_grid(im, (128, 34, 178, 255), 56)
rr = L.RAYS.resize((int(L.RAYS.width * 1.1), int(L.RAYS.height * 1.1))); paste(im, rr, 360, 640, .5)
paste(im, senlogo(90), 360, 120)
paste(im, text_layer("De cero internacionales a", IT(400, 50), LILL), 360, 225)
paste(im, text_layer("SUPEREQUIPO", ANTON(120), WHITE), 360, 330)
ph = OFI.resize((680, int(OFI.height * 680 / OFI.width)), Image.LANCZOS); paste(im, rcard(ph, 30, WHITE), 360, 690)
tl = Image.new("RGBA", (520, 90), WHITE + (255,)); d = ImageDraw.Draw(tl); d.text((260, 47), "SENTINELS 2027", font=ANTON(62), fill=PUR, anchor="mm"); paste(im, tl, 360, 1000)
for k, (nm, sub) in enumerate((("JOHNQT", "se queda"), ("OXY", "ex Cloud9"), ("BRAWK", "campeón 2025"), ("CANEZERRA", "ex Envy"), ("KEIKO", "ex NRG"))):
    c = Image.new("RGBA", (200, 88)); d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, 199, 87), 22, fill=INK + (240,))
    d.text((100, 32), nm, font=ANTON(34), fill=WHITE, anchor="mm"); d.text((100, 66), sub, font=SANS(600, 19), fill=LILL, anchor="mm")
    paste(im, shadow(c, 8, 8, .3), (140, 360, 580, 250, 470)[k], 1110 if k < 3 else 1205)
brackets(im, 2, WHITE, .8)
paste(im, text_layer("@DuplexDragon_", SANS(600, 18), WHITE), 690, 60, .8, "rm")
out = im.convert("RGB").resize((1080, 1920), Image.LANCZOS)
out.save(os.path.join(A.SD, "portada_sen_ig.jpg"), quality=95); out.crop((0, 285, 1080, 1635)).save(os.path.join(A.SD, "portada_sen_ig_4x5.jpg"), quality=95); print("ok")
