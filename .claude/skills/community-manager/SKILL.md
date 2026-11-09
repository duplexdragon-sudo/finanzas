---
name: "community-manager"
description: "Usar cuando Carlos pida planear o publicar contenido, escribir títulos, descripciones, hashtags o captions, responder comentarios, armar el calendario semanal o la bio, para YouTube (DuplexDragon) e Instagram: estrategia de crecimiento y comunidad con vidIQ. El contenido es 100 % Valorant."
---

# Community manager (YouTube Shorts + Instagram Reels) — 100 % Valorant

Meta: canal de alto rendimiento = **frecuencia fija + ganchos fuertes + comunidad que comenta**. Antes de decidir qué hacer, usa la skill `analista-datos-redes` para saber qué funciona.

## Identidad

- Nombre: **DuplexDragon**. Contenido: **solo Valorant**, en español. Edits estilo anime al ritmo (tipo JJK/MMV) y motion comics de las historias de los agentes, hechos con el Motor Morado (skills `motion-comic-morado`, `editor-profesional`, `ritmo-musical`).
- El contenido viejo de Minecraft no se borra (sigue sumando vistas), pero no se menciona ni se mezcla. Nada de títulos, ideas ni hashtags de Minecraft.
- Tono: épico y emocional en los edits, cercano y colombiano en captions y respuestas. Emojis justos (🔥💜⚡😢).

## Series fijas (cada una con su color de acento, ver `estetica-instagram`)

1. **Edits de agente**: un agente, una canción, al ritmo (Jett, Reyna, Yoru, Sage, Clove…).
2. **Historias / lore**: motion comic contando el pasado o la relación de un agente (Yoru, Omen, Viper-Sabine…).
3. **Agente vs agente**: rivalidades y peleas (Phoenix vs Yoru, Reyna vs Iso).
4. **Lo nuevo de Riot**: el agente, mapa o cinemática del momento, rápido (las primeras 24-48 h de un lanzamiento son la mejor ventana).

## Calendario base (ajustar con datos)

- **Shorts/Reels: 4-7 por semana** las primeras 4 semanas para reactivar el canal con el nicho nuevo. Mismo video en YouTube Shorts e Instagram Reels (sin marca de agua de TikTok/CapCut).
- Hora: la que diga `vidiq_subscriber_insights`; sin dato, 6-8 p. m. hora Colombia.
- 1 historia de IG diaria: encuesta "¿qué agente edito ahora?", avance del edit, detrás de cámaras del Motor Morado.
- 1 carrusel semanal en IG para guardados: "lore de X en 5 slides", "ranking de agentes más trágicos".
- Seguir el calendario de Riot (parches, agentes nuevos, Champions, episodios) y adelantar videos.

## Fórmula del Short/Reel

1. **Gancho 0-1 s**: el golpe más fuerte o la frase más fuerte primero, con letra grande. Nada de intros ni logos.
2. 15-30 s para edits, hasta 60 s para lore. Final que conecte con el inicio (loop).
3. Canción del momento o la que pidió la comunidad; cortes al ritmo (`ritmo-musical`).
4. CTA para comentar: "¿Qué agente sigue? 👇", "¿Team Jett o Team Reyna?".

## Títulos, descripción, hashtags

- Título: nombre del agente + emoción o conflicto, ≤ 60 caracteres antes de los hashtags. Ej.: "YORU: EL QUE NADIE QUISO 😢", "REYNA vs ISO 🔥", "JETT NO PERDONA ⚡". Revisa la ortografía siempre.
- Validar con `vidiq_score_title`, generar opciones con `vidiq_generate_titles`, palabras con `vidiq_keyword_research` ("valorant edit", "valorant lore", nombre del agente).
- Hashtags: 3-5, de específico a amplio: `#yoru #valorant #valorantedit #valorantlore #shorts` (en IG agregar `#valorantclips #anime`).
- Descripción: 1 línea con agente + canción (crédito al artista) + pregunta + enlace al IG/canal.

## Comunidad

- Responder **todos** los comentarios en las primeras 2 h (empuja el video). Usa `vidiq_video_comments` / `vidiq_comment_insights` y redacta con `vidiq_generate_comment_replies`. **Nunca publiques respuestas (`vidiq_reply_to_comment`) sin que Carlos apruebe el texto.**
- Fijar un comentario con pregunta ("¿qué agente hago mañana?") y hacer el más votado: la comunidad elige y vuelve.
- Retos 1 vez al mes (ej. "comenta tu main y edito al más pedido").
- Colaborar con creadores de Valorant de tamaño parecido (`vidiq_similar_channels`).

## Reglas de Riot

- Seguir la política de contenido de fans de Riot ("Legal Jibber Jabber"): fan content sí, pero no usar el logo de Valorant ni el de Riot como marca propia y no vender el arte oficial. El arte oficial se baja con la skill `arte-oficial-valorant`.

## Publicar

- YouTube: `vidiq_video_upload` / `vidiq_update_video` (título, descripción, tags) y `vidiq_update_video_thumbnail`.
- Instagram Reels: `vidiq_instagram_publish_reel` (requiere cuenta conectada con publishing).
- **Siempre mostrar a Carlos el título, el texto y la hora y esperar su OK antes de publicar o cambiar algo público.**

## Bio de Instagram (plantilla)

```
🐉 DuplexDragon | Edits y lore de Valorant 💜
Historias de agentes estilo anime ⚡
🎬 Nuevo edit 7 p. m. · Comenta tu main 👇
▶️ YouTube
```
Foto de perfil = la misma del canal. Enlace: YouTube. Destacados: ver skill `estetica-instagram`.
La bio, la foto y los destacados los cambia Carlos desde la app (no hay herramienta para eso). En YouTube conviene cambiar también el banner y la descripción del canal a Valorant.
