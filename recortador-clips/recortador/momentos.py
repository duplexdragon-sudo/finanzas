"""MOMENTOS — junta las señales (kills, hype del audio, entrevistas, Gemini) en una lista de clips con puntuación."""
import numpy as np

from .analisis import PASO, cortes, es_entrevista


def _i(t):
    return max(0, int(round(t / PASO)))


def _hype_max(a, t0, t1):
    h = a['hype'][_i(t0):_i(t1) + 1]
    return float(h.max()) if len(h) else 0.0


def candidatos_kills(v, a):
    ks = [i * PASO for i in np.flatnonzero(v['kills'] > 0)]
    grupos = []
    for t in ks:
        if grupos and t - grupos[-1][-1] < 9:
            grupos[-1].append(t)
        else:
            grupos.append([t])
    out = []
    for g in grupos:
        n = len(g)
        t0, t1 = g[0] - 5, g[-1] + 3
        # alarga el final mientras siga la reacción (caster/público)
        while t1 < g[-1] + 7 and _i(t1) < len(a['hype']) and a['hype'][_i(t1)] > 1.5:
            t1 += PASO
        hm = _hype_max(a, t0, t1)
        tipo = 'ace' if n >= 5 else 'multikill' if n >= 3 else 'kill'
        titulo = {1: 'QUÉ KILL', 2: 'DOBLE KILL', 3: 'TRIPLE KILL', 4: 'CUÁDRUPLE KILL'}.get(n, 'ACE')
        out.append(dict(inicio=t0, fin=t1, pico=g[-1], tipo=tipo, titulo=titulo, kills=n,
                        puntuacion=min(10.0, 1.5 + 1.5 * n + 0.6 * max(0, hm)), fuente='killfeed',
                        motivo=f'{n} kill(s) en el killfeed, hype {hm:.1f}'))
    return out


def candidatos_hype(v, a, umbral=2.3, separacion=20):
    h = a['hype']
    out = []
    orden = np.argsort(-h)
    picos = []
    for i in orden:
        if h[i] < umbral:
            break
        t = i * PASO
        if all(abs(t - p) > separacion for p in picos):
            picos.append(t)
    for t in sorted(picos):
        i = _i(t)
        ent = es_entrevista(v, max(0, i - 16), i + 8) if len(v['cara_area']) else False
        tipo = 'gracioso' if ent else 'hype'
        out.append(dict(inicio=t - (10 if ent else 8), fin=t + 4, pico=t, tipo=tipo,
                        titulo='SE RIÓ EN LA ENTREVISTA' if ent else 'EL CASTER EXPLOTÓ',
                        puntuacion=min(10.0, 1.5 + 0.9 * float(h[i])), fuente='audio',
                        motivo=f'pico de audio {h[i]:.1f} ' + ('en entrevista' if ent else '')))
    return out


def _solape(a, b):
    i = max(0, min(a['fin'], b['fin']) - max(a['inicio'], b['inicio']))
    return i / max(1e-6, min(a['fin'] - a['inicio'], b['fin'] - b['inicio']))


def ajustar(c, dur, dmin, dmax, ts_cortes):
    t0, t1 = c['inicio'], c['fin']
    pico = c.get('pico', (t0 + t1) / 2)
    if t1 - t0 < dmin:                                     # más contexto antes que después
        falta = dmin - (t1 - t0)
        t0 -= falta * 0.65
        t1 += falta * 0.35
    if t1 - t0 > dmax:                                     # recorta alrededor del momento fuerte
        t0 = max(t0, min(pico - dmax * 0.65, t1 - dmax))
        t1 = t0 + dmax
    # empezar y terminar en cortes de toma cercanos (se ve limpio)
    cerca = [x for x in ts_cortes if abs(x - t0) <= 1.5 and x < pico - 2]
    if cerca:
        t0 = min(cerca, key=lambda x: abs(x - t0))
    cerca = [x for x in ts_cortes if -1.5 <= x - t1 <= 1.0 and x > pico + 1]
    if cerca:
        t1 = min(cerca, key=lambda x: abs(x - t1)) - 0.05
    t0 = max(0.0, t0)
    t1 = min(dur, t1)
    c = dict(c, inicio=round(t0, 2), fin=round(t1, 2))
    c['pico'] = float(min(max(pico, c['inicio']), c['fin']))
    return c


FILTROS = {
    'todo': None,
    'kills': {'kill', 'multikill', 'ace', 'clutch', 'jugada', 'hype'},
    'graciosos': {'gracioso', 'entrevista', 'reaccion'},
    'entrevistas': {'entrevista', 'gracioso'},
}


def elegir(v, a, dur, n=8, dmin=15, dmax=45, gem=None, filtro='todo'):
    ts = cortes(v) if len(v.get('corte', [])) else []
    cands = candidatos_kills(v, a) + candidatos_hype(v, a)
    final = []
    for g in gem or []:                                    # Gemini manda; si coincide con una señal, más puntos
        g = dict(g)
        g['puntuacion'] = g['puntuacion'] * 1.1
        g.setdefault('pico', (g['inicio'] + g['fin']) / 2)
        for c in cands:
            if _solape(g, c) > 0.3:
                g['puntuacion'] += 1.5
                g['kills'] = max(g.get('kills', 0), c.get('kills', 0))
                g['motivo'] = (g.get('motivo', '') + ' | ' + c['motivo']).strip(' |')
                g['pico'] = c['pico']
                c['usado'] = True
        final.append(g)
    final += [c for c in cands if not c.get('usado')]
    tipos = FILTROS.get(filtro)
    if tipos:
        final = [c for c in final if c['tipo'] in tipos]
    final = [ajustar(c, dur, dmin, dmax, ts) for c in final]
    final.sort(key=lambda c: -c['puntuacion'])
    elegidos = []
    for c in final:
        if c['fin'] - c['inicio'] < min(5, dmin):
            continue
        if all(_solape(c, e) < 0.25 for e in elegidos):
            elegidos.append(c)
        if len(elegidos) >= n:
            break
    for k, c in enumerate(elegidos, 1):
        c['rango'] = k
        c['puntuacion'] = round(min(10.0, c['puntuacion']), 1)
    return elegidos
