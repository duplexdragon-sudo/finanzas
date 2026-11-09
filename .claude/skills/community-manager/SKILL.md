---
name: "community-manager"
description: "Usar cuando Carlos pida planear o publicar contenido, escribir títulos, descripciones, hashtags o captions, responder comentarios, armar el calendario semanal o la bio, para YouTube (DuplexDragon) e Instagram: estrategia de crecimiento y comunidad con vidIQ."
---

# Community manager (YouTube Shorts + Instagram Reels)

Meta: canal de alto rendimiento = **frecuencia fija + ganchos fuertes + comunidad que comenta**. Antes de decidir qué hacer, usa la skill `analista-datos-redes` para saber qué funciona.

## Identidad

- Nombre: **DuplexDragon**. Nicho principal medido: memes/POV de Minecraft en español (Colombia), humor con amigos. Línea secundaria: edits anime de Valorant del Motor Morado (skill `motion-comic-morado`).
- No mezclar los dos nichos sin plan: o una cuenta por nicho, o series fijas por día (ej. lun/mié/vie Minecraft, sáb edit Valorant). Medir 4 semanas y decidir con datos.
- Tono: cercano, colombiano, humor de "parce", emojis justos (💀😂😢).

## Calendario base (ajustar con datos)

- **Shorts/Reels: 1 al día** las primeras 4 semanas para reactivar (mínimo 4/semana). Mismo video en YouTube Shorts e Instagram Reels (sin marca de agua de TikTok/CapCut).
- Hora: la que diga `vidiq_subscriber_insights`; si no hay dato, 6-8 p. m. hora Colombia.
- 1 historia de IG diaria (encuesta, "¿cuál subo mañana?", detrás de cámaras).
- 1 carrusel semanal en IG (top 5, "tipos de amigos en Minecraft") para guardados.

## Fórmula del Short/Reel

1. **Gancho 0-1 s**: texto grande en pantalla con el conflicto ("POV: tu amigo encuentra tu base secreta"). Nada de intros.
2. 7-30 s (los mejores del canal miden 10-29 s). Final que conecte con el inicio para que se repita (loop).
3. Audio en tendencia o el que funcionó antes.
4. CTA con pregunta para comentar: "¿Cuál es tu amigo? 👇".

## Títulos, descripción, hashtags

- Título: MAYÚSCULAS en la frase clave, formato POV / "MI AMIGO VS YO" / "CUANDO…", ≤ 60 caracteres antes de los hashtags. Revisa ortografía (ojo: "miniecraft" en vez de "minecraft", "ENCUTRAS", "CARME" aparecen en títulos viejos y restan credibilidad y búsquedas).
- Validar con `vidiq_score_title` y generar opciones con `vidiq_generate_titles`; palabras con `vidiq_keyword_research`.
- Hashtags: 3-5, de específico a amplio: `#minecraft #minecraftmemes #minecraftespañol #humor #shorts`. Mantener `#miniecraftdelflow` solo si es la marca de la serie (escrito siempre igual).
- Descripción: 1 línea con palabras clave + pregunta + enlace al IG/canal.

## Comunidad

- Responder **todos** los comentarios en las primeras 2 h (empuja el video). Usa `vidiq_video_comments` / `vidiq_comment_insights` y redacta con `vidiq_generate_comment_replies`. **Nunca publiques respuestas (`vidiq_reply_to_comment`) sin que Carlos apruebe el texto.**
- Fijar el mejor comentario o una pregunta.
- Retos y "comenta X" funcionaron (el sorteo de Roblox sacó 16 comentarios): repetir 1 vez al mes.
- Usar comentarios como ideas de próximos videos.

## Publicar

- YouTube: `vidiq_video_upload` / `vidiq_update_video` (título, descripción, tags) y `vidiq_update_video_thumbnail`.
- Instagram Reels: `vidiq_instagram_publish_reel` (requiere cuenta conectada con publishing).
- **Siempre mostrar a Carlos el título, el texto y la hora y esperar su OK antes de publicar o cambiar algo público.**

## Bio de Instagram (plantilla)

```
🐉 DuplexDragon | Memes de Minecraft 🇨🇴
POV que te pasaron con tus amigos 💀
🎬 Nuevo Reel todos los días 7 p. m.
👇 YouTube
```
Foto de perfil = la misma del canal (consistencia). Enlace: YouTube. Destacados: ver skill `estetica-instagram`.
La bio, la foto y los destacados los cambia Carlos desde la app (no hay herramienta para eso).
