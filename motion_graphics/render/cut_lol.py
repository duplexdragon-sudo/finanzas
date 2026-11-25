import sys
from PIL import Image, ImageFilter
from rembg import remove, new_session
src, dst, model = sys.argv[1], sys.argv[2], sys.argv[3]; crop = tuple(map(int, sys.argv[4].split(","))) if len(sys.argv) > 4 else None
im = Image.open(src).convert("RGB")
if crop: im = im.crop(crop)
im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
o = remove(im, session=new_session(model)); o = o.crop(o.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox()); o.save(dst); print("ok", dst, o.size)
