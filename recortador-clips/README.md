# Recortador de Clips — Valorant / e-sports

Subes un video largo (partida, VOD de torneo, entrevista, stream) y la app saca sola los mejores momentos
como clips **verticales 9:16 (1080x1920)** listos para TikTok, Reels y YouTube Shorts:

- **Kills**: lee el killfeed de Valorant (arriba a la derecha) y junta kills seguidas → *kill, multikill, ACE*.
- **Hype**: detecta cuando el caster grita o el público explota (volumen y brillo del audio por encima de lo normal).
- **Entrevistas y momentos graciosos**: detecta caras grandes (cámara de entrevista o de jugador) y risas en la transcripción.
- **Gemini (opcional, recomendado)**: la IA mira el video completo, entiende qué pasa (clutch, ACE, broma en la entrevista…),
  elige los momentos y les pone un título gancho. Si coincide con el killfeed o el audio, el clip sube de puntuación.
- **Subtítulos palabra por palabra** (estilo TikTok, palabra activa en morado) con Whisper en tu PC o con Gemini.
- **Formato vertical automático**: partidas = centro del juego grande + fondo desenfocado + recuadro del killfeed;
  entrevistas = recorte que sigue la cara. Audio a −14 LUFS. Portada `.jpg` por clip.

## Instalar (una vez)

1. Instala **Python 3.10+** (python.org; en Windows marca "Add to PATH").
2. Instala **ffmpeg**: Windows `winget install Gyan.FFmpeg` · Mac `brew install ffmpeg`.
3. (Recomendado) Clave gratis de **Gemini**: https://aistudio.google.com/apikey y guárdala:
   - Windows (una vez, en una terminal): `setx GEMINI_API_KEY "tu_clave"` y vuelve a abrir la terminal.
   - Mac: agrega `export GEMINI_API_KEY="tu_clave"` a `~/.zshrc`.

## Usar

- **Windows**: doble clic en `iniciar.bat`. **Mac/Linux**: `./iniciar.sh`.
- Se abre `http://localhost:5000`: arrastra tus videos, ajusta opciones y espera. Cada clip se ve y se descarga ahí
  (o todos juntos en .zip). Los archivos quedan en `trabajos/`.
- Desde el celular en la misma Wi-Fi: `python app.py --red` y abre `http://IP-de-tu-PC:5000`.

Línea de comandos (sin la app):

```
python recortar.py partido.mp4 --clips 10 --marca @tu_canal
python recortar.py entrevista.mp4 --filtro graciosos --formato entrevista
python recortar.py stream.mkv --sin-gemini --dmin 20 --dmax 60
```

## Opciones

| Opción | Qué hace |
|---|---|
| Clips por video | cuántos clips sacar (los mejores primero) |
| Duración mín./máx. | largo de cada clip en segundos (15–45 por defecto) |
| Qué buscar | todo · solo kills/jugadas · graciosos/reacciones · entrevistas |
| Formato | auto · juego (centro grande) · completo (16:9 entero, se ve el HUD) · entrevista (sigue la cara) |
| Subtítulos | auto · Whisper · Gemini · sin subtítulos |
| Indicaciones para la IA | texto libre: "prioriza a Jett", "solo cuando se ríen", "nada de pausas técnicas" |
| Zona del killfeed | si tu video no es la vista normal de Valorant: `x0,y0,x1,y1` en proporción 0–1 |

## Cómo está armado

```
app.py                  app web (Flask): subir, cola de trabajos, ver y descargar clips
recortar.py             lo mismo por línea de comandos
recortador/
  medios.py             ffprobe/ffmpeg: info, audio, cuadros, copia ligera 360p
  analisis.py           línea de tiempo de 0.5 s: hype del audio, cortes de toma, movimiento, killfeed, caras (YuNet)
  gemini.py             Gemini mira el video y propone momentos; transcribe el audio de cada clip
  transcribir.py        Whisper local → Gemini → sin subtítulos
  momentos.py           junta las señales, puntúa, ajusta duración y cortes de toma, elige sin repetir
  vertical.py           render 1080x1920: fondo desenfocado / seguimiento de cara, títulos y subtítulos ASS, −14 LUFS
  pipeline.py           orquesta todo y escribe resumen.json
fuentes/                Anton y Bebas Neue (del Motor Morado, licencia OFL)
modelos/yunet.onnx      detector de caras YuNet (opencv_zoo, MIT)
web/index.html          interfaz
```

Del **Motor Morado** se reusan las fuentes, el estilo de subtítulos palabra por palabra (v15), el audio a −14 LUFS
y la idea del editor que revisa. Los clips se pueden pasar después por `aplicar_look.py` del motor para darles el color
de una referencia.

## Límites conocidos

- El detector de kills por killfeed está calibrado para la vista normal de Valorant (16:9). Con overlays de torneo
  distintos puede fallar: usa Gemini o ajusta la "zona del killfeed".
- Sin Gemini, los títulos son genéricos ("TRIPLE KILL", "EL CASTER EXPLOTÓ").
- Gemini acepta videos de hasta ~1 h por vez con la copia de 360p; para VODs de 3–4 h, córtalos por mapa.
- Respeta los derechos de los videos que recortes (VODs oficiales de Riot/ligas tienen sus reglas de uso).
