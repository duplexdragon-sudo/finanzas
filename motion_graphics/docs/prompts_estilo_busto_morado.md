# Estilo "busto morado editorial": ingeniería inversa y prompts para Gemini

## 1. Qué tiene la imagen (medido)

| Elemento | Cómo es |
|---|---|
| **Sujeto** | Busto de mármol clásico (un filósofo barbudo), de **3/4**, mirando a la derecha, cortado a la altura del pecho. Muy detallado (rizos, pliegues de la toga) |
| **Color** | **Monocromo morado (duotono)**: sombras violeta muy oscuro `#342043`, medios violeta `#8953AB` → `#AA53FA`, luces lila casi blanco `#E0D6F1` / `#FADAFF` |
| **Fondo** | Gris muy claro `#EAEAEA` → `#F5F3F6`, con una **textura sutil de mármol o líquido** en tono gris |
| **Luz** | Luz de estudio suave desde la izquierda arriba, con mucho contraste en los detalles y brillos lilas |
| **Base** | La parte de abajo del busto **se funde con el fondo** (degradado a blanco) |
| **Profundidad** | Mariposas moradas: unas nítidas y otras **muy desenfocadas en primer plano** (bokeh) |
| **Diseño** (lo agrego yo, no Gemini) | Dos **barras verticales moradas** `#A44DF3` detrás del busto, texto gigante condensado `#8D38DC` y adornos de UI |

**Clave del estilo:** foto realista y muy detallada **convertida en duotono morado**, sobre fondo claro, con la base desvanecida. Las barras, los textos y las mariposas desenfocadas los pongo yo en el video. **A Gemini pídele solo el objeto.**

---

## 2. Prompt base (cópialo y cambia solo lo que está entre [corchetes])

```
Hyperrealistic studio photograph of [OBJETO], [ÁNGULO], centered with generous margin, the whole object visible.
Monochrome purple duotone color grading: deep violet shadows (#342043), rich violet midtones (#8953AB to #AA53FA), soft lilac-white highlights (#F1EAFB). No other colors.
Pure light grey background (#EDEDF0), completely plain, with the bottom of the object softly fading into the background.
Soft studio lighting from the upper left, crisp micro-details, high contrast in the textures, subtle film grain, editorial poster aesthetic, 8K, ultra sharp.
No text, no letters, no logos, no watermark, no frame, no extra objects.
```
**Formato:** pide **vertical 4:5 o 9:16**. Si Gemini te deja elegir, la máxima resolución.

> Si sale con fondo con textura o con otros elementos, agrega al final: `isolated object only, empty plain background`.

---

## 3. Prompts listos por objeto (sección B de la lista)

Cada uno ya trae el ángulo. Pega el **prompt base** y reemplaza `[OBJETO], [ÁNGULO]` por lo que dice aquí:

| # | Archivo | Reemplaza `[OBJETO], [ÁNGULO]` por |
|---|---|---|
| 17a | `17_rey_ajedrez.png` | `a polished marble chess king piece, three-quarter view slightly from below` |
| 17b | `17_caballo_ajedrez.png` | `a marble chess knight piece, side three-quarter view` |
| 17c | `17_reina_ajedrez.png` | `a marble chess queen piece, three-quarter view` |
| 18 | `18_corona.png` | `an ornate royal crown with engraved details and gems, three-quarter view from slightly above` |
| 19 | `19_reloj_arena.png` | `an antique hourglass with sand falling, front view` |
| 20 | `20_ojo.png` | `a hyperrealistic human eyeball with detailed iris, front view, slightly turned` |
| 21 | `21_cerebro.png` | `a realistic human brain sculpture, side three-quarter view` |
| 22 | `22_dados.png` | `two marble dice mid-air, tilted, showing different faces` |
| 23 | `23_rompecabezas.png` | `a single glossy 3D puzzle piece, isometric view` |
| 24 | `24_diamante.png` | `a large brilliant-cut diamond, three-quarter view from above` |
| 25 | `25_columna.png` | `a classical Corinthian marble column, full height, front view` |
| 25b | `25_busto.png` | `a classical marble bust of a bearded philosopher, three-quarter view facing right, cropped at the chest` |
| 26a | `26_mouse.png` | `a sleek gaming mouse, three-quarter top view` |
| 26b | `26_teclado.png` | `a mechanical gaming keyboard, angled three-quarter view` |
| 27 | `27_audifonos.png` | `over-ear gaming headphones with microphone, three-quarter view` |
| 28 | `28_monitor.png` | `a gaming monitor on a stand, screen off, three-quarter view` |
| 29 | `29_medalla.png` | `a winner medal with ribbon, front view` |
| 30 | `30_rayo.png` | `a stylized lightning bolt sculpture made of glossy marble, front view` |
| 31 | `31_cadena_rota.png` | `a heavy metal chain breaking apart in the middle, links flying, side view` |
| 32 | `32_brujula.png` | `an antique brass compass, open, top three-quarter view` |
| 33 | `33_mariposa.png` | `a single butterfly with wings open, top view` |
| 34 | `34_mano_estatua.png` | `a marble statue hand reaching forward, open palm, three-quarter view` |
| 35 | `35_alas.png` | `a pair of marble angel wings, front view, symmetrical` |

**Ejemplo completo (corona):**
```
Hyperrealistic studio photograph of an ornate royal crown with engraved details and gems, three-quarter view from slightly above, centered with generous margin, the whole object visible.
Monochrome purple duotone color grading: deep violet shadows (#342043), rich violet midtones (#8953AB to #AA53FA), soft lilac-white highlights (#F1EAFB). No other colors.
Pure light grey background (#EDEDF0), completely plain, with the bottom of the object softly fading into the background.
Soft studio lighting from the upper left, crisp micro-details, high contrast in the textures, subtle film grain, editorial poster aesthetic, 8K, ultra sharp.
No text, no letters, no logos, no watermark, no frame, no extra objects.
```

---

## 4. Objetos de Valorant (sección A): **no los generes en Gemini**

Las armas, la Spike, los agentes y los logos son diseños de Riot. Si se los pides a Gemini, sale una copia deformada y además es copiar su diseño. Es mejor así:
1. **Agentes, íconos y cartas:** los bajo yo de la API oficial de Riot. Dime qué agentes.
2. **Armas, Spike, escudos y rangos:** también salen de la API oficial (`valorant-api.com`, que ya tengo habilitado), o súbelos tú.
3. **Yo les aplico este mismo estilo** (duotono morado, base desvanecida y fondo claro) con código. Así quedan iguales a los de Gemini y conservan el diseño original.

### Si tienes una foto y quieres pasarla al estilo dentro de Gemini (edición de imagen)
Sube la foto a Gemini y escribe:
```
Recolor this image into a monochrome purple duotone: deep violet shadows (#342043), violet midtones (#8953AB to #AA53FA), lilac-white highlights (#F1EAFB). Keep every detail and the exact shape. Replace the background with plain light grey (#EDEDF0) and softly fade the bottom of the object into it. No text, no watermark.
```

---

## 5. Cómo me los mandas
- PNG o JPG con el nombre de la tabla (`18_corona.png`…), mínimo **1500 px**.
- **Súbelos como archivo** (igual que las coronas).
- Yo los recorto, les quito el fondo gris, ajusto todos al mismo tono exacto y los animo.
