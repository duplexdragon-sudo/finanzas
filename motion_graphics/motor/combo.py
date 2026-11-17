import sys, numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session
from scipy import ndimage
sys.path.insert(0, '.')
src, dst, crop = sys.argv[1], sys.argv[2], tuple(map(int, sys.argv[3].split(',')))
im = Image.open(src).convert('RGB').crop(crop); im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
fine = np.asarray(remove(im, session=new_session('birefnet-portrait')).getchannel('A')).astype(np.float32) / 255
hum = np.asarray(remove(im, session=new_session('u2net_human_seg')).getchannel('A')) > 100
hum = ndimage.binary_dilation(hum, iterations=14)                     # margen para el pelo
hum = np.asarray(Image.fromarray((hum * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
al = fine * hum
rgb = np.asarray(im).astype(np.float32)
# descontaminación: color del borde = color del interior más cercano
solid = al > .95; idx = ndimage.distance_transform_edt(~solid, return_distances=False, return_indices=True)
near = rgb[idx[0], idx[1]]; edge = (al > 0) & ~solid; rgb[edge] = rgb[edge] * .35 + near[edge] * .65
out = Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8), 'RGBA')
out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 25 else 0).getbbox()); out.save(dst); print('ok', dst)
