import os, math
from PIL import Image, ImageDraw
import render_aspas as A
from render_aspas import *
cf = clip(MOV, 24, 2, (0, 420, 500, 600), (720, 1280), 0.5); im = Image.blend(cf, canvas(PUR + (255,)), .68)
ring(im, 360, 900, 320, 1.0, WHITE, .4)
ph = ASP_F.resize((int(ASP_F.width * 1.12), int(ASP_F.height * 1.12)))
paste(im, ph, 360, 1300 - ph.height / 2)
paste(im, text_layer("Rechazó millones de", IT(400, 56), LILL), 360, 140)
paste(im, text_layer("CHINA", ANTON(190), WHITE), 330, 270)
paste(im, CN.resize((120, 80)), 625, 290)
stamp(im, "NO", 625, 290, 9, 0, (255, 255, 255), -12, 52)
rib = Image.new("RGBA", (680, 96), WHITE + (255,)); ImageDraw.Draw(rib).text((340, 50), "Y SE VA A TURQUÍA", font=ANTON(66), fill=PUR, anchor="mm"); paste(im, rib, 360, 435)
paste(im, TR.resize((120, 80)), 360, 530)
tag = Image.new("RGBA", (330, 70), INK + (255,)); ImageDraw.Draw(tag).text((165, 37), "FUT ESPORTS · 2027", font=ANTON(40), fill=WHITE, anchor="mm"); paste(im, tag, 360, 620)
confetti(im, 1.2, 0); particles(im, 3.0, WHITE, .45); brackets(im, 2, WHITE, .8)
paste(im, text_layer("@DuplexDragon_", SANS(600, 18), WHITE), 690, 60, .8, "rm")
out = im.convert("RGB").resize((1080, 1920), Image.LANCZOS)
out.save(os.path.join(A.AD, "portada_aspas_ig.jpg"), quality=95); out.crop((0, 285, 1080, 1635)).save(os.path.join(A.AD, "portada_aspas_ig_4x5.jpg"), quality=95); print("ok")
