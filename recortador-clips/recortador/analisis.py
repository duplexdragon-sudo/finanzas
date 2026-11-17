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
    a = medios.audio_mono(ruta, sr)
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


_det = {}
YUNET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'modelos', 'yunet.onnx')


def _caras(bgr):
    """cajas (x, y, w, h) de caras: YuNet (opencv_zoo, MIT) si está el modelo; si no, Haar de OpenCV 4"""
    h, w = bgr.shape[:2]
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


def analizar_video(ruta, fps=1 / PASO, killfeed=KILLFEED, progreso=None):
    inf = medios.info(ruta)
    total = max(1, int(inf['duracion'] * fps))
    corte, mov, kf, kf_area, cara_area, cara_x, cara_y = [], [], [], [], [], [], []
    prev_g = prev_hist = prev_roi = prev_filas = None
    for i, (t, bgr) in enumerate(medios.cuadros(ruta, fps=fps, ancho=480)):
        h, w = bgr.shape[:2]
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        g_peq = cv2.resize(g, (160, int(160 * h / w))).astype(np.float32)
        x0, y0, x1, y1 = int(killfeed[0] * w), int(killfeed[1] * h), int(killfeed[2] * w), int(killfeed[3] * h)
        roi = hsv[y0:y1, x0:x1]
        area, filas = _barras_killfeed(roi)
        roi_g = g[y0:y1, x0:x1].astype(np.float32)
        if prev_g is None:
            corte.append(0.0); mov.append(0.0); kf.append(0.0)
        else:
            corte.append(float(1 - cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)))
            m = float(np.abs(g_peq - prev_g).mean())
            mov.append(m)
            # filas que ahora son barra y antes no, o barras cuyo texto cambió (la lista se corrió = entrada nueva)
            texto = np.abs(roi_g - prev_roi).mean(1) > 18
            kf.append(float((filas & (~prev_filas | texto)).mean()))
        kf_area.append(area)
        prev_g, prev_hist, prev_roi, prev_filas = g_peq, hist, roi_g, filas
        # caras: la más grande
        cs = _caras(bgr)
        if len(cs):
            x, y, cw, ch = max(cs, key=lambda c: c[2] * c[3])
            cara_area.append(cw * ch / (w * h)); cara_x.append((x + cw / 2) / w); cara_y.append((y + ch / 2) / h)
        else:
            cara_area.append(0.0); cara_x.append(np.nan); cara_y.append(np.nan)
        if progreso and i % 20 == 0:
            progreso(min(1.0, i / total))
    r = {k: np.array(v, np.float32) for k, v in dict(corte=corte, movimiento=mov, kf_cambio=kf, kf_area=kf_area,
                                                       cara_area=cara_area, cara_x=cara_x, cara_y=cara_y).items()}
    r['kills'] = detectar_kills(r)
    return r


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
