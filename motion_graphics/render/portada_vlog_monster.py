import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
from render_smg import text_layer, ANTON, PUR
B = os.path.abspath("..")
logo = text_layer("MONSTER × GTA VI", ANTON(90), PUR)
icons = [S.R.HAB[k] for k in ("neon_0", "jett_0", "raze_0", "reyna_0", "neon_1", "jett_1", "raze_1", "reyna_1") if k in S.R.HAB]
P.portada(f"{B}/evento/portada_vlog_monster.jpg", "FUI AL LANZAMIENTO DE MONSTER", logo, "TP GAMING ARENA · BOGOTÁ",
          Image.open(f"{B}/evento/yo_134.png").convert("RGBA"), icons=icons, ghost="VICE")
Image.open(f"{B}/evento/portada_vlog_monster.jpg").resize((540, 960)).save(f"{B}/evento/portada_chk.jpg"); print("ok")
