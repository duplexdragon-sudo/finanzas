# Estructura base de un video de noticia (modelo: Cloud9, nov 2026)

Este es el formato aprobado por Carlos: **limpio, sin superposiciones, con jugadas reales y animaciones**.
Todo video de noticia nuevo parte de `motion_graphics/render/render_c9.py`: se copia, se cambian los recursos y el guion, y se conserva esta estructura.

**Datos técnicos:**
- Duración: unos 60–65 s.
- Formato: vertical 720×1280 a 30 fps, exportado a 1080×1920.
- Escenas: 11 (L0–L10), una por frase del guion (`guion.json`).
- Cada escena empieza con un barrido morado y un pequeño zoom de entrada.

## Línea de tiempo

| Escena | Tiempo aprox. | Fondo | Qué pasa | Recursos |
|---|---|---|---|---|
| **L0 · Gancho** | 0–4,7 s | Morado ↔ blanco, 4 escenas de ~1 s con flash lila | Se ve a los **jugadores primero**: tarjetas iguales en grilla 2×2 con su **símbolo de rol volando** → "AFUERA" con el logo tachado → nombre del equipo con 2 jugadores grandes y "ROSTER NUEVO" → "DESDE ABAJO" con el logo subiendo y las habilidades girando | `card(same())`, `rolefly`/`badge`, `stamp`, `c9orb` |
| **L1 · Frase emocional** | 4,7–9 s | Blanco con cuadrícula | Frase en cursiva + palabra grande con `slam` + cinta | `word`, `slam`, `ribbon` |
| **L2 · Contexto con fecha** | 9–16 s | Blanco | El **calendario pasa hojas** hasta el mes del hecho → contador grande + etiqueta → chip ✗ del equipo | `calflip`, `counter`, `chipx` |
| **L3 · Otros afectados** | 16–21 s | Blanco con rayas | Chips rojos ✗ que entran uno por uno + sello | `chipx`, `stamp` |
| **L4 · Giro** | 21–27 s | Morado | Titular (`slam`) + etiqueta + logo con habilidades girando | `slam`, `nchip`, `c9orb` |
| **L5 · Presentación del roster** | 27–34 s | Alterna morado y blanco por jugador | **Cada jugador con su jugada real**: nombre grande + rol arriba, tarjeta de la jugada (arma y HUD completos), foto abajo a la izquierda y símbolo de rol abajo a la derecha. Flash entre jugadores. Al final, **grilla de los 5** con rol, nombre y coach | `gclip`, `rolefly`, `badge`, grilla |
| **L6 · Los que se fueron** | 34–38 s | Blanco | Foto del jugador + chip + logo del nuevo equipo | `pop`, `nchip` |
| **L7 · Dato histórico** | 38–43 s | Morado | Contador de años (2026→2023) + sello "HACE 3 AÑOS" | `counter`, `stamp` |
| **L8 · Resultado** | 43–50 s | Blanco | "DEBUT PERFECTO" + chips ✓ con marcadores + sello + confeti | `chipx(ok)`, `stamp`, `confetti` |
| **L9 · Próximo partido** | 50–56 s | Morado | El calendario pasa a la fecha → cinta de la fecha + "C9 vs RIVAL" + sello del objetivo | `calflip`, `ribbon`, `slam`, `stamp` |
| **L10 · Cierre / CTA** | 56–63,5 s | Blanco | Pregunta ("¿… vuelve a LO MÁS ALTO?") → ícono de **comentar** → ícono de **compartir** ("compártelo con ese amigo fan de…") + logo con habilidades + banda de fuentes | `U.COMMENT`, `U.SHARE`, `c9orb` |

## Guion (11 frases, voz Andrés a 1,1×)
1. **Gancho:** quién y qué pasó, en una frase con los nombres.
2. **Frase emocional** o metáfora.
3. **Contexto** con fecha y cifra.
4. **Otros afectados.**
5. **El giro:** qué hizo el equipo.
6. **El roster nombre por nombre**, con el coach al final.
7. **Los que se fueron.**
8. **Dato histórico.**
9. **Resultado reciente.**
10. **Lo que viene**, con fecha y rival.
11. **CTA:** pregunta + "te leo en los comentarios… y compártelo con ese amigo fan de…".

## Audio
- **Voz:**
  - ElevenLabs con `/with-timestamps`.
  - `loudnorm` a −15.
  - Cada corte cae en la palabra exacta con `wt(frase, "palabra")`.
- **Música:**
  - La que mande Carlos (Cloud9: `audio/musica/c9_tiktok.mp3`, 161 BPM, con un *drop* en el segundo 30 que coincide con el roster).
  - Si es más corta que el video, se alarga repitiendo la última sección con `acrossfade`.
  - Se ajusta el volumen según los LUFS de la canción: con −14 LUFS va a 0,34, y con −10 LUFS a 0,2.
  - Va comprimida con *sidechain* bajo la voz.
- **Efectos:**
  - braam + hit808 al inicio;
  - swoosh en cada cambio de escena;
  - hit808 + glitch en los golpes;
  - pop en cada jugador o ícono;
  - shimmer y cheer en las victorias.
- **Volumen final:** −13 a −14 LUFS.

## Recursos que pide Carlos para cada video
- Fotos de los jugadores (PNG, que se recortan con rembg).
- Logo del equipo.
- Ícono oficial de cada rol (ya guardados en `motion_graphics/roles/`).
- **Una jugada por jugador** de 3 a 5 s (los TikTok de jugadas sirven). Se recorta el área de juego **completa, con el arma y el HUD**, por debajo del texto quemado del clip original.
- La música.

## Antes de entregar
1. Revisor de texto con 0 choques.
2. 0 tramos quietos.
3. Volumen entre −13 y −14 LUFS.
4. Inventario: todo el material usado.

**Revisar también:**
- que cada jugada sea del jugador correcto (ej.: **Derke ≠ Derrek**);
- la portada en 4K y 4:5;
- la descripción para IG.
