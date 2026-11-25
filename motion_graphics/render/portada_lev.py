import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
im = Image.open(f"{B}/lev/logos/leviatan.png").convert("RGBA"); lg = Image.new("RGBA", im.size, S.PUR + (255,)); lg.putalpha(im.getchannel("A")); lg = lg.crop(lg.getbbox())
e = Image.open(f"{B}/loud/rec/erde.png").convert("RGBA"); e = e.crop(e.getbbox()); l = Image.open(f"{B}/lev/rec/p124.png").convert("RGBA"); l = l.crop(l.getbbox())
e = e.resize((400, int(e.height * 400 / e.width))); l = l.resize((400, int(l.height * 400 / l.width)))
H = max(e.height, l.height) + 40; duo2 = Image.new("RGBA", (820, H)); duo2.alpha_composite(l, (420, H - l.height)); duo2.alpha_composite(e, (0, H - e.height))
P.portada(f"{B}/lev/portada_lev_ig.jpg", "MIBR OFRECIÓ MÁS… Y ELIGIERON LEV", lg, "ERDE Y LUKXO · SEGÚN REPORTES", duo2, icons=[Image.new("RGBA", (4, 4))], ghost="LEV")
Image.open(f"{B}/lev/portada_lev_ig.jpg").resize((400, 711)).save(f"{B}/chk9.jpg"); print("ok")
