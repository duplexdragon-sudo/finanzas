#!/usr/bin/env python3
"""RECORTAR — línea de comandos (sin la app web).

    python recortar.py partido.mp4                       -> carpeta clips/partido/ con los clips 9:16
    python recortar.py entrevista.mp4 --filtro graciosos --clips 5
    python recortar.py partido.mp4 --formato completo --marca @tu_canal --sin-gemini
"""
import argparse
import os
import sys

from recortador import pipeline


def main():
    ap = argparse.ArgumentParser(description='Recorta los mejores momentos de un video de Valorant/e-sports en clips verticales')
    ap.add_argument('videos', nargs='+')
    ap.add_argument('--salida', default='clips', help='carpeta de salida (default: clips/)')
    ap.add_argument('--clips', type=int, default=8)
    ap.add_argument('--dmin', type=float, default=15)
    ap.add_argument('--dmax', type=float, default=45)
    ap.add_argument('--formato', choices=['auto', 'juego', 'completo', 'entrevista'], default='auto')
    ap.add_argument('--filtro', choices=['todo', 'kills', 'graciosos', 'entrevistas'], default='todo')
    ap.add_argument('--subtitulos', choices=['auto', 'whisper', 'gemini', 'no'], default='auto')
    ap.add_argument('--sin-gemini', action='store_true')
    ap.add_argument('--marca', default='', help='tu @ abajo del video')
    ap.add_argument('--color', default='#FF4655')
    ap.add_argument('--indicaciones', default='', help='texto libre para Gemini')
    ap.add_argument('--killfeed', default=None, help='zona del killfeed x0,y0,x1,y1 en 0-1')
    a = ap.parse_args()
    for v in a.videos:
        base = os.path.splitext(os.path.basename(v))[0]
        carpeta = os.path.join(a.salida, base)
        def prog(f, txt=''):
            sys.stdout.write(f'\r[{int(f * 100):3d}%] {txt:60s}'); sys.stdout.flush()
            if f >= 1: print()
        def log(m):
            print('\n' + m)
        pipeline.procesar(v, carpeta, dict(clips=a.clips, dmin=a.dmin, dmax=a.dmax, formato=a.formato, filtro=a.filtro,
                                           subtitulos=a.subtitulos, gemini='no' if a.sin_gemini else 'auto', marca=a.marca,
                                           color=a.color, indicaciones=a.indicaciones, killfeed=a.killfeed), log, prog)
        print(f'Clips en: {os.path.abspath(carpeta)}')


if __name__ == '__main__':
    main()
