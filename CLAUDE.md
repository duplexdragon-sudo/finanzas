# Redes sociales (Instagram y TikTok)

## Skills de estrategia
`.claude/skills/` contiene las 106 skills de
[social-media-skills/skills](https://github.com/social-media-skills/skills) (licencia MIT,
ver `.claude/skills/LICENSE-social-media-skills`). Úsalas para cualquier tarea de redes:

- Empieza por `brand-profile` y `voice-builder` si aún no existe el perfil de marca.
- Crecimiento: `instagram-growth`, `tiktok-growth`, `profile-optimization`, `instagram-seo`.
- Contenido: `hook-writer`, `reels-script`, `tiktok-script`, `caption-writer`, `carousel-writer`,
  `content-calendar`, `trend-jacking`, `viral-reverse-engineering`.
- Medición y monitoreo: `analytics-and-reporting`, `goals-and-kpis`, `content-audit`,
  `competitor-analysis`.

## Conexión con Instagram (MCP `instagram`)
`.mcp.json` registra el servidor [ig-mcp](https://github.com/jlbadano/ig-mcp), que se instala
solo con `.claude/mcp/instagram/run.sh`. Lee sus credenciales de variables de entorno
(`INSTAGRAM_ACCESS_TOKEN`, `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`,
`INSTAGRAM_BUSINESS_ACCOUNT_ID`). Nunca guardes tokens en el repositorio.
En la nube, el entorno debe permitir el dominio `graph.facebook.com`.

Para métricas de TikTok y datos públicos de Instagram también está el conector vidIQ.
