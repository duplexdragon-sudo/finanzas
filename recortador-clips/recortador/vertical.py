"""VERTICAL — renderiza un clip 1080x1920 listo para TikTok / Reels / Shorts.

Formatos:
  juego       partida 16:9: centro del juego recortado 4:5 grande + fondo desenfocado, título arriba, subtítulos abajo
  completo    el cuadro 16:9 entero (se ve el killfeed y el minimapa) sobre fondo desenfocado
  entrevista  recorte 9:16 que sigue la cara (cambia de persona en cada corte de toma)
  auto        entrevista si hay cara grande, juego si no
Audio normalizado a -14 LUFS (lo que piden TikTok/YouTube).
"""
import os
import subprocess

import numpy as np

from . import medios
from .analisis import PASO

W, H = 1080, 1920
FUENTES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fuentes')


def _color_ass(hexrgb):
    h = (hexrgb or '#FF4655').lstrip('#')
    if len(h) != 6:
        h = 'FF4655'
    return f'&H{h[4:6]}{h[2:4]}{h[0:2]}'.upper()


def _esc(t):
    return t.replace('\\', '').replace('{', '(').replace('}', ')').replace('\n', ' ')


def _hms(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def grupos_de_palabras(pals, maximo=3, pausa=0.6):
    gs = []
    for p in pals:
        if gs and len(gs[-1]) < maximo and p['inicio'] - gs[-1][-1]['fin'] < pausa \
                and not gs[-1][-1]['texto'].endswith(('.', '?', '!')):
            gs[-1].append(p)
        else:
            gs.append([p])
    return gs


def escribir_ass(ruta, dur, titulo='', pals=(), marca='', color='#FF4655', y_sub=420, y_titulo=150):
    est = ('Style: Titulo,Anton,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,7,2,8,60,60,{yt},1\n'
           'Style: Sub,Anton,108,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,1,0,1,8,3,2,70,70,{ys},1\n'
           'Style: Marca,Bebas Neue,54,&H40FFFFFF,&H40FFFFFF,&H78000000,&H00000000,0,0,0,0,100,100,3,0,1,3,0,2,40,40,70,1\n'
           ).format(yt=y_titulo, ys=y_sub)
    lin = []
    if titulo:
        lin.append(f'Dialogue: 1,{_hms(0)},{_hms(dur)},Titulo,,0,0,0,,'
                   r'{\fad(120,0)\fscx115\fscy115\t(0,180,\fscx100\fscy100)}' + _esc(titulo.upper()))
    if marca:
        lin.append(f'Dialogue: 0,{_hms(0)},{_hms(dur)},Marca,,0,0,0,,{_esc(marca)}')
    acento = _color_ass(color)
    for g in grupos_de_palabras(list(pals)):
        fin_g = g[-1]['fin'] + 0.25
        for k, p in enumerate(g):
            t0 = p['inicio']
            t1 = g[k + 1]['inicio'] if k + 1 < len(g) else fin_g
            if t1 <= t0:
                continue
            partes = []
            for j, q in enumerate(g):
                txt = _esc(q['texto'].upper())
                partes.append(r'{\c' + acento + '&}' + txt + r'{\c&H00FFFFFF&}' if j == k else txt)
            pop = r'{\fscx112\fscy112\t(0,90,\fscx100\fscy100)}' if k == 0 else ''
            lin.append(f'Dialogue: 2,{_hms(t0)},{_hms(min(t1, dur))},Sub,,0,0,0,,{pop}' + ' '.join(partes))
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n'
                '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
                'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, '
                'MarginL, MarginR, MarginV, Encoding\n' + est +
                '\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(lin) + '\n')
    return ruta


def _ruta_filtro(p):
    p = os.path.abspath(p).replace('\\', '/')
    return p.replace(':', r'\:').replace("'", r"\'")


def seguir_cara(v, t0, t1, ancho_src, alto_src, ts_cortes):
    """expresión de ffmpeg para la x del recorte 9:16: quieta en cada toma, centrada en la cara"""
    cw = int(alto_src * 9 / 16) // 2 * 2
    if cw >= ancho_src:
        return '0', ancho_src
    i0, i1 = int(t0 / PASO), int(t1 / PASO) + 1
    xs = np.array(v['cara_x'][i0:i1], dtype=np.float64) if len(v.get('cara_x', [])) else np.array([])
    limites = [0.0] + [c - t0 for c in ts_cortes if t0 + 0.5 < c < t1 - 0.5] + [t1 - t0]
    tramos = []
    for a, b in zip(limites[:-1], limites[1:]):
        seg = xs[int(a / PASO):int(b / PASO) + 1] if len(xs) else np.array([])
        seg = seg[~np.isnan(seg)] if len(seg) else seg
        cx = float(np.median(seg)) if len(seg) >= 2 else (tramos[-1][1] if tramos else 0.5)
        tramos.append((b, cx))
    def px(cx):
        return int(min(max(cx * ancho_src - cw / 2, 0), ancho_src - cw))
    expr = str(px(tramos[-1][1]))
    for b, cx in reversed(tramos[:-1]):
        expr = f'if(lt(t\\,{b:.2f})\\,{px(cx)}\\,{expr})'
    return expr, cw


def render(src, t0, t1, salida, formato='juego', titulo='', pals=(), marca='', v=None, ts_cortes=(), color='#FF4655',
           fps_max=60, calidad=20, killfeed=None):
    inf = medios.info(src)
    dur = t1 - t0
    sw, sh = inf['ancho'], inf['alto']
    fps = min(fps_max, round(inf['fps']))
    base = os.path.splitext(salida)[0]
    if formato == 'entrevista':
        xexpr, cw = seguir_cara(v or {}, t0, t1, sw, sh, ts_cortes)
        vid = f"[0:v]crop={cw}:{sh // 2 * 2}:'{xexpr}':0,scale={W}:{H}:flags=lanczos,setsar=1[v0]"
        y_sub, y_tit = 380, 160
    else:
        if formato == 'completo':
            fg = f'[f]scale={W}:-2:flags=lanczos[fg]'
            y_sub, y_tit = 430, 260
        else:                                               # juego: centro 4:5 grande
            fg = f"[f]crop='min(iw\\,ih*4/5)':ih:'(iw-min(iw\\,ih*4/5))/2':0,scale={W}:-2:flags=lanczos[fg]"
            y_sub, y_tit = 330, 110
        n = 3 if killfeed else 2
        vid = (f'[0:v]split={n}[b][f]' + ('[k]' if killfeed else '') + ';'
               f'[b]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},'
               f'gblur=sigma=28,eq=brightness=-0.12:saturation=1.1[bg];{fg};'
               f'[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1' + ('[v1]' if killfeed else '[v0]'))
        if killfeed:                                        # el killfeed en un recuadro arriba a la derecha
            x0, y0, x1, y1 = killfeed
            kw, kh = int((x1 - x0) * sw) // 2 * 2, int((y1 - y0) * sh) // 2 * 2
            vid += (f';[k]crop={kw}:{kh}:{int(x0 * sw)}:{int(y0 * sh)},scale=400:-2:flags=lanczos[kf]'
                    f';[v1][kf]overlay=W-w-24:{(H - 1350) // 2 + 24}[v0]')
    ass = escribir_ass(base + '.ass', dur, titulo, pals, marca, color, y_sub, y_tit)
    vid += f";[v0]ass='{_ruta_filtro(ass)}':fontsdir='{_ruta_filtro(FUENTES)}',fps={fps},format=yuv420p[v]"
    filtro = vid
    mapa = ['-map', '[v]']
    if inf['audio']:
        filtro += ';[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]'
        mapa += ['-map', '[a]']
    script = base + '.filtro.txt'
    with open(script, 'w', encoding='utf-8') as f:
        f.write(filtro)
    cmd = [medios.FFMPEG, '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', src,
           '-filter_complex_script', script, *mapa, '-c:v', 'libx264', '-preset', 'fast', '-crf', str(calidad),
           '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', salida]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError('ffmpeg falló: ' + r.stderr[-800:])
    for p in (script, ass):
        try:
            os.remove(p)
        except OSError:
            pass
    return salida


def portada(clip, t, salida):
    subprocess.run([medios.FFMPEG, '-v', 'error', '-y', '-ss', f'{max(0, t):.2f}', '-i', clip, '-frames:v', '1',
                    '-q:v', '3', salida], check=True)
    return salida
