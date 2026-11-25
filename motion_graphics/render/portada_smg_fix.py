import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
lg = Image.open(f"{B}/duel/logos/smg_icono.png").convert("RGBA"); c = Image.new("RGBA", lg.size, S.PUR + (255,)); c.putalpha(lg.getchannel("A"))
P.portada(f"{B}/duel/portada_smg_ig.jpg", "4 DUELISTAS… POR ERROR", c, "Y AUN ASÍ GANARON 13–3",
          Image.open(f"{B}/duel/rec/enerii.png").convert("RGBA"), icons=S.ICON_CY, ghost="SMG")
Image.open(f"{B}/duel/portada_smg_ig.jpg").resize((400,711)).save(f"{B}/chk4.jpg"); print("ok")
