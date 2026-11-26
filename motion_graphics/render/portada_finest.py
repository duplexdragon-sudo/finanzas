import os
from PIL import Image, ImageDraw, ImageFilter
import render_smg as S
from render_smg import PUR, LIL, WHITE, INK, ANTON, IT, bg, shadow, paste, brackets
B = os.path.abspath(".."); A = f"{B}/finest/arte"
def ld(n): im = Image.open(f"{A}/{n}").convert("RGBA"); return im.crop(im.getchannel("A").getbbox())
sp = ld("spray.png"); sp = sp.resize((430, int(sp.height * 430 / sp.width)), Image.LANCZOS)
icons = [S.R.HAB[k] for k in ("jett_0", "jett_1", "jett_2", "jett_3", "jett_0", "jett_1", "jett_2", "jett_3") if k in S.R.HAB]
im = bg("w", "")
def fit(fn, t, w, s):
    while fn(s).getlength(t) > w and s > 20: s -= 2
    return fn(s)
f = fit(ANTON, "REVIVE ME, JETT", 540, 92); rib = Image.new("RGBA", (590, 110), PUR + (255,)); ImageDraw.Draw(rib).text((295, 57), "REVIVE ME, JETT", font=f, fill=WHITE, anchor="mm"); paste(im, rib, 360, 255)
pt = "LA HISTORIA REAL · FINEST"; pf = fit(ANTON, pt, 520, 52); pw = int(pf.getlength(pt)) + 80
p = Image.new("RGBA", (pw, 84)); ImageDraw.Draw(p).rounded_rectangle((0, 0, pw - 1, 83), 42, fill=INK + (255,)); ImageDraw.Draw(p).text((pw / 2, 44), pt, font=pf, fill=WHITE, anchor="mm"); paste(im, shadow(p, 10, 10, .3), 360, 365)
S.player_orbit(im, sp, 360, 455 + sp.height, 0, 2.3, icons, 1.0, 62, PUR, LIL)
qf = fit(lambda s_: IT(900, s_), "Nunca olvidado", 560, 100); bb = qf.getbbox("Nunca olvidado")
q = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40)); ImageDraw.Draw(q).text((20 - bb[0], 20 - bb[1]), "Nunca olvidado", font=qf, fill=PUR, stroke_width=7, stroke_fill=WHITE)
paste(im, q, 360, 1010)
brackets(im, 2, PUR, .9)
out = im.convert("RGB").resize((2160, 3840), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
out.save(f"{B}/finest/portada_finest_ig.jpg", quality=96, subsampling=0)
out.crop((0, 570, 2160, 3270)).save(f"{B}/finest/portada_finest_ig_4x5.jpg", quality=96, subsampling=0)
a = Image.open(f"{B}/finest/portada_finest_ig.jpg").resize((540, 960)); b = Image.open(f"{B}/finest/portada_finest_ig_4x5.jpg").resize((540, 675))
s = Image.new("RGB", (1100, 960), "white"); s.paste(a, (0, 0)); s.paste(b, (560, 0)); s.save(f"{B}/edit/chk_portada_fin.jpg"); print("ok")
