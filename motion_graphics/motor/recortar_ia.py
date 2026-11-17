#!/usr/bin/env python3
"""Recorte con IA (rembg isnet) + limpieza de bordes (decontaminación de color). Motor Morado."""
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from rembg import remove, new_session
SES = new_session("isnet-general-use")
def limpiar(o):
    a = np.asarray(o).astype(np.float32); al = a[..., 3] / 255
    al = np.clip((al - .08) / .84, 0, 1)                                   # quita el velo de sombra muy tenue
    solid = al > .97
    # color de borde = color del interior más cercano (quita el halo claro del fondo)
    idx = ndimage.distance_transform_edt(~solid, return_distances=False, return_indices=True)
    rgb = a[..., :3].copy(); near = rgb[idx[0], idx[1]]
    edge = (al > 0) & ~solid; rgb[edge] = near[edge]
    al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))).astype(np.float32) / 255
    out = Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8), "RGBA")
    bb = out.getchannel("A").point(lambda v: 255 if v > 25 else 0).getbbox(); return out.crop(bb)
def recortar(src, dst, crop=None):
    im = Image.open(src).convert("RGB")
    if crop: im = im.crop(crop)
    o = remove(im, session=SES, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=20, alpha_matting_erode_size=8)
    limpiar(o).save(dst); print("ok", dst.split("/")[-1])
if __name__ == "__main__":
    recortar(sys.argv[1], sys.argv[2])
