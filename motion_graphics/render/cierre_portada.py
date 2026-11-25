import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
lata0 = Image.open(f"{B}/evento/lata_rec.png").convert("RGBA")
lata = Image.new("RGBA", (int(lata0.width * 2.3), lata0.height)); lata.alpha_composite(lata0, ((lata.width - lata0.width) // 2, 0))   # lienzo ancho → órbita más abierta
# logo: "MONSTER × GTA VI" en morado (texto limpio, sin imitar el logo oficial)
from render_smg import text_layer, ANTON, PUR
logo = text_layer("MONSTER × GTA VI", ANTON(90), PUR)
icons = [S.R.HAB[k] for k in ("neon_0", "jett_0", "raze_0", "reyna_0", "neon_1", "jett_1", "raze_1", "reyna_1") if k in S.R.HAB]
P.portada(f"{B}/evento/cierre_portada.jpg", "LA PROBÉ… ¿Y TÚ?", logo, "ULTRA VICE GUAVA · ZERO SUGAR", lata, icons=icons, ghost="VICE")
Image.open(f"{B}/evento/cierre_portada.jpg").resize((540, 960)).save(f"{B}/evento/cierre_portada_chk.jpg"); print("ok")
