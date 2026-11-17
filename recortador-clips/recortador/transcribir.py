"""TRANSCRIBIR — palabras con tiempo para los subtítulos de cada clip.
1) faster-whisper en tu PC (gratis, sin internet después de bajar el modelo la primera vez)
2) si no está instalado, Gemini
3) si no hay ninguno, el clip sale sin subtítulos
"""
import os

_modelo = None
_whisper_roto = False
MODELO_WHISPER = os.environ.get('RECORTADOR_WHISPER', 'small')     # tiny / base / small / medium / large-v3

RISAS = ('jaja', 'jeje', 'haha', 'hehe', 'kkkk', '[risas]', '(risas)', '[laughter]', '(laughs)', '[laughs]')


def whisper_disponible():
    try:
        import faster_whisper  # noqa: F401
        return True
    except Exception:
        return False


def _whisper(wav, idioma=None):
    global _modelo
    from faster_whisper import WhisperModel
    if _modelo is None:
        _modelo = WhisperModel(MODELO_WHISPER, device='auto', compute_type='int8')
    segs, _ = _modelo.transcribe(wav, language=idioma, word_timestamps=True, vad_filter=True)
    out = []
    for s in segs:
        for w in s.words or []:
            if w.word.strip():
                out.append(dict(texto=w.word.strip(), inicio=float(w.start), fin=float(w.end)))
    return out


def usa_whisper(motor):
    return motor in ('auto', 'whisper') and whisper_disponible() and not _whisper_roto


def palabras(wav, motor='auto', idioma=None, log=print):
    """motor: auto | whisper | gemini | no"""
    if motor == 'no':
        return []
    global _whisper_roto
    if motor in ('auto', 'whisper') and whisper_disponible() and not _whisper_roto:
        try:
            return _whisper(wav, idioma)
        except Exception as e:
            _whisper_roto = True                            # no reintentar en cada clip
            log(f'Whisper falló ({e}); uso Gemini para los subtítulos')
    if motor in ('auto', 'gemini'):
        from . import gemini
        if gemini.disponible():
            try:
                return gemini.transcribir(wav)
            except Exception as e:
                log(f'Gemini no pudo transcribir: {e}')
    return []


def hay_risas(pals):
    return sum(1 for p in pals if any(r in p['texto'].lower() for r in RISAS))
