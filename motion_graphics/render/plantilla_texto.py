#!/usr/bin/env python3
"""Plantilla fija de texto — guía "Noticias Valorant: guía para ser el mejor" (21 nov 2026).
3+1 fuentes fijas: Anton (titular), Montserrat ExtraBold (subtítulo), Permanent Marker (acento), Oswald (etiqueta).
Zona segura 870×1360 dentro de 1080×1920 (180 arriba, 380 abajo, 60 izq., 150 der.). Lienzo de trabajo 720×1280 (escala 2/3)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
W, H = 720, 1280; K = W / 1080
SAFE = (int(60 * K), int(180 * K), int((1080 - 150) * K), int((1920 - 380) * K))      # x0, y0, x1, y1 → (40, 120, 620, 1027)
SAFE_CX = W / 2                                          # eje centrado en la pantalla
SAFE_W = 2 * min(SAFE_CX - SAFE[0], SAFE[2] - SAFE_CX)    # ancho simétrico que respeta los 150 px de la derecha
TIT_Y = SAFE[1] + (SAFE[3] - SAFE[1]) * .22          # tercio superior de la zona segura
SUB_Y = H * .55                                       # subtítulos: centro al 50–60 % de la altura
ANTON = lambda s: ImageFont.truetype(os.path.join(F, "anton-400-normal.ttf"), s)
MONT = lambda s: ImageFont.truetype(os.path.join(F, "montserrat-800.ttf"), s)
MARK = lambda s: ImageFont.truetype(os.path.join(F, "permanent-marker.ttf"), s)
OSW = lambda s: ImageFont.truetype(os.path.join(F, "oswald-500.ttf"), s)
PUR = (115, 16, 165); LIL = (166, 97, 196); LILL = (228, 205, 238)
BRAND = PUR                                           # color de marca: el morado de siempre

def _fit(txt, mk, size, maxw):
    while size > 16 and mk(size).getlength(txt) > maxw: size -= 2
    return mk(size)

def _layer(txt, font, fill, stroke):
    bb = font.getbbox(txt, stroke_width=stroke); pad = 30
    lay = Image.new("RGBA", (bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2)); d = ImageDraw.Draw(lay)
    d.text((pad - bb[0], pad - bb[1]), txt, font=font, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); return lay

def _put(im, lay, cx, cy, alpha=1.0, sc=1.0, rot=0, shadow=True):
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    if sc != 1.0: lay = lay.resize((max(1, int(lay.width * sc)), max(1, int(lay.height * sc))), Image.LANCZOS)
    if shadow:
        sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .55)))
        out = Image.new("RGBA", lay.size); out.alpha_composite(sh, (0, 4)); out.alpha_composite(lay); lay = out
    if alpha < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * max(0, alpha))))
    x = cx - lay.width / 2                                                            # centrado exacto
    im.alpha_composite(lay, (int(x), int(cy - lay.height / 2)))

def titular(im, txt, y=None, color=(255, 255, 255), size=140, **kw):
    """Titular / gancho: Anton, 1–3 palabras en MAYÚSCULAS, 140–220 px en 1080 (≈95–145 aquí), blanco con borde negro."""
    f = _fit(txt.upper(), ANTON, int(size * K * 1.0) if size > 150 else size, SAFE_W)
    _put(im, _layer(txt.upper(), f, color, max(2, f.size // 30)), SAFE_CX, TIT_Y if y is None else y, **kw)

def subtitulo(im, txt, y=None, size=48, **kw):
    """Subtítulo: Montserrat ExtraBold, 60–80 px en 1080 (≈40–53 aquí), frase normal (minúsculas), 1–2 líneas."""
    words = txt.split()
    while True:
        f = MONT(size); lines, cur = [], ""
        for w_ in words:
            if f.getlength((cur + " " + w_).strip()) > SAFE_W - 20 and cur: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines.append(cur)
        if len(lines) <= 2 or size <= 30: break
        size -= 2                                   # nunca se corta texto: se achica hasta caber en 2 líneas
    y0 = (SUB_Y if y is None else y) - (len(lines) - 1) * f.size * .6
    for k, ln in enumerate(lines): _put(im, _layer(ln, f, (255, 255, 255), 3), SAFE_CX, y0 + k * f.size * 1.2, **kw)

def acento(im, txt, x=None, y=None, color=LIL, size=56, rot=-6, **kw):
    """Acento manuscrito: Permanent Marker, UNA palabra encima del titular."""
    _put(im, _layer(txt, MARK(size), color, 2), SAFE_CX if x is None else x, (TIT_Y - 85) if y is None else y, rot=rot, **kw)

def etiqueta(im, txt, x=None, y=None, size=26, box=None, fg=(255, 255, 255), **kw):
    """Etiqueta tipo revista: Oswald Medium 32–40 px en 1080 (≈21–27 aquí), caja de color de marca."""
    f = OSW(size); t = txt.upper(); tw = f.getlength(t); box = Image.new("RGBA", (int(tw) + 28, int(size * 1.55)), (box or BRAND) + (255,))
    ImageDraw.Draw(box).text((box.width / 2, box.height / 2), t, font=f, fill=fg + (255,), anchor="mm")
    _put(im, box, SAFE_CX if x is None else x, (TIT_Y + 95) if y is None else y, shadow=False, **kw)

def guia_zona_segura(im):
    d = ImageDraw.Draw(im); d.rectangle(SAFE, outline=(60, 160, 255, 255), width=2)

if __name__ == "__main__":
    import render_smg as S
    out = Image.new("RGB", (W * 2 + 20, H), (255, 255, 255))
    # 1) escena blanca con cuadrícula (titular morado)
    a = S.bg("w", "KINGG"); titular(a, "KINGG SE VA", color=PUR); acento(a, "oficial"); etiqueta(a, "VCT 2027 · FICHAJES")
    subtitulo(a, "Leviatán confirma su salida después de 5 años")
    # 2) escena morada (titular blanco)
    b = Image.new("RGBA", (W, H), PUR + (255,)); titular(b, "KINGG SE VA"); acento(b, "oficial", color=LILL); etiqueta(b, "VCT 2027 · FICHAJES", box=(255, 255, 255), fg=PUR)
    subtitulo(b, "Leviatán confirma su salida después de 5 años")
    out.paste(a.convert("RGB"), (0, 0)); out.paste(b.convert("RGB"), (W + 20, 0))
    out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plantilla_texto_demo.jpg")); print("ok")
