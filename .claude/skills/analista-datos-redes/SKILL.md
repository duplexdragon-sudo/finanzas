---
name: "analista-datos-redes"
description: "Usar cuando Carlos pida revisar cómo van su YouTube (DuplexDragon, @duplex_dragon) o su Instagram, qué contenido funciona (100 % Valorant), por qué bajaron las vistas, mejores horarios, o un reporte de rendimiento: mide con vidIQ, compara contra su propio promedio y entrega 3 decisiones concretas."
---

# Analista de datos (YouTube + Instagram)

Objetivo: que cada decisión de contenido salga de los números de Carlos, no de corazonadas. Siempre se termina con **3 decisiones accionables**, no con una tabla suelta.

## Cuentas

- YouTube: canal **DuplexDragon** `UCYlEih7xACf_uOIzXgE-ckg` (@duplex_dragon), conectado en vidIQ con cacarrillogomez2005@gmail.com.
- Instagram: verificar con `vidiq_instagram_connected_accounts`. Si sale vacío o `public_fallback`, mostrar `vidiq_connect_instagram_account` con `mode: "oauth"` (cuenta profesional/creador) y esperar. Sin owner insights solo hay datos públicos: decirlo así.

## El contenido ahora es 100 % Valorant

Desde nov 2026 Carlos solo hace **Valorant**: edits estilo anime al ritmo y motion comics de las historias de los agentes (Motor Morado, skills `motion-comic-morado` y `editor-profesional`). Nada de Minecraft en recomendaciones, ideas, títulos ni competencia.

## Línea base medida (9 nov 2026)

- 545 suscriptores, 191 218 vistas, 34 videos. **Todo eso es del contenido viejo de memes de Minecraft** (el mejor: 33 K, POV de 10 s; último subido 15 mar 2026).
- Por eso: **no comparar los videos de Valorant contra el promedio viejo.** La línea base de Valorant empieza en cero: mediana de los primeros 10 Shorts/Reels de Valorant.
- Esperado al cambiar de nicho: los suscriptores de Minecraft no ven Valorant, así que los primeros videos tendrán menos vistas de "suscriptores" y más de "Shorts feed / explorar". Mirar fuentes de tráfico, no solo vistas.
- Lección que sí se lleva del canal viejo: lo corto (7-30 s) con gancho en el primer segundo rindió 5-20× más que lo largo.
- **Instagram @duplex_dragon (`platformAccountId` 40657586163839891, owner insights activos)**: 553 seguidores, 46 posts leídos. 20 Reels de Valorant (3 abr - 25 jun 2026); mediana ≈ 1 900 vistas.
  - Ganadores = **historias entre dos agentes / emoción**: Omen + Sage 40 375 vistas (783 compartidos, 1 352 guardados), Deadlock 13 500, Chamber + Viper 9 732. Edits de un solo agente "poderoso" ≈ 2 000.
  - Otros juegos (God of War 345, Hitman 446, RDR2 1 051) rinden menos: confirma el 100 % Valorant.
  - Último post: 25 jun 2026, justo después del mejor Reel. Volver con la parte 2 de Omen + Sage.
  - Textos reescritos de los 20 Reels: https://claude.ai/artifact/KkDWeerewJx9WkdpYibvWq Aplicados los 20 el 9 nov 2026 con `redes/subir-shorts/editar_instagram.py` (Instagram no permite editar captions por API: la herramienta usa Brave con la sesión de Carlos).
- YouTube: los Reels llevan canciones con licencia solo para Instagram; al subirlos a Shorts, Content ID los bloquea (Deadlock: "Arabella" de Arctic Monkeys, bloqueado en todo el mundo). Subir a YouTube solo el edit sin música y poner la canción desde el editor de Shorts de la app.
- Actualiza esta sección cuando haya 10 videos de Valorant nuevos (fecha arriba).

## Flujo de análisis

1. **Datos** (en paralelo):
   - `vidiq_channel_analytics` / `vidiq_channel_performance_trends` (owner: retención, fuentes de tráfico, suscriptores ganados).
   - `vidiq_channel_videos` con `videoFormat: "short"` y `popular: true` y `false` (top vs recientes).
   - `vidiq_subscriber_insights` (cuándo está conectada la audiencia).
   - Instagram: `vidiq_instagram_owner_insights` (alcance, guardados, compartidos, watch time, skip rate) o `vidiq_ig_profile_reels` si solo hay públicos.
2. **Métricas que importan** (en este orden):
   - Shorts/Reels: % que ve vs desliza (skip rate), retención media, vistas en las primeras 48 h, compartidos y guardados por cada 1 000 vistas, suscriptores por video.
   - Engagement = (likes + comentarios×3 + compartidos×5 + guardados×5) / vistas. Comentarios y compartidos pesan más que likes.
   - `breakoutScore` de vidIQ: >100 = el video superó mucho al canal; estudiar su gancho.
3. **Comparar contra el propio canal**, no contra MrBeast: mediana de los últimos 10 videos. Un video es "ganador" si dobla la mediana.
4. **Encontrar el porqué**: agrupar por formato (edit al ritmo, motion comic/lore, "agente vs agente", clip), agente, canción/género (suave, rap, phonk), duración, hora y día. Ver qué tienen en común los 3 mejores: primer segundo, texto en pantalla, audio.
5. **Competencia y tendencias**: `vidiq_outliers` y `vidiq_instagram_tiktok_outlier_search` con "valorant edit", "valorant anime edit", "valorant lore español" y el agente del video para ver qué formatos están explotando ahora; `vidiq_similar_channels` para referencias de tamaño parecido.
6. **Entregar**:
   - 3-5 líneas de diagnóstico.
   - Tabla pequeña: top 5 y peores 5 con la métrica clave.
   - **3 decisiones** ("haz más X", "deja Y", "prueba Z a las HH:MM") con la evidencia.
   - Si Carlos quiere verlo bonito: usa la skill `dataviz` y publica un artifact (dashboard).

## Reglas

- Nunca inventar números: si una herramienta no devuelve un dato, decir "no disponible".
- Mediana, no promedio (un viral distorsiona el promedio).
- Mínimo 5 videos para concluir algo de un formato; con menos es "señal", no regla.
- Revisión semanal (lunes) de los 7 días anteriores; revisión mensual con tendencias.
- Créditos vidIQ: revisa `vidiq_balance` antes de análisis grandes.
