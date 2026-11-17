# Ingeniería inversa: video "ak ARTIST ko…" → recreación con Flow (v2, revisado)

**Video original:** 720×1280 (9:16), 30 fps, 18,75 s, audio AAC estéreo. Es **una sola composición sin cortes duros**: todas las escenas cambian con un *push* (empuje) animado.
**Cómo lo revisé:** saqué cuadros cuadro a cuadro (15 fps en cada transición), cuadros a resolución completa para leer los textos, una curva de volumen del audio cada 0,1 s y la transcripción del audio con Gemini.

---

## 0. Lo MÁS importante para no gastar créditos

**El video original NO tiene video generado ni filmado.** Todo son **imágenes fijas** (estatua, tarjeta, recortes de artistas, panel) que se mueven en After Effects con posición, escala, rotación 3D y desenfoque. Ningún personaje se mueve por sí mismo: el bailarín, el cantante y el baterista son **PNG quietos**.

Por eso, si quieres el resultado **igual** al original y gastando lo mínimo:

| Elemento | ¿Hace falta video de Flow (Veo)? | Cómo hacerlo barato |
|---|---|---|
| Estatua con laptop | **No** | 1 imagen (Nano Banana / Imagen) y luego zoom en CapCut |
| Foto dentro de la tarjeta de Instagram | **No** | 1 imagen; la tarjeta y el giro 3D se hacen en CapCut |
| Bailarín / cantante / baterista | **No** | 3 imágenes de cuerpo entero con fondo liso, y quitar el fondo en CapCut |
| Panel de vidrio y comentarios | **No** | Se diseña en CapCut/Canva (rectángulo + desenfoque + borde) |
| Fondo negro con grano y polvo | **No** | Overlay gratis de "film grain / dust" |
| Hojas de palma desenfocadas | **No** | 1 imagen PNG de hoja + desenfoque |

**Flow-video (Veo) solo conviene si quieres MEJORAR el original**, por ejemplo que el baterista toque de verdad o que la estatua escriba. En ese caso, gasta créditos **solo en esos 1–3 clips** (ver la sección 5).

**Reglas para no perder créditos:**
1. Genera y aprueba **todas las imágenes primero**. Son mucho más baratas que el video.
2. En video, prueba siempre primero en el modo **rápido (Fast)** y usa el de calidad solo con la toma ya aprobada.
3. Escribe **"no text, no letters, no logos"** en cada prompt. Si Veo mete texto deformado, el clip no sirve.
4. **No pidas famosos.** En el original, el bailarín es claramente Michael Jackson y el cantante se parece a Sonu Nigam. Flow lo rechaza o te cobra un clip inservible. Usa personas genéricas.
5. Pide clips **sin diálogo**. La voz va aparte (ver la sección 3), porque si Veo genera voz en hindi, casi seguro sale mal.
6. Cada prompt describe **un solo movimiento simple**. Si pides varias acciones, Veo suele fallar y tienes que repetir.

---

## 1. Línea de tiempo exacta (cuadro a cuadro)

| Tiempo | Escena | Contenido | Animación dentro de la escena | Transición de salida (verificada a 15 fps) |
|---|---|---|---|---|
| **0,0–2,6 s** | **1. Póster claro** | Fondo blanco lavanda con una cuadrícula fina en el centro. La estatua de mármol (tipo *El Pensador*) usa una laptop plateada. Arriba a la derecha, código de barras + "05 DEC 2025". Abajo a la izquierda, "RISHI KUMAR". Una línea curva fina cruza el póster en diagonal y hay hojas de palma azul marino desenfocadas en las esquinas. | **0–0,6 s:** un cursor (flecha azul marino) entra y "escribe" el título letra por letra: "ak" → "ARTIS" → "ARTIST" → "ko", dentro de un recuadro punteado. **0,4–0,9 s:** la estatua aparece desde la cuadrícula, de pixelada/borrosa a nítida. **~1,3 s:** "Paise ke alwa" sale palabra por palabra. **~2,0 s:** aparece la píldora azul marino con "KYA CHAIYE HOTA HAI ?" en serif itálica blanca, y el cursor la "clica". El párrafo de abajo se escribe solo. Las hojas se mueven lento y la línea curva se dibuja. | **Push vertical hacia arriba (2,5–2,9 s):** todo el póster sube y sale, y desde abajo entra la escena negra. Con desenfoque de movimiento ligero. |
| **2,8–5,4 s** | **2. Tarjeta Instagram 3D** | Fondo negro con esferas azules grandes, nítidas arriba y desenfocadas abajo, y un arco circular blanco fino abajo a la izquierda. Arriba, una cita dentro de un marco de esquinas: "True impact comes from consistent effort. When someone works with vision and dedication, their actions inspire many and create a powerful ripple of positive change." La tarjeta blanca gruesa es un post de **dc.kumar._ · Follow** con la foto de un hombre de espaldas en un escenario con foco y público, "**2.018 Likes**" y "**Virel Reel edit #stonevfx #insta**". Debajo, "OFCOURSE USKE" en serif itálica y "**KAAM KI TARIF**" en serif negra, dentro de un recuadro de línea discontinua. Abajo, un párrafo en MAYÚSCULAS chicas: "GREAT WORK SPEAKS BEFORE THE WORLD DOES…". | La tarjeta **entra desde abajo a la derecha girando en 3D** (eje Y ~40° y algo de eje Z), sube y se endereza en ~0,6 s con *ease-out*. Después flota muy poco. "OFCOURSE USKE" y "KAAM KI TARIF" salen palabra por palabra, al ritmo de la voz. | **Push horizontal a la izquierda (5,2–5,7 s):** la tarjeta y los textos se van a la izquierda (la tarjeta gira un poco más), y desde la derecha entran el bailarín y la píldora azul. |
| **5,5–6,7 s** | **3a. NACHNE WALA** | "Fhir chahe wo" (así, con **F**) en serif negra blanca arriba. El bailarín recortado (sombrero, pose de patada) sobre un foco circular azul. Una píldora azul marino con borde blanco y "**NACHNE WALA**" en sans negra blanca. Párrafo: "An artist transforms emotions into expression, turning imagination into reality. Their creativity inspires minds, connects hearts, and leaves a timeless impact through every stroke, note, or performance." | El texto sale palabra por palabra ("Fhir" → "chahe" → "wo"; "NACHNE" → "WALA"). Hay burbujas azules flotando y un zoom lento. | Slide horizontal con desenfoque: entra el cantante y cambia el texto de la píldora. |
| **6,7–7,8 s** | **3b. GAANE WALA** | El cantante con micrófono (camisa estampada y saco negro). Mismo layout. | Igual | Igual |
| **7,8–9,0 s** | **3c. BAJANE WALA** | El baterista con batería completa. Mismo layout. | Zoom-in lento. | **Zoom-in + push hacia arriba (8,9–9,3 s):** la escena se agranda y sale por arriba. |
| **9,1–13,0 s** | **4. Panel de vidrio** | Fondo con degradado de negro (arriba a la izquierda) a azul (abajo). Hojas de palma azules desenfocadas. Un panel de *glassmorphism* (vidrio esmerilado, borde fino claro, brillo en la esquina superior izquierda). Al principio se ve un párrafo detrás del vidrio. Tarjeta de comentario: avatar, "**Nisha** @nishren" y "**Such a satisfying edit**, everything feels balanced, clean, and very well thought out." (las primeras palabras en azul, como un enlace). | **9,1–9,5 s:** el panel aparece con un destello de luz que lo recorre. **9,6–10,5 s:** caen 3–4 tarjetas de comentario y se apilan con desfase (efecto "barajar"), y quedan en una. **11,4–12,4 s:** "Par Main Hun Kon" aparece palabra por palabra, con tamaños y alturas distintos (la palabra "Kon" queda más abajo). | **12,8–13,3 s:** toda la pantalla **se aleja (zoom-out) como una tarjeta**, se desenfoca, pasa a gris con grano y luego hay un **FLASH BLANCO** de 1–2 cuadros (~13,2 s). |
| **13,3–14,8 s** | **5a. "I'M"** | Fondo negro con polvo, rayas de película y un degradado azul abajo. "I'M" en sans negra (tipo Poppins Black) blanca. | Entra **enorme (que no cabe en pantalla) con blur** justo después del flash, y se encoge suave hasta un tamaño medio (~1,5 s, *ease-out*). | **Push horizontal a la izquierda con blur fuerte (14,7–15,1 s).** |
| **15,0–18,75 s** | **5b. "ARTIST"** | "ARTIST" en la misma tipografía, y encima a la derecha "Made with after effect" en serif chico. Esquinas en serif itálica chica: "RISHI KUAMR" (arriba a la izquierda), "VFX ARTIST" (arriba a la derecha), "DC.KUMAR._" (abajo a la izquierda) y "STOE VFX" (abajo a la derecha). Ojo: en el original estos créditos tienen **erratas**. | Entra desde la derecha con blur (0,3 s) y se asienta. Las esquinas aparecen escribiéndose. Después queda quieto con grano animado. | El audio se apaga entre 15,5 y 17,0 s. Hay casi silencio hasta el final. |

**Constantes desde el segundo 2,8 hasta el final:** texto vertical chico (rotado 90°) en los bordes. A la izquierda: "rishi kumar", "@stone_vfx" y "Dec 2025". A la derecha: "Made by after effect" y "@dc.kumar._". La cámara nunca está del todo quieta.

---

## 2. Paleta (medida en los cuadros)

| Uso | Hex |
|---|---|
| Fondo claro de la escena 1 | `#E8E8F4` → `#D2D6E3` |
| Azul marino (texto, píldora, cursor, hojas en lo claro) | `#1C2D3E` |
| Negro azulado del fondo base | `#0C1723` / `#0D1621` |
| Azul medio de los degradados (escenas 3–4) | `#1D3A56` |
| Azul de acento de las esferas, el foco y la píldora | ~`#1F4F80` |
| Texto | `#FFFFFF`; gris claro `#C9CED8` |
| Único color fuera de la paleta | El rojo del corazón de Instagram y el azul de "Follow" y los hashtags |

**Curva de luz:** claro → negro de golpe (2,8 s) → azul medio (5,5–13 s) → flash blanco (13,2 s) → casi negro con grano (cierre).

## 3. Audio (transcrito con Gemini Flash y cruzado con la curva de volumen)

**Es voz en off masculina en hindi** (tono narrativo) sobre una música cinemática oscura de unos 105 BPM. Los silencios medidos coinciden con los cambios de escena:

| Tiempo (medido) | Frase | Escena |
|---|---|---|
| 0,2–2,8 s | "Ek artist ko paise ke alawa kya chahiye hota hai?" | 1 |
| 3,4–4,6 s | "Of course uske kaam ki tareef." | 2 |
| 5,5–8,1 s | "Phir chahe woh naachne wala ho, gaane wala ho, ya bajaane wala." | 3 |
| 9,0–11,0 s | "Aur same in logon ke jaise tareef mujhe bhi mili." *(frase que **no** sale escrita en pantalla: la ilustran los comentarios)* | 4 |
| 11,4–13,0 s | "Par main hoon kaun?" | 4 |
| 13,3–15,4 s | "Main hoon… [artist]" + golpe/impacto (~13,2 s, junto al flash blanco) | 5 |

⚠️ La IA entendió "Video Editor" en la última palabra, pero en pantalla dice "ARTIST". **Escúchalo tú antes de grabar tu versión.** Lo demás coincide con el texto en pantalla.

**Efectos de sonido:** *whoosh* en cada push (2,7 / 5,4 / 9,0 / 14,8 s), *riser* (tensión que sube) entre 11 y 13 s, **impacto fuerte a ~13,2 s** (el flash) y la cola del sonido que se apaga entre 15,5 y 17 s.

## 4. Tipografía
- **Serif de alto contraste** (tipo Playfair Display Black / DM Serif Display): "ARTIST" del póster, "Paise ke alwa", "KAAM KI TARIF", "Fhir chahe wo", "Made with after effect", créditos de las esquinas. Las versiones en itálica: "OFCOURSE USKE", "KYA CHAIYE HOTA HAI ?" y las esquinas del final.
- **Sans geométrica muy gruesa** (tipo Poppins ExtraBold/Black): "I'M", "ARTIST" final, "NACHNE/GAANE/BAJANE WALA".
- **Poppins Regular, chica:** párrafos, comentarios, texto vertical de los bordes, "Par Main Hun Kon".

---

## 5. Prompts

Escríbelos en inglés y en formato 9:16. Pega este **bloque de estilo** al final de cada prompt de imagen:
```
Monochrome navy-blue palette (#0C1723 navy-black, #1D3A56 mid blue, #1F4F80 accent), soft studio spotlight, high-end editorial poster look, sharp focus on subject, clean empty space above and below the subject for typography, vertical 9:16. No text, no letters, no logos, no watermark.
```

### A. Imágenes (Nano Banana / Imagen): 6 imágenes, sin video

**A1. Estatua**
```
A classical white-grey marble statue of a bearded seated thinker in a draped toga, chin resting on one hand, typing on a modern silver laptop on his knee, seated on a stone block, side three-quarter view, isolated on a plain pale lavender-white background (#E8E8F4), soft even light, museum photography, full figure visible. No text, no letters, no logos. Vertical 9:16.
```
**A2. Foto de la tarjeta de Instagram (cuadrada 1:1)**
```
A lone performer in a dark suit seen from behind standing on a stage, arms slightly open, facing a huge dark crowd, a single intense white spotlight beam from above creating haze and glow, cinematic, desaturated cool blue-grey tones, square 1:1. No text, no logos.
```
**A3. Bailarín** (genérico, NO famoso)
```
Full-body photo of a male dancer in a black fedora hat, black jacket, white shirt, black trousers, white socks and black loafers, frozen mid high-kick dance pose, dynamic, isolated on a plain flat dark navy background, studio light, sharp edges for easy cutout. Original person, not a celebrity. [STYLE BLOCK]
```
**A4. Cantante**
```
Waist-up photo of a male singer with curly dark hair, black blazer over a white graphic t-shirt, singing passionately into a vintage silver microphone held close to his mouth, eyes closed, isolated on a plain flat dark navy background, studio light, sharp edges for cutout. Original person, not a celebrity. [STYLE BLOCK]
```
**A5. Baterista**
```
Full-body photo of a male drummer in a black t-shirt playing a full wooden-finish drum kit with cymbals, sticks raised mid-hit, three-quarter view, isolated on a plain flat dark navy background, studio light, sharp edges for cutout. Original person, not a celebrity. [STYLE BLOCK]
```
**A6. Hoja de palma (PNG para las esquinas)**
```
A single tropical palm leaf silhouette in solid navy blue (#1C2D3E) on a pure white background, flat, high contrast, top-down. No text.
```

### B. Video en Flow (Veo): OPCIONAL, solo si quieres mejorar el original
Usa **Frames to Video** con la imagen aprobada como primer cuadro. Pruébalo primero en modo Fast.

**B1. Estatua que escribe** (con A1)
```
The marble statue stays completely still except his fingers gently typing on the laptop. Locked-off camera with a very slow push-in. Soft light. No camera cuts, no new objects, no text, no letters, no dialogue, no music.
```
**B2. Baterista tocando** (con A5)
```
The drummer plays a steady rock beat, sticks hitting snare and cymbals, cymbals vibrating. Locked-off camera, background stays a flat dark navy color. No camera cuts, no text, no dialogue.
```
**B3. Fondo final con grano** (solo si no tienes un overlay)
```
Pure black background with a soft deep-blue gradient glow rising from the bottom, heavy vintage film grain, floating dust specks and occasional film scratches. Static camera with very subtle shake. Nothing else in frame. No text, no letters, no people, no dialogue.
```

---

## 6. Montaje en CapCut (orden exacto)

1. **Proyecto 9:16, 30 fps, de 18,75 s.** Pon primero la **voz** (grábala tú o usa la del original como guía temporal) y la música. Corta todo según los tiempos de la tabla 1.
2. **Escena 1 (0–2,6 s):** fondo `#E8E8F4` + cuadrícula + estatua A1 (aparición de 0,4 a 0,9 s con *mosaic/blur → nítido*) + título con animación de **máquina de escribir** + PNG de un cursor que se mueve + hojas A6 desenfocadas en las esquinas + código de barras y fecha.
3. **Transición 1:** *slide up* (empujar hacia arriba) de 0,4 s con desenfoque de movimiento.
4. **Escena 2:** fondo negro + 2 círculos `#1F4F80` (uno con desenfoque) + tarjeta (rectángulo blanco redondeado con A2 dentro e iconos de Instagram). Animación **3D Rotate Y de 40° a 0°** + subida desde abajo a la derecha, 0,6 s *ease-out*.
5. **Transición 2:** *slide left* de 0,4 s.
6. **Escenas 3a/3b/3c:** quita el fondo de A3/A4/A5 y ponlos sobre un foco circular azul (círculo con mucho desenfoque). La píldora con borde blanco es fija y solo cambia el texto. Slide con blur entre cada artista, cada ~1,1 s.
7. **Transición 3:** zoom-in + slide up de 0,4 s.
8. **Escena 4:** degradado negro→azul + rectángulo redondeado con *desenfoque de fondo* y borde blanco al 30 % + barrido de luz. Tarjetas de comentario duplicadas cayendo con 2–3 cuadros de desfase. Después, "Par Main Hun Kon" palabra por palabra.
9. **Transición 4:** zoom-out de toda la escena al 70 % + desenfoque, y **flash blanco de 2 cuadros justo en el impacto del audio (~13,2 s)**.
10. **Escena 5:** fondo negro con overlay de grano y polvo. "I'M" empieza en 300 % de escala con blur y baja al 100 % en 1,5 s. *Slide left* con blur. "ARTIST" entra desde la derecha. Pon los créditos en las esquinas (sin las erratas del original).
11. **Todo el video:** texto vertical en los bordes desde el segundo 2,8, viñeta suave, grano al 15–25 %, y *whoosh* en cada transición.

## 7. Textos en pantalla (copia exacta del original)
```
05 DEC 2025 | RISHI KUMAR
ak ARTIST ko · Paise ke alwa · KYA CHAIYE HOTA HAI ?
Greatness is built quietly—through focus, discipline, and relentless commitment. When a person gives their best, their work naturally stands out and motivates
True impact comes from consistent effort. When someone works with vision and dedication, their actions inspire many and create a powerful ripple of positive change.
dc.kumar._ · Follow | 2.018 Likes | Virel Reel edit #stonevfx #insta
OFCOURSE USKE · KAAM KI TARIF
GREAT WORK SPEAKS BEFORE THE WORLD DOES. WHEN DEDICATION MEETS SKILL, IT INSPIRES PEOPLE, MOVES CROWDS, AND CREATES LASTING IMPACT. EVERY EFFORT, EVERY STEP, EVERY IDEA BUILDS A MOMENT WHERE EXCELLENCE STANDS AT THE CENTER—AND THE WORLD LISTEN
Fhir chahe wo · NACHNE WALA · GAANE WALA · BAJANE WALA
An artist transforms emotions into expression, turning imagination into reality. Their creativity inspires minds, connects hearts, and leaves a timeless impact through every stroke, note, or performance.
Nisha @nishren — Such a satisfying edit, everything feels balanced, clean, and very well thought out.
Par Main Hun Kon
I'M · ARTIST · Made with after effect
RISHI KUAMR · VFX ARTIST · DC.KUMAR._ · STOE VFX   (bordes: rishi kumar · @stone_vfx · Dec 2025 · Made by after effect · @dc.kumar._)
```
Cambia los nombres, los @ y las fechas por los tuyos. Este video es el trabajo de otro editor: úsalo como referencia de estilo, no lo copies tal cual.
