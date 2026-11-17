#!/usr/bin/env python3
"""RECORTADOR DE CLIPS — app web local. Subes tus videos de Valorant / e-sports y te devuelve los clips verticales.

    python app.py            -> abre http://localhost:5000 en el navegador
    python app.py --puerto 8080 --red    (--red: también desde el celular en la misma Wi-Fi)
"""
import argparse
import io
import json
import os
import queue
import re
import threading
import time
import traceback
import uuid
import webbrowser
import zipfile

from flask import Flask, abort, jsonify, request, send_file, send_from_directory

from recortador import gemini, pipeline, transcribir

RAIZ = os.path.dirname(os.path.abspath(__file__))
TRABAJOS = os.path.join(RAIZ, 'trabajos')
CACHE = os.path.join(TRABAJOS, '_cache')          # análisis guardados: el mismo video no se analiza dos veces
os.makedirs(CACHE, exist_ok=True)

app = Flask(__name__, static_folder=os.path.join(RAIZ, 'web'), static_url_path='/web')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 ** 3          # hasta 20 GB por subida
cola = queue.Queue()
estados = {}
candado = threading.Lock()
EXT = ('.mp4', '.mov', '.mkv', '.webm', '.avi', '.m4v', '.flv', '.ts')


def _guardar(id_, **cambios):
    with candado:
        e = estados.setdefault(id_, {})
        e.update(cambios)
        with open(os.path.join(TRABAJOS, id_, 'estado.json'), 'w', encoding='utf-8') as f:
            json.dump(e, f, ensure_ascii=False)


def _cargar_estados():
    for id_ in os.listdir(TRABAJOS):
        p = os.path.join(TRABAJOS, id_, 'estado.json')
        if id_.startswith('_'):
            continue
        if os.path.exists(p):
            try:
                e = json.load(open(p, encoding='utf-8'))
                if e.get('estado') in ('en cola', 'procesando'):
                    e['estado'] = 'interrumpido'
                estados[id_] = e
            except Exception:
                pass


def _linea(lt, maximo=600):
    """hype reducido a <= 600 puntos y tiempos de las kills, para la gráfica de la interfaz"""
    paso, hype, kills = lt['paso'], lt['hype'] or [], lt['kills'] or []
    k = max(1, -(-len(hype) // maximo))
    puntos = [round(max(v for v in hype[i:i + k] if v is not None), 2) if any(v is not None for v in hype[i:i + k]) else 0
              for i in range(0, len(hype), k)]
    return dict(paso=paso * k, hype=puntos, kills=[round(i * paso, 1) for i, v in enumerate(kills) if v])


def trabajador():
    while True:
        id_ = cola.get()
        e = estados[id_]
        carpeta = os.path.join(TRABAJOS, id_)
        logs = []

        def log(m):
            logs.append(time.strftime('%H:%M:%S ') + str(m))
            _guardar(id_, log=logs[-60:])

        def progreso(f, txt=''):
            _guardar(id_, progreso=round(f, 3), paso=txt)

        _guardar(id_, estado='procesando', inicio=time.time())
        try:
            video = os.path.join(carpeta, e['archivo'])
            kf = re.sub(r'[^0-9.,]', '', e['opciones'].get('killfeed') or '')
            base = re.sub(r'[^A-Za-z0-9.-]', '_', e['archivo'])
            cache = os.path.join(CACHE, '%d_%s%s.npz' % (os.path.getsize(video), base, '_' + kf if kf else ''))
            r = pipeline.procesar(video, os.path.join(carpeta, 'clips'), e['opciones'], log, progreso, cache=cache)
            _guardar(id_, estado='listo', clips=r['clips'], progreso=1.0, segundos=r['segundos'], duracion=r['duracion'],
                     linea=_linea(r['linea_tiempo']))
        except Exception as ex:
            log('ERROR: ' + str(ex))
            log(traceback.format_exc()[-1500:])
            _guardar(id_, estado='error', error=str(ex))
        finally:
            if e.get('opciones', {}).get('borrar_original'):
                try:
                    os.remove(os.path.join(carpeta, e['archivo']))
                except OSError:
                    pass
            cola.task_done()


@app.route('/')
def inicio():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/fuentes/<path:archivo>')
def fuentes(archivo):
    return send_from_directory(os.path.join(RAIZ, 'fuentes'), archivo)


@app.route('/api/clave', methods=['POST'])
def api_clave():
    """guarda la clave de Gemini pegada en la app (solo en esta PC, en clave_gemini.txt)"""
    e = gemini.guardar_clave(request.form.get('clave', ''))
    return jsonify(gemini=e == 'ok', gemini_estado=e)


@app.route('/api/estado')
def api_estado():
    return jsonify(gemini=gemini.disponible(), gemini_estado=gemini.estado(), whisper=transcribir.whisper_disponible(), opciones=pipeline.OPCIONES)


def _num(v, tipo, defecto):
    try:
        return tipo(v)
    except (TypeError, ValueError):
        return defecto


def _opciones(fo):
    op = dict(
        clips=max(1, min(30, _num(fo.get('clips'), int, 8))),
        dmin=max(5, _num(fo.get('dmin'), float, 15)), dmax=min(180, _num(fo.get('dmax'), float, 45)),
        formato=fo.get('formato', 'auto'), filtro=fo.get('filtro', 'todo'), gemini=fo.get('gemini', 'auto'),
        subtitulos=fo.get('subtitulos', 'auto'), marca=fo.get('marca', '')[:40], color=fo.get('color', '#B026FF'),
        indicaciones=fo.get('indicaciones', '')[:500], idioma=fo.get('idioma', 'español'),
        killfeed=fo.get('killfeed') or None, borrar_original=fo.get('borrar_original') == '1')
    if op['dmax'] < op['dmin']:
        op['dmax'] = op['dmin'] + 10
    return op


def _nuevo_trabajo(nombre, op, guardar):
    id_ = time.strftime('%Y%m%d-%H%M%S-') + uuid.uuid4().hex[:6]
    os.makedirs(os.path.join(TRABAJOS, id_))
    guardar(os.path.join(TRABAJOS, id_, nombre))
    _guardar(id_, id=id_, archivo=nombre, opciones=op, estado='en cola', progreso=0, paso='En cola', creado=time.time(), log=[])
    cola.put(id_)
    return id_


@app.route('/api/subir', methods=['POST'])
def api_subir():
    f = request.files.get('video')
    if not f or not f.filename:
        return jsonify(error='No llegó ningún video'), 400
    nombre = re.sub(r'[^\w.\- ]', '_', os.path.basename(f.filename))
    if not nombre.lower().endswith(EXT):
        return jsonify(error='Formato no soportado: usa mp4, mov, mkv, webm...'), 400
    return jsonify(id=_nuevo_trabajo(nombre, _opciones(request.form), f.save))


@app.route('/api/trabajo/<id_>/rehacer', methods=['POST'])
def api_rehacer(id_):
    """sacar otros clips del mismo video con otras opciones, sin subirlo ni analizarlo otra vez"""
    e = estados.get(id_)
    if not e:
        abort(404)
    origen = os.path.join(TRABAJOS, id_, e['archivo'])
    if not os.path.exists(origen):
        return jsonify(error='El video original ya se borró: súbelo otra vez'), 400

    def enlazar(destino):
        try:
            os.link(origen, destino)                       # mismo archivo, no ocupa espacio extra
        except OSError:
            import shutil
            shutil.copy2(origen, destino)
    return jsonify(id=_nuevo_trabajo(e['archivo'], _opciones(request.form), enlazar))


@app.route('/api/trabajos')
def api_trabajos():
    with candado:
        lista = sorted(estados.values(), key=lambda e: -e.get('creado', 0))
    return jsonify(lista)


@app.route('/api/trabajo/<id_>', methods=['DELETE'])
def api_borrar(id_):
    if id_ not in estados or estados[id_].get('estado') in ('procesando',):
        abort(400)
    import shutil
    shutil.rmtree(os.path.join(TRABAJOS, id_), ignore_errors=True)
    with candado:
        estados.pop(id_, None)
    return jsonify(ok=True)


@app.route('/clips/<id_>/<path:archivo>')
def clip(id_, archivo):
    if id_ not in estados:
        abort(404)
    return send_from_directory(os.path.join(TRABAJOS, id_, 'clips'), archivo,
                               as_attachment=request.args.get('descargar') == '1')


@app.route('/clips/<id_>.zip')
def zip_clips(id_):
    if id_ not in estados:
        abort(404)
    d = os.path.join(TRABAJOS, id_, 'clips')
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, 'w', zipfile.ZIP_STORED) as z:
        for n in sorted(os.listdir(d)):
            if n.endswith(('.mp4', '.jpg', 'resumen.json')):
                z.write(os.path.join(d, n), n)
    mem.seek(0)
    base = os.path.splitext(estados[id_]['archivo'])[0]
    return send_file(mem, mimetype='application/zip', as_attachment=True, download_name=f'clips_{base}.zip')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--puerto', type=int, default=5000)
    ap.add_argument('--red', action='store_true', help='abrir también a otros aparatos de tu Wi-Fi')
    ap.add_argument('--sin-navegador', action='store_true')
    a = ap.parse_args()
    _cargar_estados()
    threading.Thread(target=trabajador, daemon=True).start()
    url = f'http://localhost:{a.puerto}'
    print(f'Recortador de clips listo en {url}')
    if not a.sin_navegador:
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    app.run(host='0.0.0.0' if a.red else '127.0.0.1', port=a.puerto, threaded=True)


if __name__ == '__main__':
    main()
