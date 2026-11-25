import os, numpy as np
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
im = Image.open(f"{B}/fnc/logos/fnatic.png").convert("RGBA"); a = np.asarray(im).astype(float); m = np.clip((255 * 3 - a[..., :3].sum(2) - 60) * 2, 0, 255) * (a[..., 3] / 255)
lg = Image.new("RGBA", im.size, S.PUR + (255,)); lg.putalpha(Image.fromarray(m.astype(np.uint8))); lg = lg.crop(lg.getbbox())
P.portada(f"{B}/fnc/portada_fnc_ig.jpg", "FIN DE UNA ERA EN FNATIC", lg, "SE VA BOASTER · LLEGARÍA VALYN", Image.open(f"{B}/fnc/rec/boaster.png").convert("RGBA"),
          icons=[Image.new("RGBA", (4, 4))], ghost="FNC")
Image.open(f"{B}/fnc/portada_fnc_ig.jpg").resize((400, 711)).save(f"{B}/chk6.jpg"); print("ok")
