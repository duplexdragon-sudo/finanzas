"""PIPELINE — de un video largo a clips verticales:
analizar (audio + video) -> Gemini (opcional) -> elegir momentos -> subtítulos -> render 9:16 -> resumen.json
"""
import concurrent.futures as cf
import hashlib
import json
import math
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
    color='#B026FF',         # color de la palabra que se está diciendo (morado del Motor Morado)
    indicaciones='',         # texto libre para Gemini: "solo jugadas de TenZ", "prioriza risas"...
    killfeed=None,           # zona del killfeed "x0,y0,x1,y1" (0-1) si tu video no es la vista normal de Valorant
    calidad=20,              # CRF de x264 (menos = mejor, más pesado)
)


def _nombre(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^\w\s-]', '', texto.lower(), flags=re.UNICODE).strip()
    return re.sub(r'[\s_-]+', '_', s)[:40] or 'clip'


def analisis_mmss(t):
    t = int(t)
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}' if t >= 3600 else f'{t // 60}:{t % 60:02d}'


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
    # 1) análisis: una sola lectura del video, en tramos paralelos (con caché para volver a sacar clips rápido)
    cache = cache or os.path.join(carpeta, 'analisis.npz')   # mismo video = no se vuelve a analizar
    usar_gem = op['gemini'] == 'si' or (op['gemini'] == 'auto' and gemini.disponible())
    tramos = []
    if os.path.exists(cache):
        d = np.load(cache)
        a = {k[2:]: d[k] for k in d.files if k.startswith('a_')}
        v = {k[2:]: d[k] for k in d.files if k.startswith('v_')}
        log('Este video ya estaba analizado: me salto el análisis')
    else:
        txt = 'Analizando video y audio (kills, gritos, caras)' + (' + copia para Gemini' if usar_gem else '') + '...'
        progreso(0.02, txt)
        a, v, tramos = analisis.analizar_rapido(video, killfeed=kf, carpeta_proxy=carpeta if usar_gem else None,
                                                progreso=lambda f: progreso(0.02 + 0.5 * f, txt))
        np.savez_compressed(cache, **{'a_' + k: x for k, x in a.items()}, **{'v_' + k: x for k, x in v.items()})
        log(f'Análisis listo en {time.time() - t_ini:.0f} s ({len(tramos)} tramos en paralelo)')
    minutos = max(1.0, dur / 60)
    if v['kills'].sum() / minutos > 10:                    # imposible en Valorant: el overlay de esta transmisión no es el killfeed normal
        log(f"El killfeed no se pudo leer en este video ({int(v['kills'].sum())} 'kills' en {minutos:.0f} min = overlay distinto). "
            "Lo ignoro y uso el audio" + (' y Gemini' if usar_gem else '') + ". Si quieres, ajusta la 'Zona del killfeed'.")
        v = dict(v, kills=np.zeros_like(v['kills']))
    log(f"Kills detectadas en el killfeed: {int(v['kills'].sum())} · picos de hype: {int((a['hype'] > 2.3).sum())} muestras · "
        f"cortes de toma: {len(analisis.cortes(v))}")

    # 2) Gemini: cada tramo (máx. 45 min) se manda en paralelo; las respuestas se guardan para no volver a pedirlas
    gem = []
    if usar_gem:
        clave = hashlib.md5(json.dumps([op['clips'], op['dmin'], op['dmax'], op['idioma'], op['indicaciones']]).encode()).hexdigest()[:8]
        gcache = cache[:-4] + f'_gemini_{clave}.json'
        if os.path.exists(gcache):
            gem = json.load(open(gcache, encoding='utf-8'))
            log(f'Gemini ya había mirado este video: {len(gem)} momentos guardados')
        else:
            progreso(0.53, 'Gemini está mirando el video...')
            t_gem = time.time()
            if not tramos or not all(t[2] and os.path.exists(t[2]) for t in tramos):
                tramos = medios.proxies_paralelo(video, carpeta)
            n_tramo = max(4, math.ceil((op['clips'] + 4) * max(t1 - t0 for t0, t1, _ in tramos) / max(1, dur)) + 2)

            def mirar(t):
                t0, t1, prox = t
                ms = gemini.momentos(prox, n=n_tramo, dmin=op['dmin'], dmax=op['dmax'], idioma=op['idioma'],
                                     extra=op['indicaciones'], log=lambda m: None)
                return [dict(m, inicio=m['inicio'] + t0, fin=min(m['fin'], t1 - t0) + t0) for m in ms if m['inicio'] < t1 - t0]
            errores, listos = [], 0
            limite = time.time() + max(600, 120 * len(tramos))  # no esperar a Gemini para siempre
            ex = cf.ThreadPoolExecutor(min(2, len(tramos)))       # de 2 en 2: el plan gratis tiene límite por minuto
            futuros = {ex.submit(mirar, t): t for t in tramos}
            try:
                for fut in cf.as_completed(futuros, timeout=max(1, limite - time.time())):
                    t0, t1, _ = futuros[fut]
                    listos += 1
                    try:
                        ms = fut.result()
                        gem += ms
                        log(f'Gemini tramo {analisis_mmss(t0)}–{analisis_mmss(t1)}: {len(ms)} momentos ({listos}/{len(tramos)})')
                    except Exception as e:
                        errores.append(str(e))
                        log(f'Gemini tramo {analisis_mmss(t0)}–{analisis_mmss(t1)} falló: {str(e)[:160]}')
                    progreso(0.53 + 0.07 * listos / len(tramos), f'Gemini está mirando el video ({listos} de {len(tramos)} partes)...')
            except cf.TimeoutError:
                errores.append('tiempo agotado')
                log(f'Gemini tardó demasiado: sigo con {listos} de {len(tramos)} partes y el análisis de audio/video')
            finally:
                ex.shutdown(wait=False, cancel_futures=True)
            log(f'Gemini propuso {len(gem)} momentos en {time.time() - t_gem:.0f} s')
            if gem and not errores:
                with open(gcache, 'w', encoding='utf-8') as f:
                    json.dump(gem, f, ensure_ascii=False, indent=1)
    else:
        log('Sin Gemini: uso solo el análisis de audio y video')
    for t in tramos:
        try:
            if t[2] and os.path.exists(t[2]):
                os.remove(t[2])
        except OSError:                                      # Windows: todavía se está subiendo
            pass

    # 3) elegir
    progreso(0.6, 'Eligiendo los mejores momentos...')
    elegidos = momentos.elegir(v, a, dur, n=op['clips'], dmin=op['dmin'], dmax=op['dmax'], gem=gem, filtro=op['filtro'])
    if not elegidos:
        log('No encontré momentos claros. Prueba con Gemini activado o con el filtro "todo".')
    ts_cortes = analisis.cortes(v)

    # 4) subtítulos (uno por uno: Whisper usa todos los núcleos) y render (varios clips a la vez)
    trabajos = []
    for c in elegidos:
        i0, i1 = int(c['inicio'] / analisis.PASO), int(c['fin'] / analisis.PASO) + 1
        entrevista = analisis.es_entrevista(v, i0, i1)
        trabajos.append([len(trabajos), c, op['formato'] if op['formato'] != 'auto' else ('entrevista' if entrevista else 'juego'), []])

    def subtitular(tr):
        k, c = tr[0], tr[1]
        wav = os.path.join(carpeta, f'_clip{k}.wav')
        try:
            medios.recortar_audio(video, c['inicio'], c['fin'], wav)
            tr[3] = transcribir.palabras(wav, op['subtitulos'], log=log)
            if transcribir.hay_risas(tr[3]) and c['tipo'] in ('entrevista', 'hype'):
                c['tipo'] = 'gracioso'
                c['puntuacion'] = min(10, c['puntuacion'] + 1)
        except Exception as e:
            log(f'Sin subtítulos para el clip {k + 1}: {e}')
        finally:
            if os.path.exists(wav):
                os.remove(wav)
    if op['subtitulos'] != 'no' and trabajos:
        progreso(0.62, f'Escribiendo subtítulos de {len(trabajos)} clips...')
        t_sub = time.time()
        # Whisper ya usa todos los núcleos (uno por uno); Gemini se puede pedir de 4 en 4
        en_paralelo = 1 if transcribir.usa_whisper(op['subtitulos']) else 4
        with cf.ThreadPoolExecutor(en_paralelo) as ex:
            list(ex.map(subtitular, trabajos))
        log(f'Subtítulos listos en {time.time() - t_sub:.0f} s')

    hechos = [0]
    progreso(0.72, f'Creando {len(trabajos)} clips verticales...')

    def renderizar(tr):
        k, c, fmt, pals = tr
        nombre = f"{k + 1:02d}_{c['tipo']}_{_nombre(c['titulo'])}"
        salida = os.path.join(carpeta, nombre + '.mp4')
        con_kf = fmt == 'juego' and c['tipo'] in ('kill', 'multikill', 'ace', 'clutch')
        vertical.render(video, c['inicio'], c['fin'], salida, fmt, c['titulo'], pals, op['marca'], v, ts_cortes,
                        op['color'], calidad=op['calidad'], killfeed=kf if con_kf else None)
        vertical.portada(salida, c['pico'] - c['inicio'], os.path.join(carpeta, nombre + '.jpg'))
        hechos[0] += 1
        progreso(0.72 + 0.27 * hechos[0] / max(1, len(trabajos)), f'Clip {hechos[0]} de {len(trabajos)} listo...')
        return dict(c, archivo=nombre + '.mp4', portada=nombre + '.jpg', formato=fmt, duracion=round(c['fin'] - c['inicio'], 1),
                    transcripcion=' '.join(p['texto'] for p in pals))

    resultado = []
    t_ren = time.time()
    log(f'Creando clips con: {vertical.tarjeta()} ({vertical.clips_a_la_vez()} a la vez)')
    with cf.ThreadPoolExecutor(vertical.clips_a_la_vez()) as ex:
        futuros = [(tr, ex.submit(renderizar, tr)) for tr in trabajos]
        for tr, fut in futuros:
            try:
                r = fut.result()
                resultado.append(r)
                log(f"✔ {r['archivo']}  [{r['inicio']:.0f}s-{r['fin']:.0f}s] {r['tipo']} · {r['puntuacion']}/10 · {r['formato']}")
            except Exception as e:
                log(f'Error en el clip {tr[0] + 1}: {e}')
    log(f'Clips creados en {time.time() - t_ren:.0f} s · todo listo en {time.time() - t_ini:.0f} s')

    resumen = dict(video=os.path.basename(video), duracion=dur, opciones=op, clips=resultado,
                   segundos=round(time.time() - t_ini, 1),
                   linea_tiempo=dict(paso=analisis.PASO, hype=_a_lista(a['hype']), kills=_a_lista(v['kills'])))
    with open(os.path.join(carpeta, 'resumen.json'), 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    progreso(1.0, f'Listo: {len(resultado)} clips')
    return resumen
