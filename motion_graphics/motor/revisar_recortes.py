#!/usr/bin/env python3
"""Bot revisor de recortes (Motor Morado). Uso: python3 revisar_recortes.py img1.png img2.png ... -> hoja_recortes.jpg + informe."""
import sys, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
def revisar(p):
    im = Image.open(p).convert("RGBA"); a = np.asarray(im).astype(np.float32); al = a[..., 3]; rgb = a[..., :3]
    lum = rgb.mean(-1); sat = rgb.max(-1) - rgb.min(-1); op = al > 128
    av = []
    # 1) borde claro: píxeles del contorno (alfa parcial o pegados al borde) que son gris claro casi sin color
    edge = op & ~ndimage.binary_erosion(op, iterations=3)
    halo = (edge & (lum > 200) & (sat < 22)).sum() / max(1, edge.sum())
    if halo > .18: av.append(f"borde claro {halo:.0%}")
    # 2) recortado: el objeto toca el borde de la imagen (salvo abajo si es un desvanecido intencional)
    for nom, fila in (("arriba", op[0]), ("izquierda", op[:, 0]), ("derecha", op[:, -1])):
        if fila.mean() > .08: av.append(f"tocado {nom} {fila.mean():.0%}")
    # 3) fondo atrapado dentro: zonas opacas grandes gris claro sin color
    trap = op & (lum > 222) & (sat < 10); lab, n = ndimage.label(trap)
    big = sum(1 for s in ndimage.sum(trap, lab, range(1, n + 1)) if s > op.sum() * .01) if n else 0
    if big: av.append(f"fondo atrapado ({big} zonas)")
    # 4) islas sueltas
    lab, n = ndimage.label(op); sz = ndimage.sum(op, lab, range(1, n + 1)) if n else []
    islas = sum(1 for s in sz if s < max(sz) * .003) if n else 0
    if islas > 25: av.append(f"{islas} puntitos sueltos")
    return im, av
if __name__ == "__main__":
    fs = sys.argv[1:]; tiles = []; f = ImageFont.load_default()
    for p in fs:
        im, av = revisar(p); print(("⚠ " if av else "✓ ") + os.path.basename(p), "—", ", ".join(av) or "bien")
        t = im.copy(); t.thumbnail((230, 230)); c = Image.new("RGB", (250, 280), (115, 16, 165))
        c.paste(t, ((250 - t.width) // 2, 10), t); d = ImageDraw.Draw(c)
        d.text((6, 245), os.path.basename(p)[:30], fill=(255, 255, 255), font=f); d.text((6, 262), ("⚠ " + av[0]) if av else "OK", fill=(255, 220, 90) if av else (150, 255, 150), font=f)
        tiles.append(c)
    cols = 6; rows = (len(tiles) + cols - 1) // cols; S = Image.new("RGB", (250 * cols, 280 * rows), (40, 0, 60))
    for i, t in enumerate(tiles): S.paste(t, ((i % cols) * 250, (i // cols) * 280))
    S.save("hoja_recortes.jpg", quality=90)
