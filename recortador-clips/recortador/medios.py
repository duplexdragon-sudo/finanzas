"""MEDIOS — leer información, audio y cuadros de un video con ffmpeg (sin cargar todo en memoria)."""
import json
import os
import shutil
import subprocess

import numpy as np

FFMPEG = shutil.which('ffmpeg') or 'ffmpeg'
FFPROBE = shutil.which('ffprobe') or 'ffprobe'


def info(ruta):
    """duración, ancho, alto, fps y si tiene audio"""
    o = subprocess.run([FFPROBE, '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', ruta],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
    d = json.loads(o.stdout)
    v = next((s for s in d['streams'] if s.get('codec_type') == 'video'), None)
    if v is None:
        raise ValueError(f'{ruta} no tiene video')
    num, den = (v.get('avg_frame_rate') or v.get('r_frame_rate') or '30/1').split('/')
    fps = float(num) / float(den) if float(den) else 30.0
    w, h = int(v['width']), int(v['height'])
    rot = 0
    for sd in v.get('side_data_list', []) or []:
        if 'rotation' in sd:
            rot = int(sd['rotation'])
    if abs(rot) in (90, 270):
        w, h = h, w
    dur = float(d['format'].get('duration') or v.get('duration') or 0)
    audio = any(s.get('codec_type') == 'audio' for s in d['streams'])
    return dict(duracion=dur, ancho=w, alto=h, fps=fps if 1 < fps < 241 else 30.0, audio=audio)


def audio_mono(ruta, sr=16000):
    """audio completo como float32 mono (16 kHz: 1 h = 230 MB, suficiente para analizar)"""
    raw = subprocess.run([FFMPEG, '-v', 'error', '-i', ruta, '-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def cuadros(ruta, fps=2.0, ancho=480):
    """genera (t, cuadro_bgr) a 'fps' cuadros por segundo y 'ancho' píxeles, en un solo paso de ffmpeg"""
    inf = info(ruta)
    alto = int(round(inf['alto'] * ancho / inf['ancho'] / 2)) * 2
    p = subprocess.Popen([FFMPEG, '-v', 'error', '-i', ruta, '-an', '-vf', f'fps={fps},scale={ancho}:{alto}',
                          '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    tam = ancho * alto * 3
    i = 0
    try:
        while True:
            b = p.stdout.read(tam)
            if len(b) < tam:
                break
            yield i / fps, np.frombuffer(b, np.uint8).reshape(alto, ancho, 3)
            i += 1
    finally:
        p.stdout.close()
        p.wait()


def recortar_audio(ruta, t0, t1, salida, sr=16000):
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', ruta, '-vn', '-ac', '1',
                    '-ar', str(sr), salida], check=True)
    return salida


def proxy_ligero(ruta, salida, alto=360, fps=None):
    """copia chica del video (360p) para mandarla a Gemini rápido"""
    vf = f'scale=-2:{alto}' + (f',fps={fps}' if fps else '')
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', ruta, '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '30', '-c:a', 'aac', '-b:a', '64k', '-ac', '1', salida], check=True)
    return salida


def proxies_paralelo(ruta, carpeta, max_tramo=2700, hilos=4):
    """copias ligeras (360p, 1 cuadro/s) por tramos de máx. 45 min, en paralelo, para Gemini"""
    import concurrent.futures as cf
    import math
    inf = info(ruta)
    dur = inf['duracion']
    partes = max(1, math.ceil(dur / max_tramo))
    largo = dur / partes
    tramos = [(i * largo, min(dur, (i + 1) * largo), os.path.join(carpeta, f'_tramo{i:02d}.mp4')) for i in range(partes)]

    def uno(t):
        t0, t1, sal = t
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-threads', '2', '-skip_frame', 'noref', '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}',
                        '-i', ruta, '-vf', 'fps=1,scale=-2:360', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '32']
                       + (['-c:a', 'aac', '-b:a', '48k', '-ac', '1'] if inf['audio'] else ['-an']) + [sal], check=True)
    with cf.ThreadPoolExecutor(min(hilos, partes)) as ex:
        list(ex.map(uno, tramos))
    return tramos
