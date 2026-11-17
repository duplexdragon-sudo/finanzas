# Aprendizaje: motion graphics de @DuplexDragon_ (estilo morado editorial)

Resumen de cómo se hicieron los videos verticales de Valorant/esports de Carlos (TenZ, LOUD, SMG, aspas), para reutilizarlo en otros proyectos, como el canal de animación 2D.
Todo el código está en `motion_graphics/`. Aquí no hay videos, audios ni claves.

---

## 1. Herramientas y flujo

| Paso | Herramienta | Qué hace |
|---|---|---|
| Investigar y verificar la noticia | Agent Reach (`agent-reach web search` / `read`: Exa + Jina) y fuentes como vlr.gg, THESPIKE.GG, Sheep Esports, Strafe, Liquipedia | Ningún dato sale sin fuente. Si algo no es oficial, se dice "según reportes". |
| Analizar videos de referencia | ffmpeg (hojas de cuadros por segundo) + Gemini Flash (`gemini-3-flash-preview`) para transcribir el audio con tiempos | Ingeniería inversa del ritmo, los textos y las transiciones (ver `motion_graphics/docs/ingenieria_inversa_*.md`). |
| Imágenes de objetos 3D o fondos | Gemini (app de Carlos; la API gratis no da modelos de imagen) con los prompts de `docs/PROMPTS_GEMINI_estilo_morado.txt` y `docs/prompts_estilo_busto_morado.md` | Objetos "busto morado" sin texto, en fondo plano. |
| Recortar personas y objetos | rembg: `birefnet-portrait` (mejor pelo), `u2net_human_seg` (silueta de persona), `isnet-general-use` / `birefnet-general` (objetos) → `motor/recortar_ia.py`, `motor/combo.py` | `combo.py` combina el pelo fino de BiRefNet con la máscara de persona para quitar sillas y monitores. `motor/revisar_recortes.py` revisa los bordes y arma una hoja de control sobre morado. |
| Arte oficial de Valorant | valorant-api.com (`fullPortrait`, `displayIcon` y los íconos de habilidades) | Agentes y habilidades. |
| Voz | ElevenLabs, voz **Andrés** (`OKVzBuEkwwiTZZFB3pCw`), modelo **eleven_v4**, endpoint `/with-timestamps`, `mp3_44100_128`, una frase por llamada, con los ajustes guardados de la voz | Los tiempos por palabra sincronizan cada texto en pantalla (función `wt(frase, "palabra")`). Después se acelera a 1,1× con `atempo`. |
| Efectos de sonido | ElevenLabs `sound-generation` (braam, hit808, glitch, rewind, swoosh, riser, crowd) + librería propia (whoosh, pop, punch, impact, shimmer, clink, boom, cheer, typing) | Ver la sección 4. |
| Render | Python + PIL + numpy, cuadro a cuadro en 720×1280 a 30 fps, enviado a ffmpeg (libx264 crf 16, escalado lanczos a 1080×1920, AAC 256k) | `render/render_*.py`. Cada uno tiene `--preview t1,t2,...` para revisar cuadros sueltos antes del render completo. |
| Control de calidad | Chequeo automático de "tramos quietos" (diferencia entre cuadros a 10 fps en una ventana de 0,5 s) + `ebur128` para medir volumen + hoja de cuadros cada 3 s | Regla: **0 tramos quietos** y volumen final de unos −14 LUFS. |

### Flow (Google Flow / Veo)
- **Acceso:** Flow es la herramienta web de Google (labs.google/flow) con la cuenta de Carlos. Se entra desde su navegador; desde esta sesión en la nube no hubo acceso directo. Genera **clips de video (Veo)** a partir de texto o de una imagen, y también **imágenes**.
- **Lo que aprendimos (ver `docs/ingenieria_inversa_video_flow.md`):** casi todos los videos de referencia **no usan video generado**. Son imágenes fijas animadas: posición, escala, rotación 3D y desenfoque. Flow solo vale la pena para 1 a 3 tomas con movimiento real.
- **Reglas para no gastar créditos:**
  1. Aprobar primero todas las imágenes.
  2. Probar en modo Fast.
  3. Escribir "no text, no letters, no logos" en cada prompt.
  4. No pedir famosos.
  5. Generar sin diálogo.
  6. Un solo movimiento por prompt.
- En los videos finales de LOUD, SMG y aspas **no se usó Flow**: todo es motion graphics por código, con clips reales recortados.

---

## 2. Estilo visual

- **Paleta:** morado principal `PUR = (115, 16, 165)`, lila `LIL = (166, 97, 196)`, lila claro `LILL = (228, 205, 238)`, blanco, tinta `INK = (17, 17, 17)`. Para alertas y sellos, rojo `(200, 30, 60)`.
- **Duotono morado:** todas las fotos y clips pasan por un LUT de 4 paradas, de casi negro morado a lila blanco (`duo()` en `render_tenz_morado.py`; `LUTA` en `render_loud.py` para los clips).
- **Tipografías:**
  - **Anton** para titulares grandes y golpes.
  - **Playfair Display Italic** (400/900) para frases editoriales en cursiva.
  - **Poppins** para etiquetas, créditos y la @.
  - Todas son de Google Fonts/Fontsource.
- **Fondos:** se alternan blanco con cuadrícula fina y "luz de ventana", y morado con cuadrícula y destellos ("burst") en las esquinas. Detrás va una palabra gigante en tono fantasma ("LOUD", "2026", "FUT"…).
- **Composición:** el texto arriba (zona segura desde unos 120 px), la persona recortada abajo con desvanecido inferior, esquineras en escenas alternas y la @DuplexDragon_ arriba a la derecha.
- **Animaciones de texto:**
  - `word()`: entra con desenfoque que se aclara y un pequeño deslizamiento.
  - `slam()`: golpe que va de escala 1,9 a 1.
  - `ribbon()`: cinta que se despliega.
  - `stamp()`: sello rotado que cae.
  - `counter()`: contadores.
  - `puzzle_tile()`: letra hecha de 4 piezas.
  - Calendario que pasa hojas.
  - Firma que se dibuja sola.
- **Movimiento constante (regla de Carlos: nunca una pantalla quieta):**
  - Zoom lento de cámara en cada escena.
  - Partículas flotando.
  - Anillos punteados que giran.
  - Fotos que flotan.
  - Confeti en los momentos de victoria.
  - Billetes que caen.
  - Banderas que ondean.
- **Anillo 3D de habilidades** (`player_orbit()`): los íconos de los agentes que jugó cada jugador giran en elipse; los de atrás pasan detrás de la foto.
- **Transiciones:** barrido diagonal morado de 0,18 s, más un zoom de entrada de 1,06 a 1.
- **Impactos** (`impact_fx()`): en cada golpe fuerte, sacudida de cámara, separación RGB de unos 0,12 s y un destello blanco de 0,05 s.
- **Ritmo:** una escena por frase de voz, de 3 a 6 s cada una. Cada palabra clave aparece justo cuando se dice.
- **Estructura del guion:** gancho en el segundo 0 → frase motivacional → historia con datos → remate → llamada a la acción (comentar, seguir con el botón SEGUIR→SIGUIENDO y el cursor, compartir, guardar) → fuentes.

---

## 3. Diseño de sonido y mezcla

- **Voz:** `loudnorm I=-15:TP=-1.5:LRA=11`, sin efectos. Carlos pidió la voz limpia; la reverb y el EQ "de locutor" los rechazó.
- **Música** (por ejemplo "Deep End"):
  - Arranca en la caída fuerte de la canción.
  - Volumen 0,2 y EQ −4 dB en 3 kHz.
  - **Ducking:** `sidechaincompress` (threshold 0.02, ratio 8, attack 15 ms, release 350 ms) con la voz como señal.
- **Efectos de sonido al 55 %:**
  - swoosh en cada cambio de escena
  - hit808 en cada golpe fuerte y glitch en la mitad de ellos
  - braam en el gancho y en el clímax
  - riser antes del clímax y crowd en la victoria
  - pop en cada elemento que aparece
- **Final:** `alimiter 0.95`, que deja unos **−14 LUFS**. Fade-out de 1,5 s.

---

## 4. Qué le gustó a Carlos

- La estética morada editorial: duotono, Anton con cursiva serif, cuadrícula.
- Las habilidades girando en anillo 3D alrededor del jugador (venía del video de TenZ).
- El trofeo con rayos de luz, brillo que lo barre, resplandor y destellos.
- Los ganchos fuertes desde el segundo 0, con una frase motivacional después.
- Los impactos con sacudida y los sonidos fuertes (braam, 808, glitch).
- Las cadenas que se rompen, el calendario que se rebobina con efecto VHS y la firma que se dibuja.
- Que **nunca haya un momento quieto en pantalla**.
- Sus propios recursos en morado: billete, banderas y objetos.
- Usar la foto oficial del evento y del equipo.
- Usar clips reales recortados, sin la cámara del creador, sin marcas de agua y sin subtítulos ajenos.
- La mención a otros creadores, por ejemplo Perdomix.

## 5. Qué rechazó o corrigió

- **Recortes:**
  - Malos recortes: medio rostro, brazos y codos cortados, pelo con borde recto. Preferible dejar la silla a cortar mal a la persona.
  - Sombras y halos en los objetos.
- **Composición:**
  - Textos amontonados o encima de otros elementos.
  - Elementos que tapan la cara.
  - Alas en TenZ.
  - El logo de un equipo encima del texto.
- **Fotos y voz:**
  - Fotos feas descargadas de internet cuando él ya había mandado las suyas.
  - El clon de su voz ("una porquería"): se usa la voz Andrés.
  - Efectos de reverb o "configuraciones" en la voz: la quiere limpia.
- **Ritmo:** pantallas estáticas, por ejemplo Darker quieto al inicio o el reloj de arena sin vida.
- **Datos:**
  - Datos falsos o sin verificar. Ejemplos: SMG eligió 4 duelistas, no 5; el fichaje de aspas es un "acuerdo verbal"; el trofeo de 2022 no es el de 2026.
  - Logos con un año equivocado.
  - Fotos de otro equipo o de otra plantilla.

---

## 6. Rutas de los archivos clave (`motion_graphics/`)

| Archivo | Para qué |
|---|---|
| `render/render.py` | Motor base: `text_layer`, `paste`, curvas de suavizado (`eo`, `eio`), `rotate_y` 3D, desenfoque de movimiento, `scale_about` |
| `render/render_motion.py` | Paleta, `word`, `pop`, `shadow`, cuadrícula y destellos ("burst") |
| `render/render_tenz_morado.py` | Duotono, fondos `bg()`, `tenz_orbit`, `card`, `brackets`, `puzzle_tile`, `ribbons`, luz de ventana |
| `render/render_loud.py` | `slam`, `ribbon`, `ring`, `counter`, `particles`, `confetti`, `flag_wave`, `trophy_fx`, `chain_band`, `impact_fx`, `vhs`, `calendar`, `player_orbit`, mezcla de audio completa |
| `render/render_smg.py` | Voz original de un clip mezclada con la narración, subtítulos, `stamp`, `ping_meter`, `lineup`, `clip()` en duotono |
| `render/render_aspas.py` | Video más reciente (ASPAS_FUT): billetes, banderas, `money`, `pen_sign`, `roster_chip`, `wave_flag` |
| `render/render_dia1u.py` | Íconos de la llamada a la acción (comentar, seguir, compartir, guardar) |
| `render/portada_*.py` | Portadas 9:16 con recorte 4:5 para la cuadrícula de Instagram |
| `motor/recortar_ia.py`, `motor/combo.py`, `motor/revisar_recortes.py` | Recortes con IA y control de calidad |
| `motor/gen_imagenes_gemini.py` | Generar imágenes con la API de Gemini (requiere un plan con modelos de imagen) |
| `guiones/*.json`, `guiones/*.md` | Guiones finales (una frase por línea) |
| `docs/` | Ingeniería inversa de referencias y prompts de Gemini para objetos |

**Requisitos:** Python 3 con Pillow, numpy, scipy y rembg; ffmpeg; las fuentes Anton, Playfair Display y Poppins en `fonts/`. Las rutas a recursos (`motion/objetos`, `tz2/hab`, `audio/*.48.wav`, `loud/`, `duel/`, `aspas/`) son relativas a la carpeta de trabajo original y no se suben, porque son imágenes, audio y clips pesados o de terceros.
