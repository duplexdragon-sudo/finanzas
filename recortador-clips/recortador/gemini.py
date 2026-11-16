"""GEMINI — la parte "que entiende" el video: Gemini mira el video (copia de 360p) y elige los momentos
(kills, ace, clutch, risas en entrevistas, reacciones, gritos del caster) con un título corto para cada clip.
También transcribe el audio de cada clip para los subtítulos cuando no hay Whisper.

Clave: variable de entorno GEMINI_API_KEY (gratis en https://aistudio.google.com/apikey).
Modelo: RECORTADOR_GEMINI_MODELO (si no, prueba gemini-3-flash-preview, gemini-flash-latest...).
"""
import base64
import json
import os
import re
import time

import requests

API = 'https://generativelanguage.googleapis.com'
# si un modelo está saturado (503) o ya no existe (404) se prueba el siguiente
MODELOS = [m for m in [os.environ.get('RECORTADOR_GEMINI_MODELO')] if m] + [
    'gemini-3-flash-preview', 'gemini-flash-latest', 'gemini-3.5-flash', 'gemini-2.5-flash']
_bueno = []


def _clave():
    return os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY') or ''


def disponible():
    """hay clave, o un proxy que la pone (como en el contenedor de Claude)"""
    if _clave():
        return True
    try:
        r = requests.get(f'{API}/v1beta/models', headers={'x-goog-api-key': 'x'}, timeout=15)
        return r.status_code == 200
    except Exception:
        return False


def _h(extra=None):
    h = {'x-goog-api-key': _clave() or 'x'}
    h.update(extra or {})
    return h


def subir(ruta, mime='video/mp4'):
    tam = os.path.getsize(ruta)
    r = requests.post(f'{API}/upload/v1beta/files', headers=_h({
        'X-Goog-Upload-Protocol': 'resumable', 'X-Goog-Upload-Command': 'start',
        'X-Goog-Upload-Header-Content-Length': str(tam), 'X-Goog-Upload-Header-Content-Type': mime,
        'Content-Type': 'application/json'}), json={'file': {'display_name': os.path.basename(ruta)}}, timeout=60)
    r.raise_for_status()
    url = r.headers.get('x-goog-upload-url') or r.headers.get('X-Goog-Upload-URL')
    with open(ruta, 'rb') as f:
        r = requests.post(url, headers=_h({'Content-Length': str(tam), 'X-Goog-Upload-Offset': '0',
                                           'X-Goog-Upload-Command': 'upload, finalize'}), data=f, timeout=1800)
    r.raise_for_status()
    archivo = r.json()['file']
    for _ in range(360):                                   # el video tarda en procesarse en Google
        if archivo.get('state') == 'ACTIVE':
            return archivo
        if archivo.get('state') == 'FAILED':
            raise RuntimeError('Gemini no pudo procesar el video')
        time.sleep(5)
        archivo = requests.get(f"{API}/v1beta/{archivo['name']}", headers=_h(), timeout=30).json()
    raise TimeoutError('Gemini tardó demasiado en procesar el video')


def borrar(archivo):
    try:
        requests.delete(f"{API}/v1beta/{archivo['name']}", headers=_h(), timeout=30)
    except Exception:
        pass


def _generar(partes, esquema, temperatura=0.4, resolucion_baja=False, espera=900):
    cfg = {'responseMimeType': 'application/json', 'responseSchema': esquema, 'temperature': temperatura}
    if resolucion_baja:
        cfg['mediaResolution'] = 'MEDIA_RESOLUTION_LOW'
    cuerpo = {'contents': [{'role': 'user', 'parts': partes}], 'generationConfig': cfg}
    ult = None
    orden = _bueno[:1] + [m for m in MODELOS if m not in _bueno[:1]]
    for ronda in range(2):
        for m in orden:
            try:
                r = requests.post(f'{API}/v1beta/models/{m}:generateContent', headers=_h({'Content-Type': 'application/json'}),
                                  json=cuerpo, timeout=espera)
            except requests.RequestException as e:
                ult = e
                continue
            if r.status_code == 200:
                try:
                    d = r.json()
                    txt = ''.join(p.get('text', '') for p in d['candidates'][0]['content']['parts'] if not p.get('thought'))
                    res = json.loads(txt)
                    _bueno[:] = [m]
                    return res
                except Exception as e:
                    ult = e
                    continue
            ult = RuntimeError(f'Gemini {m} {r.status_code}: {r.text[:200]}')
            if r.status_code in (400, 401, 403):
                raise ult
        time.sleep(10 * (ronda + 1))
    raise ult


def _seg(v):
    """'01:23' / '1:02:03' / '83.5' -> segundos"""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if re.fullmatch(r'[\d.]+', s):
        return float(s)
    partes = [float(p) for p in s.split(':')]
    t = 0.0
    for p in partes:
        t = t * 60 + p
    return t


PROMPT_MOMENTOS = """Eres editor de clips de e-sports de VALORANT para TikTok, Reels y YouTube Shorts (formato vertical).
Mira y escucha TODO el video y encuentra los mejores momentos para clips cortos y virales:
- kills espectaculares: multikill (3K, 4K), ACE (5 kills de un jugador), clutch (1vX que gana la ronda), flicks, tiros de Operator, wallbangs, kills con habilidad
- momentos graciosos: risas, bromas o caras raras en entrevistas, cámaras de jugadores o del público
- entrevistas: frases fuertes, confianza, trash talk, emoción
- reacciones: gritos del caster, público explotando, celebraciones de equipo
- cualquier otro momento con mucha energía o que haga que alguien quiera ver el clip completo
Reglas:
- Cada clip debe entenderse solo: empieza un poco antes de la acción (contexto) y termina justo después del remate o la reacción.
- Duración entre {dmin} y {dmax} segundos. Sin clips repetidos ni encimados.
- Tiempos en formato MM:SS (o H:MM:SS) EXACTOS según el video.
- titulo: gancho de 2 a 6 palabras en {idioma}, en mayúsculas, sin emojis (ej. "ACE CON SHERIFF", "SE RIÓ EN LA ENTREVISTA").
- puntuacion: 1-10, qué tan viral puede ser.
- Devuelve hasta {n} clips ordenados de mejor a peor.{extra}"""

ESQUEMA_MOMENTOS = {'type': 'ARRAY', 'items': {'type': 'OBJECT', 'properties': {
    'inicio': {'type': 'STRING'}, 'fin': {'type': 'STRING'},
    'tipo': {'type': 'STRING', 'enum': ['kill', 'multikill', 'ace', 'clutch', 'gracioso', 'entrevista', 'reaccion', 'hype', 'jugada']},
    'titulo': {'type': 'STRING'}, 'puntuacion': {'type': 'NUMBER'}, 'motivo': {'type': 'STRING'}},
    'required': ['inicio', 'fin', 'tipo', 'titulo', 'puntuacion']}}


def momentos(proxy, n=12, dmin=15, dmax=60, idioma='español', extra='', log=print):
    """sube la copia ligera del video y le pide a Gemini la lista de momentos"""
    log('Gemini: subiendo video...')
    arch = subir(proxy)
    try:
        log('Gemini: mirando el video y eligiendo momentos...')
        prompt = PROMPT_MOMENTOS.format(n=n, dmin=dmin, dmax=dmax, idioma=idioma,
                                        extra=('\nIndicaciones del usuario: ' + extra) if extra else '')
        res = _generar([{'file_data': {'mime_type': arch.get('mimeType', 'video/mp4'), 'file_uri': arch['uri']}},
                        {'text': prompt}], ESQUEMA_MOMENTOS, resolucion_baja=True)
    finally:
        borrar(arch)
    out = []
    for m in res or []:
        try:
            t0, t1 = _seg(m['inicio']), _seg(m['fin'])
        except Exception:
            continue
        if t1 > t0:
            out.append(dict(inicio=t0, fin=t1, tipo=m.get('tipo', 'jugada'), titulo=m.get('titulo', '').strip(),
                            puntuacion=float(m.get('puntuacion', 5)), motivo=m.get('motivo', ''), fuente='gemini'))
    return out


ESQUEMA_PALABRAS = {'type': 'ARRAY', 'items': {'type': 'OBJECT', 'properties': {
    'texto': {'type': 'STRING'}, 'inicio': {'type': 'NUMBER'}, 'fin': {'type': 'NUMBER'}},
    'required': ['texto', 'inicio', 'fin']}}


def transcribir(wav):
    """palabras con tiempos (segundos desde el inicio del audio) para subtítulos"""
    datos = base64.b64encode(open(wav, 'rb').read()).decode()
    prompt = ('Transcribe exactamente lo que se dice en este audio, en el idioma original (español, inglés, portugués...). '
              'Devuelve cada PALABRA con su tiempo de inicio y fin en segundos (con décimas) desde el inicio del audio. '
              'Marca risas como "[risas]". Si solo hay música o ruido devuelve una lista vacía.')
    res = _generar([{'inline_data': {'mime_type': 'audio/wav', 'data': datos}}, {'text': prompt}], ESQUEMA_PALABRAS, 0.1, espera=180)
    return [dict(texto=p['texto'].strip(), inicio=float(p['inicio']), fin=float(p['fin'])) for p in res or [] if p.get('texto', '').strip()]
