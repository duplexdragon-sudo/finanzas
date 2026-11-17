"""PIPELINE — de un video largo a clips verticales:
analizar (audio + video) -> Gemini (opcional) -> elegir momentos -> subtítulos -> render 9:16 -> resumen.json
"""
import json
import os
import re
import time
import unicodedata

import numpy as np

from . import analisis, gemini, medios, momentos, transcribir, vertical

OPCIONES = dict(
    clips=8,                 # cuántos clips sacar por video
    dmin=15, dmax=45,        # duración de cada clip (s)
    formato='auto',          # auto | juego | completo | entrevista
    filtro='todo',           # todo | kills | graciosos | entrevistas
    gemini='auto',           # auto | si | no
    subtitulos='auto',       # auto | whisper | gemini | no
    idioma='español',        # idioma de los títulos
    marca='',                # tu @ abajo del video
    color='#FF4655',         # color de la palabra que se está diciendo (rojo Valorant)
    indicaciones='',         # texto libre para Gemini: "solo jugadas de TenZ", "prioriza risas"...
    killfeed=None,           # zona del killfeed "x0,y0,x1,y1" (0-1) si tu video no es la vista normal de Valorant
    calidad=20,              # CRF de x264 (menos = mejor, más pesado)
)


def _nombre(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^\w\s-]', '', texto.lower(), flags=re.UNICODE).strip()
    return re.sub(r'[\s_-]+', '_', s)[:40] or 'clip'


def _a_lista(x):
    if isinstance(x, np.ndarray):
        return [None if (isinstance(v, float) and np.isnan(v)) else round(float(v), 4) for v in x]
    return x


def procesar(video, carpeta, opciones=None, log=print, progreso=lambda f, txt='': None, cache=None):
    op = dict(OPCIONES, **{k: v for k, v in (opciones or {}).items() if v is not None})
    os.makedirs(carpeta, exist_ok=True)
    inf = medios.info(video)
    dur = inf['duracion']
    log(f"Video: {os.path.basename(video)} · {dur / 60:.1f} min · {inf['ancho']}x{inf['alto']} · {inf['fps']:.0f} fps")
    t_ini = time.time()

    kf = tuple(float(x) for x in op['killfeed'].split(',')) if op['killfeed'] else analisis.KILLFEED
    # 1) análisis clásico (con caché para volver a renderizar rápido)
    cache = cache or os.path.join(carpeta, 'analisis.npz')   # mismo video = no se vuelve a analizar
    if os.path.exists(cache):
        d = np.load(cache)
        a = {k[2:]: d[k] for k in d.files if k.startswith('a_')}
        v = {k[2:]: d[k] for k in d.files if k.startswith('v_')}
        log('Este video ya estaba analizado: me salto el análisis')
    else:
        progreso(0.02, 'Escuchando el audio (gritos, público, risas)...')
        a = analisis.analizar_audio(video) if inf['audio'] else dict(volumen=np.zeros(0), hype=np.zeros(0), brillo=np.zeros(0))
        progreso(0.08, 'Mirando el video (kills, cortes, caras)...')
        v = analisis.analizar_video(video, killfeed=kf, progreso=lambda f: progreso(0.08 + 0.37 * f, 'Mirando el video (kills, cortes, caras)...'))
        n = min(len(v['corte']), len(a['hype'])) if len(a['hype']) else len(v['corte'])
        if len(a['hype']) == 0:
            a = {k: np.zeros(n, np.float32) for k in ('volumen', 'hype', 'brillo')}
        np.savez_compressed(cache, **{'a_' + k: x for k, x in a.items()}, **{'v_' + k: x for k, x in v.items()})
    log(f"Kills detectadas en el killfeed: {int(v['kills'].sum())} · picos de hype: {int((a['hype'] > 2.3).sum())} muestras · "
        f"cortes de toma: {len(analisis.cortes(v))}")

    # 2) Gemini
    gem = []
    usar_gem = op['gemini'] == 'si' or (op['gemini'] == 'auto' and gemini.disponible())
    if usar_gem:
        progreso(0.47, 'Gemini está mirando el video...')
        try:
            proxy = os.path.join(carpeta, '_proxy360.mp4')
            if not os.path.exists(proxy):
                medios.proxy_ligero(video, proxy)
            gem = gemini.momentos(proxy, n=max(op['clips'] + 4, 10), dmin=op['dmin'], dmax=op['dmax'], idioma=op['idioma'],
                                  extra=op['indicaciones'], log=log)
            log(f'Gemini propuso {len(gem)} momentos')
            with open(os.path.join(carpeta, 'gemini.json'), 'w', encoding='utf-8') as f:
                json.dump(gem, f, ensure_ascii=False, indent=1)
        except Exception as e:
            log(f'Gemini no disponible ({e}); sigo solo con el análisis de audio/video')
    else:
        log('Sin Gemini: uso solo el análisis de audio y video')

    # 3) elegir
    progreso(0.6, 'Eligiendo los mejores momentos...')
    elegidos = momentos.elegir(v, a, dur, n=op['clips'], dmin=op['dmin'], dmax=op['dmax'], gem=gem, filtro=op['filtro'])
    if not elegidos:
        log('No encontré momentos claros. Prueba con Gemini activado o con el filtro "todo".')
    ts_cortes = analisis.cortes(v)

    # 4) render
    resultado = []
    for k, c in enumerate(elegidos):
        frac = 0.62 + 0.36 * k / max(1, len(elegidos))
        progreso(frac, f'Renderizando clip {k + 1} de {len(elegidos)}...')
        i0, i1 = int(c['inicio'] / analisis.PASO), int(c['fin'] / analisis.PASO) + 1
        entrevista = analisis.es_entrevista(v, i0, i1)
        fmt = op['formato'] if op['formato'] != 'auto' else ('entrevista' if entrevista else 'juego')
        pals = []
        if op['subtitulos'] != 'no':
            wav = os.path.join(carpeta, f'_clip{k}.wav')
            try:
                medios.recortar_audio(video, c['inicio'], c['fin'], wav)
                pals = transcribir.palabras(wav, op['subtitulos'], log=log)
                # en partidas, los subtítulos solo si hay voz clara (caster); en entrevistas siempre
                risas = transcribir.hay_risas(pals)
                if risas and c['tipo'] in ('entrevista', 'hype'):
                    c['tipo'] = 'gracioso'
                    c['puntuacion'] = min(10, c['puntuacion'] + 1)
            except Exception as e:
                log(f'Sin subtítulos para el clip {k + 1}: {e}')
            finally:
                if os.path.exists(wav):
                    os.remove(wav)
        nombre = f"{k + 1:02d}_{c['tipo']}_{_nombre(c['titulo'])}"
        salida = os.path.join(carpeta, nombre + '.mp4')
        try:
            con_kf = fmt == 'juego' and c['tipo'] in ('kill', 'multikill', 'ace', 'clutch')
            vertical.render(video, c['inicio'], c['fin'], salida, fmt, c['titulo'], pals, op['marca'], v, ts_cortes,
                            op['color'], calidad=op['calidad'], killfeed=kf if con_kf else None)
            vertical.portada(salida, c['pico'] - c['inicio'], os.path.join(carpeta, nombre + '.jpg'))
        except Exception as e:
            log(f'Error en el clip {k + 1}: {e}')
            continue
        texto = ' '.join(p['texto'] for p in pals)
        resultado.append(dict(c, archivo=nombre + '.mp4', portada=nombre + '.jpg', formato=fmt, duracion=round(c['fin'] - c['inicio'], 1),
                              transcripcion=texto))
        log(f"✔ {nombre}.mp4  [{c['inicio']:.0f}s-{c['fin']:.0f}s] {c['tipo']} · {c['puntuacion']}/10 · {fmt}")

    for p in ('_proxy360.mp4',):
        try:
            os.remove(os.path.join(carpeta, p))
        except OSError:
            pass
    resumen = dict(video=os.path.basename(video), duracion=dur, opciones=op, clips=resultado,
                   segundos=round(time.time() - t_ini, 1),
                   linea_tiempo=dict(paso=analisis.PASO, hype=_a_lista(a['hype']), kills=_a_lista(v['kills'])))
    with open(os.path.join(carpeta, 'resumen.json'), 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    progreso(1.0, f'Listo: {len(resultado)} clips')
    return resumen
