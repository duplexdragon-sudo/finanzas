#!/usr/bin/env python3
"""Plantilla de portada DuplexDragon (estilo 'Su primer día en T1'):
fondo blanco con cuadrícula · cinta morada con título · logo del equipo en morado · pastilla negra con el dato ·
persona en morado con habilidades en anillo · pregunta grande en cursiva morada abajo."""
import math, os
from PIL import Image, ImageDraw
import render_smg as S
from render_smg import W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, SANS, bg, shadow, text_layer, paste, brackets, R

def fit(font_fn, txt, maxw, start):
    s = start
    while font_fn(s).getlength(txt) > maxw and s > 20: s -= 2
    return font_fn(s)

def portada(out_path, titulo, logo, pastilla, persona, pregunta=None, icons=None, ghost="", extra=None):
    """logo: RGBA ya en morado (o None). persona: RGBA recortado (se pasa a duotono). icons: lista de íconos de habilidades."""
    im = bg("w", ghost)
    # cinta morada con el título
    f = fit(ANTON, titulo, 540, 88); dy = 0
    if f.size >= 64:
        rib = Image.new("RGBA", (580, 92), PUR + (255,)); ImageDraw.Draw(rib).text((290, 48), titulo, font=f, fill=WHITE, anchor="mm"); paste(im, rib, 360, 245)
    else:   # título largo: dos líneas, letra grande
        ws = titulo.split(); best = min(range(1, len(ws)), key=lambda k: abs(len(" ".join(ws[:k])) - len(" ".join(ws[k:]))))
        l1, l2 = " ".join(ws[:best]), " ".join(ws[best:]); f = min((fit(ANTON, l, 540, 80) for l in (l1, l2)), key=lambda x: x.size)
        rib = Image.new("RGBA", (580, 170), PUR + (255,)); d = ImageDraw.Draw(rib)
        d.text((290, 46), l1, font=f, fill=WHITE, anchor="mm"); d.text((290, 124), l2, font=f, fill=WHITE, anchor="mm"); paste(im, rib, 360, 284); dy = 78
    if logo is not None:
        lh = 150 if logo.width < logo.height * 1.2 else 120; lg = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
        if lg.width > 340: lg = logo.resize((340, int(logo.height * 340 / logo.width)), Image.LANCZOS)
        paste(im, lg, 360, 370 + dy)
    pf = fit(ANTON, pastilla, 540, 62); pw = int(pf.getlength(pastilla)) + 90
    p = Image.new("RGBA", (pw, 96)); ImageDraw.Draw(p).rounded_rectangle((0, 0, pw - 1, 95), 48, fill=INK + (255,))
    ImageDraw.Draw(p).text((pw / 2, 50), pastilla, font=pf, fill=WHITE, anchor="mm"); paste(im, shadow(p, 10, 10, .3), 360, 505 + dy)
    ph = S.duo(persona, 1.08); ph = ph.crop(ph.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
    top = 552 + dy; ht = (1170 if pregunta else 1290) - top          # la cabeza queda casi pegada a la pastilla negra
    sc = ht / ph.height
    if ph.width * sc > 780: sc = 780 / ph.width                       # foto ancha: se agranda y se sale un poco por los lados
    ph = ph.resize((max(1, int(ph.width * sc)), max(1, int(ph.height * sc))), Image.LANCZOS)
    ph = S.fade_bottom(ph, .12) if hasattr(S, "fade_bottom") else ph
    import numpy as np
    _a = np.asarray(ph.getchannel("A")) > 120; _top = _a[: int(ph.height * .35)]; _cols = np.where(_top.any(0))[0]
    cx = 360 + (ph.width / 2 - (_cols.min() + _cols.max()) / 2) if len(_cols) else 360
    S.player_orbit(im, ph, cx, top + ph.height, 0, 2.3, icons or S.ICON_CY, 1.0, 66, PUR, LIL)   # anclada arriba
    if extra: extra(im)
    if pregunta:
      qf = fit(lambda s: IT(900, s), pregunta, 580, 110); bb = qf.getbbox(pregunta); q = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40))
      ImageDraw.Draw(q).text((20 - bb[0], 20 - bb[1]), pregunta, font=qf, fill=PUR, stroke_width=7, stroke_fill=WHITE); paste(im, q, 360, 905)
    brackets(im, 2, PUR, .9)
    from PIL import ImageFilter
    out = im.convert("RGB").resize((2160, 3840), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))   # 4K vertical
    out.save(out_path, quality=96, subsampling=0)
    out.crop((0, 570, 2160, 3270)).save(out_path.replace(".jpg", "_4x5.jpg"), quality=96, subsampling=0); return out_path
