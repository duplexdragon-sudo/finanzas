"""ANALISIS — mide el video entero en una línea de tiempo de 0.5 s:

  audio   hype       gritos del caster / público: volumen y brillo por encima de lo normal en ese tramo del video
  video   corte      cambio de toma (para empezar y terminar los clips en un corte limpio)
          movimiento cuánto se mueve la imagen
          killfeed   entradas nuevas en el killfeed de Valorant (arriba a la derecha) = kills
          cara       cara grande en cuadro (entrevistas, cámaras de jugadores) + su posición para el recorte vertical

Todo es clásico (numpy + OpenCV), corre en CPU sin descargar modelos. Gemini (gemini.py) es la capa "inteligente" opcional.
"""
import os

import numpy as np
import cv2

from . import medios

PASO = 0.5                       # segundos por muestra
# zona del killfeed en un video 16:9 de Valorant (proporción del cuadro: x0, y0, x1, y1). Se cambia con --killfeed
KILLFEED = (0.70, 0.06, 0.995, 0.34)


def _mediana_movil(x, w):
    if len(x) == 0:
        return x
    w = max(3, int(w) | 1)
    p = np.pad(x, (w // 2, w // 2), mode='reflect' if len(x) > w // 2 else 'edge')
    v = np.lib.stride_tricks.sliding_window_view(p, w)
    return np.median(v, axis=1)


def _suave(x, n):
    n = max(1, int(n))
    return np.convolve(x, np.ones(n) / n, mode='same') if len(x) else x


def zscore_local(x, ventana_seg=90):
    """qué tan por encima está cada punto de lo normal en su tramo (mediana y MAD móviles)"""
    w = int(ventana_seg / PASO)
    base = _mediana_movil(x, w)
    mad = _mediana_movil(np.abs(x - base), w) * 1.4826
    if len(x) == 0:
        return x
    piso = max(float(np.percentile(mad, 20)), 1e-6)
    return (x - base) / np.maximum(mad, piso)


def analizar_audio(ruta, sr=16000):
    return audio_desde_arreglo(medios.audio_mono(ruta, sr), sr)


def audio_desde_arreglo(a, sr=16000):
    n = int(PASO * sr)
    k = len(a) // n
    if k == 0:
        return dict(volumen=np.zeros(0), hype=np.zeros(0), brillo=np.zeros(0))
    v = a[:k * n].reshape(k, n)
    rms = np.sqrt((v ** 2).mean(1) + 1e-10)
    db = 20 * np.log10(rms + 1e-7)
    # brillo: proporción de energía arriba de 1.5 kHz (gritos, público, "OHHH" del caster)
    f = np.fft.rfftfreq(n, 1 / sr)
    m_alto, m_total = (f > 1500) & (f < 6000), (f > 80) & (f < 6000)
    ventana = np.hanning(n).astype(np.float32)
    alto, total = np.zeros(k), np.zeros(k)
    for i in range(0, k, 600):                              # por bloques de 5 min: videos de horas sin llenar la RAM
        esp = np.abs(np.fft.rfft(v[i:i + 600] * ventana, axis=1)) ** 2
        alto[i:i + 600] = esp[:, m_alto].sum(1)
        total[i:i + 600] = esp[:, m_total].sum(1)
    total += 1e-9
    brillo = alto / total
    silencio = db < -50
    z_vol = zscore_local(db)
    z_bri = zscore_local(brillo)
    hype = _suave(0.7 * np.clip(z_vol, -3, 6) + 0.3 * np.clip(z_bri, -3, 6), 3)
    hype[silencio] = np.minimum(hype[silencio], 0)
    return dict(volumen=db, hype=hype, brillo=brillo)


import threading
_hilo = threading.local()
YUNET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'modelos', 'yunet.onnx')


def _caras(bgr):
    """cajas (x, y, w, h) de caras: YuNet (opencv_zoo, MIT) si está el modelo; si no, Haar de OpenCV 4"""
    h, w = bgr.shape[:2]
    if not hasattr(_hilo, 'det'):
        _hilo.det = {}
    _det = _hilo.det
    if 'yn' not in _det:
        _det['yn'] = None
        if os.path.exists(YUNET) and hasattr(cv2, 'FaceDetectorYN'):
            try:
                _det['yn'] = cv2.FaceDetectorYN.create(YUNET, '', (w, h), 0.75, 0.3, 50)
            except Exception:
                pass
        if _det['yn'] is None and hasattr(cv2, 'CascadeClassifier'):
            _det['haar'] = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if _det['yn'] is not None:
        _det['yn'].setInputSize((w, h))
        _, caras = _det['yn'].detect(bgr)
        return [tuple(int(v) for v in c[:4]) for c in (caras if caras is not None else [])]
    if _det.get('haar') is not None:
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        return _det['haar'].detectMultiScale(g, 1.15, 5, minSize=(max(20, h // 14), max(20, h // 14)))
    return []


def _barras_killfeed(roi_hsv):
    """píxeles con color de fondo de una entrada del killfeed (verde/turquesa o rojo, saturado y claro)"""
    hh, s, v = roi_hsv[..., 0], roi_hsv[..., 1], roi_hsv[..., 2]
    color = (s > 110) & (v > 110) & (((hh >= 70) & (hh <= 100)) | (hh <= 8) | (hh >= 170))
    # una entrada es una franja horizontal: contamos filas donde una buena parte es color de barra
    filas = color.mean(1) > 0.10                            # en el killfeed real a veces solo los íconos llevan color
    return float(filas.mean()), filas


class _Medidor:
    """mide cuadro por cuadro (cortes, movimiento, killfeed, caras)"""
    def __init__(self, killfeed):
        self.kfz = killfeed
        self.r = {k: [] for k in ('corte', 'movimiento', 'kf_cambio', 'kf_area', 'cara_area', 'cara_x', 'cara_y')}
        self.prev = None
        self.i = 0

    def cuadro(self, bgr):
        r, kfz = self.r, self.kfz
        h, w = bgr.shape[:2]
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        g_peq = cv2.resize(g, (160, int(160 * h / w))).astype(np.float32)
        x0, y0, x1, y1 = int(kfz[0] * w), int(kfz[1] * h), int(kfz[2] * w), int(kfz[3] * h)
        area, filas = _barras_killfeed(hsv[y0:y1, x0:x1])
        roi_g = g[y0:y1, x0:x1].astype(np.float32)
        if self.prev is None:
            r['corte'].append(0.0); r['movimiento'].append(0.0); r['kf_cambio'].append(0.0)
        else:
            pg, ph, pr, pf = self.prev
            r['corte'].append(float(1 - cv2.compareHist(ph, hist, cv2.HISTCMP_CORREL)))
            r['movimiento'].append(float(np.abs(g_peq - pg).mean()))
            # filas que ahora son barra y antes no, o barras cuyo texto cambió (la lista se corrió = entrada nueva)
            texto = np.abs(roi_g - pr).mean(1) > 18
            r['kf_cambio'].append(float((filas & (~pf | texto)).mean()))
        r['kf_area'].append(area)
        self.prev = (g_peq, hist, roi_g, filas)
        # caras: una vez por segundo (es lo más caro); la muestra de en medio repite la anterior
        if self.i % 2 == 0 or not r['cara_area']:
            cs = _caras(bgr)
            if len(cs):
                x, y, cw, ch = max(cs, key=lambda c: c[2] * c[3])
                cara = (cw * ch / (w * h), (x + cw / 2) / w, (y + ch / 2) / h)
            else:
                cara = (0.0, np.nan, np.nan)
        else:
            cara = (r['cara_area'][-1], r['cara_x'][-1], r['cara_y'][-1])
        r['cara_area'].append(cara[0]); r['cara_x'].append(cara[1]); r['cara_y'].append(cara[2])
        self.i += 1

    def resultado(self, n=None):
        out = {}
        for k, v in self.r.items():
            a = np.array(v, np.float32)
            if n is not None:                                  # largo exacto del tramo
                a = a[:n] if len(a) >= n else np.concatenate([a, np.full(n - len(a), np.nan if k in ('cara_x', 'cara_y') else 0, np.float32)])
            out[k] = a
        return out


def analizar_video(ruta, fps=1 / PASO, killfeed=KILLFEED, progreso=None):
    """versión simple (un solo proceso); el pipeline usa analizar_rapido"""
    inf = medios.info(ruta)
    total = max(1, int(inf['duracion'] * fps))
    m = _Medidor(killfeed)
    for i, (t, bgr) in enumerate(medios.cuadros(ruta, fps=fps, ancho=480)):
        m.cuadro(bgr)
        if progreso and i % 20 == 0:
            progreso(min(1.0, i / total))
    r = m.resultado()
    r['kills'] = detectar_kills(r)
    return r


def _tramo(ruta, t0, t1, alto_ana, ancho_ana, killfeed, proxy, audio, avance):
    """UN solo paso de ffmpeg por tramo: cuadros para analizar + audio + copia ligera para Gemini"""
    dur = t1 - t0
    vf = f'fps={1 / PASO:g},scale={ancho_ana}:{alto_ana}:flags=fast_bilinear'
    if proxy:
        vf += ',split[a][q];[q]fps=1,scale=-2:360[p]'
    cmd = [medios.FFMPEG, '-v', 'error', '-y', '-threads', '2', '-skip_frame', 'noref', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}',
           '-i', ruta, '-filter_complex', f'[0:v]{vf}' + ('' if proxy else '[a]'),
           '-map', '[a]', '-f', 'rawvideo', '-pix_fmt', 'bgr24', 'pipe:1']
    if audio:
        cmd += ['-map', '0:a:0', '-ac', '1', '-ar', '16000', '-f', 'f32le', audio]
    if proxy:
        cmd += ['-map', '[p]'] + (['-map', '0:a:0', '-c:a', 'aac', '-b:a', '48k', '-ac', '1'] if audio else []) + \
               ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '32', proxy]
    p = medios.subprocess.Popen(cmd, stdout=medios.subprocess.PIPE, stderr=medios.subprocess.DEVNULL)
    m = _Medidor(killfeed)
    tam = ancho_ana * alto_ana * 3
    try:
        while True:
            b = p.stdout.read(tam)
            if len(b) < tam:
                break
            m.cuadro(np.frombuffer(b, np.uint8).reshape(alto_ana, ancho_ana, 3))
            if m.i % 40 == 0:
                avance(40)
    finally:
        p.stdout.close()
        p.wait()
    return m.resultado(int(round(dur / PASO)))


def analizar_rapido(ruta, killfeed=KILLFEED, carpeta_proxy=None, progreso=None, hilos=None, max_tramo=2700):
    """analiza el video en tramos paralelos (todos los núcleos) leyéndolo una sola vez.
    Devuelve (audio, video, tramos) donde tramos = [(t0, t1, ruta_proxy)] para Gemini."""
    import concurrent.futures as cf
    import math
    import tempfile
    inf = medios.info(ruta)
    dur = inf['duracion']
    nucleos = os.cpu_count() or 4
    hilos = hilos or max(1, min(6, nucleos // 2))
    partes = max(hilos if dur > 240 else 1, math.ceil(dur / max_tramo))
    largo = math.ceil(dur / partes / PASO) * PASO                 # tramos alineados a la muestra de 0.5 s
    tramos = [(i * largo, min(dur, (i + 1) * largo)) for i in range(partes) if i * largo < dur]
    ancho = 480
    alto = int(round(inf['alto'] * ancho / inf['ancho'] / 2)) * 2
    tmp = tempfile.mkdtemp(prefix='recortador_')
    total = max(1, int(dur / PASO))
    hecho = [0]
    candado = threading.Lock()

    def avance(n):
        with candado:
            hecho[0] += n
            if progreso:
                progreso(min(1.0, hecho[0] / total))

    def uno(k):
        t0, t1 = tramos[k]
        prox = os.path.join(carpeta_proxy, f'_tramo{k:02d}.mp4') if carpeta_proxy else None
        aud = os.path.join(tmp, f'a{k}.f32') if inf['audio'] else None
        return _tramo(ruta, t0, t1, alto, ancho, killfeed, prox, aud, avance), aud, prox

    with cf.ThreadPoolExecutor(hilos) as ex:
        res = list(ex.map(uno, range(len(tramos))))
    v = {k: np.concatenate([r[0][k] for r in res]) for k in res[0][0]}
    v['kills'] = detectar_kills(v)
    if inf['audio']:
        n16 = int(PASO * 16000)
        trozos = []
        for (t0, t1), (_, aud, _) in zip(tramos, res):
            x = np.fromfile(aud, np.float32) if os.path.exists(aud) else np.zeros(0, np.float32)
            quiere = int(round((t1 - t0) / PASO)) * n16
            trozos.append(x[:quiere] if len(x) >= quiere else np.concatenate([x, np.zeros(quiere - len(x), np.float32)]))
        a = audio_desde_arreglo(np.concatenate(trozos))
    else:
        a = {k: np.zeros(len(v['corte']), np.float32) for k in ('volumen', 'hype', 'brillo')}
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    n = min(len(a['hype']), len(v['corte']))
    a = {k: x[:n] for k, x in a.items()}
    v = {k: x[:n] for k, x in v.items()}
    return a, v, [(t0, t1, r[2]) for (t0, t1), r in zip(tramos, res)]


def detectar_kills(r):
    """una kill = entra una barra nueva al killfeed (filas de color de barra que aparecen, o barras que cambian de
    texto porque la lista se corrió), sin que sea un cambio de toma (en un corte cambia todo el cuadro)"""
    nuevo, corte = r['kf_cambio'], r['corte']
    out = np.zeros(len(nuevo), np.float32)
    ult = -99
    for i in np.flatnonzero((nuevo > 0.07) & (corte < 0.35)):
        if i - ult >= 2:                                    # la barra entra en ~0.3 s: no contarla dos veces
            out[i] = 1.0
            ult = i
    return out


def cortes(r, umbral=0.45):
    """tiempos de cambio de toma"""
    return [i * PASO for i in np.flatnonzero(r['corte'] > umbral)]


def es_entrevista(r, i0, i1):
    """tramo con cara grande casi todo el tiempo, poco movimiento y sin kills = entrevista / cámara de jugador"""
    a = r['cara_area'][i0:i1]
    if len(a) == 0:
        return False
    return (a > 0.012).mean() > 0.45 and r['kills'][i0:i1].sum() == 0 and np.median(r['movimiento'][i0:i1]) < 12
