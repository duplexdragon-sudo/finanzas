import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
im = Image.open(f"{B}/zek/logos/nrg.png").convert("RGBA"); lg = Image.new("RGBA", im.size, S.PUR + (255,)); lg.putalpha(im.getchannel("A")); lg = lg.crop(lg.getbbox())
icons = [S.R.HAB[k] for k in ("neon_0", "raze_0", "jett_0", "neon_1", "raze_1", "jett_1", "neon_2", "raze_2") if k in S.R.HAB]
P.portada(f"{B}/zek/portada_zek_ig.jpg", "ADIÓS MIBR… HOLA CAMPEONES", lg, "ZEKKEN A NRG · SEGÚN REPORTES", Image.open(f"{B}/zek/rec/zekken_mibr2.png").convert("RGBA"), icons=icons, ghost="NRG")
Image.open(f"{B}/zek/portada_zek_ig.jpg").resize((400, 711)).save(f"{B}/chk8.jpg"); print("ok")
