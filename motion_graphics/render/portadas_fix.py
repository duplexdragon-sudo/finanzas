import os
from PIL import Image
import render_smg as S, render_tenz_morado as TM
S.fade_bottom = TM.fade_bottom
import portada_tpl as P
B = os.path.abspath("..")
def morado(p):
    im = Image.open(p).convert("RGBA"); c = Image.new("RGBA", im.size, S.PUR + (255,)); c.putalpha(im.getchannel("A")); return c
R = S.R
ICONS_AS = [R.HAB[k] for k in ("jett_0","raze_0","neon_0","jett_1","raze_1","neon_1","jett_2","raze_2") if k in R.HAB]
P.portada(f"{B}/aspas/portada_aspas_ig.jpg", "RECHAZÓ MILLONES DE CHINA", morado(f"{B}/aspas/logos/fut.png"),
          "SE VA A FUT ESPORTS · TURQUÍA", Image.open(f"{B}/aspas/rec/aspas_fut_recto.png").convert("RGBA"), icons=ICONS_AS, ghost="ASPAS")
P.portada(f"{B}/sen/portada_sen_ig.jpg", "DE 0 INTERNACIONALES A SUPEREQUIPO", morado(f"{B}/sen/logos/sen_w.png"),
          "SENTINELS 2027 · 4 FICHAJES", Image.open(f"{B}/sen/rec/equipo2.png").convert("RGBA"), ghost="SEN")
im = [Image.open(f"{B}/{p}").resize((400,711)) for p in ("aspas/portada_aspas_ig.jpg","sen/portada_sen_ig.jpg")]
c = Image.new("RGB",(810,711),"white"); c.paste(im[0],(0,0)); c.paste(im[1],(410,0)); c.save(f"{B}/chk2.jpg"); print("ok")
import render_loud as L
P.portada(f"{B}/loud/portada_loud_ig.jpg", "UN COLOMBIANO CAMPEÓN DEL MUNDO", Image.open(f"{B}/loud/logos/loud_p.png").convert("RGBA"),
          "3–1 A VITALITY · CHAMPIONS 2026", Image.open(f"{B}/loud/rec/darker2.png").convert("RGBA"), icons=L.ICON_DK, ghost="DARKER")
im = [Image.open(f"{B}/{p}").resize((400,711)) for p in ("loud/portada_loud_ig.jpg","aspas/portada_aspas_ig.jpg","sen/portada_sen_ig.jpg")]
c = Image.new("RGB",(1220,711),"white")
for i,x in enumerate(im): c.paste(x,(i*410,0))
c.save(f"{B}/chk3.jpg"); print("ok3")
