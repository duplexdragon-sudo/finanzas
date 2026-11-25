import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath(".."); A = f"{B}/hush/arte"
def ld(n): im = Image.open(f"{A}/{n}").convert("RGBA"); return im.crop(im.getchannel("A").getbbox())
hb = [ld(f"hab_{k}.png") for k in ("passive", "grenade", "ability1", "ability2", "ultimate")]
lg = Image.new("RGBA", (5 * 140 - 20, 120))
for i, h in enumerate(hb):
    h = h.resize((120, int(h.height * 120 / h.width))); t = Image.new("RGBA", h.size, S.PUR + (255,)); t.putalpha(h.getchannel("A")); lg.alpha_composite(t, (i * 140, (120 - h.height) // 2))
icons = [ld(f"hab_{k}.png") for k in ("ability1", "ability2", "grenade", "ultimate", "passive", "ability1", "ability2", "grenade")]
S.duo = lambda im, *a, **k: im                      # Hush a color (arte oficial), sin duotono
P.portada(f"{B}/hush/portada_hush_ig.jpg", "CÓMO USAR A HUSH", lg, "GUÍA TECLA POR TECLA", ld("fullportrait.png"), pregunta="¿Ya la probaste?", icons=icons, ghost="")
from PIL import Image as I
a = I.open(f"{B}/hush/portada_hush_ig.jpg").resize((540, 960)); b = I.open(f"{B}/hush/portada_hush_ig_4x5.jpg").resize((540, 675))
s = I.new("RGB", (1100, 960), "white"); s.paste(a, (0, 0)); s.paste(b, (560, 0)); s.save(f"{B}/edit/chk_portada_hush.jpg"); print("ok")
