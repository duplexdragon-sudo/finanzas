# Reglas de Carlos (@DuplexDragon_) para los videos de Valorant

Estas reglas salen de las correcciones que Carlos hizo video tras video. Se cumplen **siempre**, sin que él tenga que repetirlas.
El código vive en `motion_graphics/` y la guía técnica completa está en `APRENDIZAJE_MOTION.md`.
**Estructura base de todo video de noticia:** `motion_graphics/docs/ESTRUCTURA_VIDEO_NOTICIA.md`, que toma como modelo `render/render_c9.py`.

## 1. Antes de entregar (obligatorio)
Ningún video se manda sin pasar estas 4 revisiones:

1. **Revisor de texto:** `python3 revisor_texto.py render_<proyecto> 4` debe dar **`CHOQUES: 0`**.
   - Recorre el video cuadro a cuadro y marca en rojo (`revisor_texto.jpg`) cualquier texto que toque otro texto, una cara, un logo o **un clip de jugada**.
2. **Tramos quietos:** `python3 quietos.py <video>` debe dar **0 tramos quietos**.
3. **Volumen:** `ebur128` entre **−13 y −14 LUFS**.
4. **Material:** `python3 inventario.py` debe confirmar que **todo** lo que mandó Carlos (fotos, logos, clips) está usado.
   - Cuando se hacen varios videos a la vez se olvidaban cosas; esto lo evita.

Además, hay que mirar la hoja `--preview` de **todo** el video (unos 48 cuadros) antes del render final.

## 2. Texto y composición
- **Nada se superpone:** ni textos entre sí, ni textos sobre caras, ni logos sobre títulos. Si no cabe, se pasa a otra escena o se anima en dos tiempos.
- **Centrado** horizontal y vertical. Los textos no pasan de 580 px de ancho (lienzo de 720).
- Se respeta la **zona segura de TikTok e IG**: función `SY()`, 120 px arriba y lejos de los botones de la derecha y del pie.
- Los nombres van **debajo de la cara** (en el pecho), nunca encima.
- El **agente de Valorant** siempre va **delante** del texto.
- **El agente nunca tapa el título:** va debajo del título (más chico si hace falta), con la cabeza completa dentro del cuadro.
- **Nada de letras fantasma** (texto gigante con contorno de fondo) detrás de un agente o encima de un clip de jugada.
- Revisar la **ortografía** de cada texto en pantalla, con tildes y nombres bien escritos (GLYPH, nightz, FireBallOps…).
- **Estética:**
  - Morado `(115, 16, 165)` con letra blanca, o blanco con cuadrícula y letra morada.
  - Fuentes: Anton para títulos, Playfair Italic para las frases, Montserrat/Oswald para las etiquetas.
  - Nada de neón.
- **Logos sobre fondo morado:** van en **colores invertidos** (disco blanco con el símbolo en morado) para que se vean.
- Las tarjetas o fotos que van en grupo tienen **el mismo tamaño**: se recortan al mismo formato con `same()`.

## 3. Gancho (primeros 3 a 5 s)
- **Empieza con el tema:** los jugadores o el equipo primero, para que la gente sepa de qué se habla. Nunca abrir con un calendario o un dato suelto.
- Se arma como en la ingeniería inversa (`docs/ingenieria_inversa_video3_motion.md`):
  - escenas de **~1 s**, alternando morado y blanco con **flash** en cada corte;
  - cada corte cae en la **palabra exacta** de la voz, con su golpe de sonido;
  - objetos grandes que entran con *pop*.
- Nunca una pantalla quieta, y ningún cuadro feo o borroso.

## 4. Recursos gráficos que siempre se usan
- **Habilidades de Valorant girando** alrededor del logo o de la persona (`player_orbit`).
- **Logo del equipo** en el gancho y en el cierre.
- **Animación de calendario** (`calflip`) para fechas.
- Contadores, sellos, cintas y chips con ✓ o ✗.
- **Símbolo de rol** sobre cada jugador (duelista, iniciador, centinela, controlador), con los íconos oficiales que están en `motion_graphics/roles/`.
  - Entran volando y aterrizan sobre la persona.
  - Si el rol **no está confirmado** por una fuente, va el logo del equipo y no se inventa.

## 5. Noticias y guion
- **Todo se verifica en la web** (vlr.gg, Liquipedia, THESPIKE, Sheep Esports, la cuenta oficial del equipo). Si no es oficial, se dice **"según reportes"**. Nunca se inventa.
- Si Carlos manda clips, **revisar que cada jugada sea del jugador correcto** antes de usarla.
- **Cada clip tiene que mostrar exactamente lo que dice la voz en ese momento.** Antes de montar, se revisa cada clip segundo a segundo (hoja con tiempos) y se anota en qué segundo aparece cada habilidad o jugada; el clip arranca justo ahí.
- **El clip aparece desde que empieza la escena** (nunca un hueco vacío) y se sincroniza para que la habilidad caiga justo en la palabra (`synclip`). Si la escena dura más, se repite solo la ventana de la habilidad, sin mostrar otras cosas del clip.
- Si un clip trae varias partes (por ejemplo el video oficial de Riot con una sección por habilidad), cada escena usa **solo su sección**: nunca se cuela la intro, la clasificación por edades ni otra habilidad (`SECT` en `synclip`).
- **Guías de agentes:** se explica **tecla por tecla** (teclas por defecto: F, C, Q, E, X, clic izquierdo y derecho, espacio). Las teclas aparecen una por una debajo del clip, justo cuando la voz las dice.
- Antes de entregar se revisa el video final cada medio segundo, escena por escena, para confirmar que lo que se ve coincide con lo que se dice.
- La voz es Andrés (ElevenLabs, eleven_v4) a 1,1×, y el guion tiene frases cortas.
- Fuentes en una banda al final. Se cierra con una pregunta para comentar y la @DuplexDragon_.
- Cada entrega incluye:
  - el video final comprimido (`*_final.mp4`);
  - la portada para IG en 4K y en 4:5 (`portada_tpl.py`);
  - la descripción para IG, TikTok y Shorts según `docs/REDES_SOCIALES.md` (**máximo 5 hashtags**).

## 5b. Videos de League of Legends
- **Cuando Carlos pida un video de LoL, siempre se pone la marca de agua XE** (`motion_graphics/marcas/marca_xe.png`) en **todo** el video, arriba a la derecha: blanca sobre morado y morada sobre blanco.
- **Los videos de Valorant son 100 % de Carlos:** llevan solo @DuplexDragon_, **sin** la marca XE.
- **Logos de equipos en pantalla (no solo en el anillo):** siempre en los colores de la marca: **morado sobre fondo blanco y blanco sobre fondo morado**; nunca en sus colores originales.
- **Anillo que gira en LoL:** logos de los equipos que participan, en un solo color (blanco sobre morado, morado sobre blanco), nunca círculos ni bolas.
- **Tarjetas de jugadores:** recortadas centradas en la cabeza (`headcrop`), para que todas las caras queden del mismo tamaño.
- **Objetos recortados** (la copa, por ejemplo): silueta sólida y centrada; si la foto tiene un fondo difícil, se pide una con fondo liso.
- Los nombres de equipos se dicen **en inglés**. En la voz se escriben fonéticamente ("Yen Yi", "Ti Uan", "Janwa Laif", "Di Plas Kía", "Bilibili Guéiming") y en pantalla van bien escritos.
- En lugar del símbolo de rol va la **posición** (TOP/JG/MID/ADC/SUP).

## 5c. Videos de homenaje (personas reales que fallecieron)
- Verificar todo con fuentes oficiales (Riot, wiki, medios). **No se menciona la causa de muerte** si no es pública, y no se especula.
- Tono respetuoso: la primera parte puede ser alegre (el meme o el legado); desde el fallecimiento, el fondo va oscuro, la música baja y no hay golpes fuertes.
- Si hay audio original de la persona, va al inicio con la etiqueta "AUDIO ORIGINAL".
- Se da crédito al clip original y se cierra invitando a recordarla en los comentarios.

## 8. Redes sociales (Claude como social media manager de Carlos)
- Toda descripción sigue `motion_graphics/docs/REDES_SOCIALES.md`. El orden es fijo:
  1. gancho de una línea con palabra clave;
  2. contexto;
  3. lista de valor;
  4. un solo llamado a la acción;
  5. créditos;
  6. hashtags.
- **Máximo 5 hashtags**, siempre con **#DuplexDragon**, y nada de #fyp, #viral ni #parati.
- Se entregan versiones para **Instagram, TikTok y YouTube Shorts**.

## 7. Guardar siempre
- Carlos pidió que **cada regla o corrección nueva se guarde siempre**: se agrega a este archivo y se sube a GitHub (commit + push a la rama de trabajo), sin esperar a que lo pida otra vez.

## 6. Material de Carlos
- Las imágenes pegadas en el chat a veces llegan solo como vista previa. Si no hay archivo, hay que pedírselas como **adjunto 📎**.
- Usar **todo** el material recibido.
- **Nunca subir a GitHub videos, audios pesados, claves ni tokens.**
