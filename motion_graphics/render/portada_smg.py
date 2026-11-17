import math, os
from PIL import Image, ImageDraw
import render_smg as S
from render_smg import *
im = bg("p", "4"); stripes(im, 5, 0, WHITE); ring(im, 360, 640, 330, 2.0, LILL, .45)
paste(im, R.tint(SMG_I, WHITE).resize((110, int(SMG_I.height * 110 / SMG_I.width))), 360, 120)
paste(im, text_layer("4 DUELISTAS", ANTON(140), WHITE), 345, 270)
for j, n in enumerate(("neon", "raze", "reyna", "phoenix")):
    a = AGC[n].resize((int(AGC[n].width * .78), int(AGC[n].height * .78))); paste(im, a, 130 + j * 153, 540)
stamp(im, "POR ERROR", 360, 545, 9, 0, (220, 40, 70), -10, 110)
g = GROUP.resize((500, int(GROUP.height * 500 / GROUP.width))); paste(im, g, 360, 880 + g.height / 2)
pill = Image.new("RGBA", (560, 96)); d = ImageDraw.Draw(pill); d.rounded_rectangle((0, 0, 559, 95), 48, fill=WHITE + (255,))
d.text((280, 50), "Y AUN ASÍ GANARON", font=ANTON(56), fill=PUR, anchor="mm"); paste(im, shadow(pill, 10, 10, .3), 360, 770)
tag = Image.new("RGBA", (470, 52)); d = ImageDraw.Draw(tag); d.rounded_rectangle((0, 0, 469, 51), 26, fill=INK + (230,))
d.text((235, 27), "TEAM SMG · GAME CHANGERS 2023", font=ANTON(30), fill=WHITE, anchor="mm"); paste(im, tag, 360, 845)
particles(im, 4.0, WHITE, .5); brackets(im, 2, WHITE, .8)
paste(im, text_layer("@DuplexDragon_", SANS(600, 22), WHITE), 360, 1250, .9)
out = im.convert("RGB").resize((1080, 1920), Image.LANCZOS)
out.save(os.path.join(S.DD, "portada_smg_ig.jpg"), quality=95)
out.crop((0, 285, 1080, 1635)).save(os.path.join(S.DD, "portada_smg_ig_4x5.jpg"), quality=95); print("ok")
