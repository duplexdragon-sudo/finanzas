import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
im = Image.open(f"{B}/vit/logos/vitality.webp").convert("RGBA"); lg = Image.new("RGBA", im.size, S.PUR + (255,)); lg.putalpha(im.getchannel("A")); lg = lg.crop(lg.getbbox())
icons = [S.R.HAB[k] for k in ("neon_0", "neon_1", "neon_2", "neon_3") * 2 if k in S.R.HAB]
P.portada(f"{B}/vit/portada_vit_ig.jpg", "PERDIÓ LA FINAL… Y FICHÓ A UN CAMPEÓN", lg, "JAWGEMO LLEGA A VITALITY", Image.open(f"{B}/vit/rec/jawgemo.png").convert("RGBA"),
          icons=icons, ghost="VIT")
Image.open(f"{B}/vit/portada_vit_ig.jpg").resize((400, 711)).save(f"{B}/chk7.jpg"); print("ok")
