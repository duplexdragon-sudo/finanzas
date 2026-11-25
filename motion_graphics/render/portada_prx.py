import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
from render_smg import text_layer, ANTON, PUR, paste, shadow
B = os.path.abspath("..")
logo = text_layer("PAPER REX", ANTON(120), PUR)
pri0 = Image.open(f"{B}/prx/rec/primmie_head.png").convert("RGBA"); pat0 = Image.open(f"{B}/prx/rec/patmen_head.png").convert("RGBA")
pri0 = pri0.resize((520, int(pri0.height * 520 / pri0.width))); pat0 = pat0.resize((400, int(pat0.height * 400 / pat0.width)))
pri = Image.new("RGBA", (900, pri0.height + 160)); pri.alpha_composite(pat0, (480, 200)); pri.alpha_composite(pri0, (60, 0))
pat = S.duo(Image.open(f"{B}/prx/rec/patmen_head.png").convert("RGBA"), 1.1); pat = pat.resize((190, int(pat.height * 190 / pat.width)))
def extra(im): pass
P.portada(f"{B}/prx/portada_prx_ig.jpg", "LO BARRIERON 3–0… Y LO FICHARON", logo, "PRIMMIE Y PATMEN · PRX 2027", pri,
          icons=[Image.new("RGBA", (4, 4))], ghost="PRX", extra=extra)
Image.open(f"{B}/prx/portada_prx_ig.jpg").resize((400, 711)).save(f"{B}/chk5.jpg"); print("ok")
