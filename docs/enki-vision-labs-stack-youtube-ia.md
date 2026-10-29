# Enki Vision Labs — Stack de herramientas y estrategia para un canal de YouTube con IA

**Nicho:** negocios con IA · IA aplicada a empresas · finanzas personales apoyadas en IA
**Fecha de la investigación:** 29 de octubre de 2026
**Método:** búsqueda web del 29/10/2026. Casi todos los precios proceden de **sitios comparadores de terceros** (las páginas oficiales de YouTube/Google Help y algunos medios estaban bloqueados por la red de esta sesión). Por eso cada precio lleva su fuente y debe confirmarse en la web oficial antes de pagar. Lo que no se pudo verificar va marcado como **[sin verificar]**.

> **Supuestos (rellenaste el formulario con los corchetes vacíos).** He trabajado con estos valores por defecto; cámbialos en las preguntas finales y ajusto todo:
> - Idioma: **español neutro** (con expansión a inglés y portugués mediante doblaje).
> - Mercado: **Latinoamérica + EE. UU. hispano**.
> - Formato: **ambos** → 2–3 vídeos largos (8–15 min) + 5–7 Shorts por semana.
> - Presupuesto: **≈ USD 300/mes**.
> - Nivel técnico: **básico‑intermedio** (sin programador dedicado).
> - Cámara: **faceless con voz IA**; avatar solo como recurso puntual (ver riesgos: **no** usar un avatar que se presente como "asesor financiero").

---

## 1. Resumen ejecutivo

1. **La regla que manda en 2026:** desde el 16‑jul‑2026 YouTube excluye de la monetización tres tipos de contenido "inauténtico": genérico/repetitivo o de plantilla, contenido insatisfactorio o perturbador, y **personas de IA que hablan de temas sensibles, incluida la financiera** ([TechRepublic](https://www.techrepublic.com/article/news-youtube-ai-video-monetization-rules/), [Tubefilter](https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/)). Que una voz IA narre una explicación financiera bien investigada **está permitido**; un avatar IA que se presente como asesor acreditado **no** lo está ([resumen](https://creatorblade.com/blog/youtube-inauthentic-content-policy-2026-stay-monetized)).
2. Por eso el stack está pensado para un **"faceless con criterio editorial"**: guion propio con datos verificados, voz consistente de marca, gráficos originales y una "persona" de canal declarada como IA, nunca como asesor.
3. **Stack recomendado (~USD 300/mes):** Claude Pro o ChatGPT Plus (guion) + Perplexity/NotebookLM (verificación) · ElevenLabs Creator (voz) · Descript (edición) + CapCut (Shorts) · Google AI Pro/Flow (b‑roll Veo) · Midjourney + Canva Pro (imágenes y miniaturas) · Epidemic Sound (música con Content ID) · vidIQ + 1of10 (ideas y outliers) · OpusClip (largo → Shorts) · Make (automatización) · Metricool (publicación) · auto‑doblaje nativo de YouTube (gratis).
4. Capacidad estimada: **3 largos + 7 Shorts/semana** con 1 persona a ~20–25 h/semana.
5. La monetización real del nicho está **fuera de AdSense**: afiliados de herramientas de IA, newsletter y producto digital propio (plantillas/prompts/cursos).

---

## 2. Tablas por categoría

Leyenda: **Español** = calidad para crear en español (1–5, valoración propia del equipo basada en el soporte de idioma, no en un benchmark). Precios en USD/mes salvo que se indique; "anual" = facturación anual.

### 2.1 Investigación de nicho y tendencias

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia comercial | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| Google Trends | Demanda por país/tema, comparativas, YouTube Search | Gratis [sin verificar en 2026] | Sí | 5 | N/A | Datos de Google por país LATAM | No da volumen absoluto | https://trends.google.com |
| vidIQ | Keywords, ideas diarias, competidores, IA de títulos | ~7,50–39 $/mes; Boost ~16,58 $/mes anual (ago‑2026) ([Toolradar](https://toolradar.com/compare/vidiq-vs-tubebuddy), [OutlierKit](https://outlierkit.com/resources/youtube-tool-pricing/)) | Sí (150 créditos IA/mes) | 4 | N/A | Muy completo, integrado en YouTube | Datos de volumen aproximados | https://vidiq.com/pricing |
| 1of10 | Buscador de vídeos "outlier" (que superan la media del canal) | Basic 29 $/mes, Pro 69 $/mes (2026) ([OutlierKit](https://outlierkit.com/resources/youtube-tool-pricing/)) | Sí (búsqueda de outliers) | 3 | N/A | El mejor para encontrar formatos que ya funcionan | Más útil en inglés | https://1of10.com |
| TubeBuddy | SEO, A/B, plantillas de descripciones | Pro 43,20 $/año; Legend 278,28 $/año; 50 % desc. <1.000 subs (2026) ([1of10](https://1of10.com/blog/tubebuddy-pricing-review/)) | Sí | 4 | N/A | Muy barato | Solapa con vidIQ | https://www.tubebuddy.com/pricing |
| Exploding Topics | Tendencias emergentes antes del pico | Pro desde 39 $/mes anual (2026) ([Exploding Topics](https://explodingtopics.com/blog/exploding-topics-pro-vs-free)) | Sí (limitado) | 2 | N/A | Detecta temas de IA y fintech temprano | Sesgo EE. UU./inglés | https://explodingtopics.com |
| AnswerThePublic | Preguntas reales de búsqueda | Desde ~11–13 $/mes (2026) ([Toolsurf](https://www.toolsurf.com/best-answer-the-public-alternatives-in-2025-top-tools-for-discovering-what-people-search-for-group-buy-2026-premium-access-for-just-0-99/)) | Sí (pocas búsquedas/día) | 4 | N/A | Ideal para guiones "cómo/por qué" | Datos de Google, no de YouTube | https://answerthepublic.com |
| ViewStats | Analítica de outliers y miniaturas (MrBeast) | **[sin verificar]** | **[sin verificar]** | 3 | N/A | Buen análisis de miniaturas | Precio no confirmado | https://www.viewstats.com |

### 2.2 Ideación y guiones (LLMs + verificación)

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| Claude Pro | Guiones largos con estructura y tono | 20 $/mes (may‑2026) ([eWeek](https://www.eweek.com/news/ai-pricing-cheat-sheet-2026/)) | Sí | 5 | Sí (el output es tuyo, según términos) | Redacción natural en español; Proyectos con tu "biblia de estilo" | Límites de uso en horas pico | https://claude.com/pricing |
| ChatGPT Plus | Guiones, ideas, imágenes y análisis de datos | 20 $/mes (may‑2026) ([eWeek](https://www.eweek.com/news/ai-pricing-cheat-sheet-2026/)) | Sí | 5 | Sí | Todo en uno (imagen, datos, GPTs) | Tiende al estilo "genérico" si no se le guía | https://chatgpt.com/pricing |
| Gemini (Google AI Pro) | Guiones + Deep Research + incluye Flow/Veo | 19,99 $/mes con 1.000 créditos Flow (2026) ([diyai](https://diyai.io/ai-tools/video-generation/google-veo-pricing/)) | Sí | 5 | Sí | Un pago cubre LLM + vídeo | Créditos Flow se agotan rápido | https://gemini.google |
| Perplexity | Verificación de datos con fuentes citadas | **[sin verificar]** (Pro históricamente ~20 $/mes) | Sí | 5 | N/A | Cita fuentes: clave para YMYL | Puede citar fuentes de baja calidad | https://www.perplexity.ai |
| NotebookLM | Guion basado SOLO en tus fuentes (informes, leyes fiscales) | Gratis (con cuenta Google) [sin verificar límites 2026] | Sí | 5 | N/A | Reduce alucinaciones en datos financieros | No navega la web por sí solo | https://notebooklm.google |

> Para cifras financieras, la regla es: **ningún dato numérico sale en el vídeo sin una fuente primaria enlazada** (banco central, regulador, informe oficial). Los LLM redactan; las fuentes se verifican a mano.

### 2.3 Voz en off / clonación

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| ElevenLabs | TTS, clonación profesional, doblaje | Starter ~5–6 $; Creator ~22 $ (~100–121k créditos); Pro 99 $ (2026) ([bigvu](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/), [magichour](https://magichour.ai/blog/elevenlabs-pricing)) | Sí (sin uso comercial) | 5 | Desde Starter | La voz más natural en español y acentos LATAM | Créditos se consumen rápido en vídeos largos | https://elevenlabs.io/pricing |
| Voz nativa de Google/Gemini TTS, Azure, etc. (vía API) | TTS barato a escala | Por uso **[sin verificar]** | Créditos de prueba | 4 | Sí (según términos del proveedor) | Muy barato para automatizar | Menos expresivo; requiere técnico | — |
| Descript (Overdub/AI voices) | Voz dentro del editor | Incluido en planes Descript (ver 2.8) | Sí | 3 | Sí | Corriges el guion y la voz se regenera | Español menos natural que ElevenLabs [valoración propia] | https://www.descript.com/pricing |
| Tu propia voz + limpieza IA (Descript Studio Sound / Adobe Podcast) | Locución humana con calidad de estudio | Desde gratis | Sí | 5 | Sí | **Máxima autenticidad para YPP** | Requiere grabar | https://podcast.adobe.com |

### 2.4 Avatares y presentadores IA

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| HeyGen | Avatar propio (clon) o de stock, traducción con lip‑sync | Creator 29 $/mes (24 $ anual); Pro 99 $; Business 149 $ (2026) ([Arcade](https://www.arcade.software/post/heygen-pricing)) | Sí (3 vídeos con marca de agua) | 4 | Planes de pago | Mejor relación calidad/precio | Sistema de créditos desde 2026 | https://www.heygen.com/pricing |
| Synthesia | Avatares corporativos | Starter 29 $ (18 $ anual, 10 min); Creator 89 $ (64 $ anual, 30 min) (jul‑2026) ([Creatify](https://creatify.ai/blog/synthesia-pricing-(2026)-plans-credits-and-what-you-ll-actually-pay)) | Sí (~10 min) | 4 | Planes de pago | Muy estable y "seguro" | Estética corporativa, menos YouTube | https://www.synthesia.io/pricing |
| Captions / Creatify / otros | Avatares para Shorts publicitarios | **[sin verificar]** | — | 3 | — | Rápidos para UGC | Riesgo de "plantilla" | — |

> ⚠️ **Uso recomendado:** solo para segmentos (p. ej. tu propio clon presentando la intro) y **nunca** como "experto financiero" ficticio. Si usas avatar, márcalo como contenido sintético y no le atribuyas credenciales.

### 2.5 Generación de vídeo IA (b‑roll, escenas)

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| Google Veo (vía Flow) | B‑roll realista con audio | AI Pro 19,99 $ (1.000 créditos); Ultra 99,99–199,99 $ (2026) ([diyai](https://diyai.io/ai-tools/video-generation/google-veo-pricing/)) | Sí (créditos diarios) [sin verificar cantidad] | 4 (prompts en español OK) | Sí, según términos de Google | Calidad top; incluido en Gemini | Clips cortos; créditos caros | https://labs.google/flow |
| Kling AI | B‑roll, movimiento de cámara | Standard desde 6,99 $ (promo); Ultra 180 $ (2026) ([Coverr](https://coverr.co/de/blog/runway-vs-sora-vs-veo-3-1-vs-kling-pricing-2026)) | Sí (con marca de agua) | 3 | Planes de pago | Muy barato por clip | Cambia precios a menudo | https://klingai.com |
| Runway | Edición generativa + acceso a varios modelos (Veo, Kling…) | Desde 12–15 $/mes (2026) ([Rangy](https://rangy.ai/blog/veo-vs-kling-vs-runway)) | Sí (limitado) | 3 | Planes de pago | Muchos modelos con un solo pago | Créditos se agotan | https://runwayml.com/pricing |
| Motion graphics propios (Canva / After Effects / Jitter) | Animar gráficos financieros | Ver 2.6 | Sí | 5 | Sí | **Más original y más barato** que IA de vídeo | Requiere plantilla inicial | — |

### 2.6 Imágenes y gráficos

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| Midjourney | Ilustraciones de alta calidad, estilo de marca | Basic 10 $; Standard 30 $; Pro 60 $; Mega 120 $ (may‑2026) ([gptprompts](https://gptprompts.ai/midjourney-pricing)) | No | 3 (prompts mejor en inglés) | Sí en planes de pago (Pro/Mega si facturas >1M $/año) [sin verificar umbral 2026] | Estética superior y consistente | Texto en imagen mejorable | https://www.midjourney.com |
| ChatGPT / Gemini (Nano Banana) imágenes | Imágenes con texto legible, edición | Incluido en planes LLM | Sí | 5 | Sí | Texto en español bien escrito | Menos "artístico" | — |
| Canva Pro | Infografías, miniaturas, plantillas | 15 $/mes (~10 $ anual) (may‑2026) ([Stacksheriff](https://stacksheriff.com/ai-tools/ai-tool-stack-creators-2/)) | Sí | 5 | Sí (revisar licencia de elementos) | Todo el equipo puede usarlo | Diseños "vistos" si no personalizas | https://www.canva.com/pricing |
| Datawrapper / Flourish | Gráficos financieros limpios y exactos | Gratis para uso público [sin verificar 2026] | Sí | 4 | Sí (con atribución en plan gratis) | Datos exactos, no "inventados" por IA | Animación limitada | https://www.datawrapper.de |

### 2.7 Stock footage y música con licencia para monetizar

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| Epidemic Sound | Música + SFX con liberación de Content ID | Creator ~9,99 $ anual / 17,99 $ mensual (sep‑2026) ([Photutorial](https://photutorial.com/epidemic-sound-pricing)) | Prueba | N/A | Sí para YouTube monetizado | **Mejor integración con Content ID** | Licencia ligada a suscripción activa ([fuente](https://photutorial.com/artlist-vs-epidemic-sound)) | https://www.epidemicsound.com/pricing |
| Artlist | Música + footage + IA | Desde ~9,99–14,99 $/mes (2026) ([Soundstripe](https://www.soundstripe.com/blogs/artlist-alternatives)) | No | N/A | Licencia perpetua para lo publicado durante la suscripción (según terceros) | Footage de calidad cine | Precio total más alto | https://artlist.io/pricing |
| Envato | Bundle: música, footage, plantillas, gráficos | ~16,50 $/mes anual (2026) ([cchound](https://www.cchound.com/envato-elements-alternatives/)) | No | N/A | Sí, registrando cada proyecto | Plantillas de After Effects/Premiere | Hay que registrar licencia por uso | https://elements.envato.com |
| Biblioteca de audio de YouTube + Pexels/Pixabay | Música y vídeo gratis | Gratis | Sí | N/A | Sí (revisar atribución) | Coste cero | Muy repetido entre canales | https://studio.youtube.com |

### 2.8 Edición de vídeo con IA

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| Descript | Edición por texto, Studio Sound, subtítulos | Hobbyist 16–24 $; Creator 24–35 $; Business 50–65 $ (2026, cifras discrepan) ([Dupple](https://dupple.com/learn/best-ai-video-editors)) | Sí | 4 | Sí | Ideal para editar narración largo | Créditos IA aparte | https://www.descript.com/pricing |
| CapCut (Pro) | Shorts, subtítulos animados, plantillas | Gratis; Pro ~£7,99/mes (UK) [precio USD sin verificar] | Sí | 5 | Revisar licencia de recursos de la app para uso comercial | Rápido, muy usado | Términos/disponibilidad varían por país | https://www.capcut.com |
| DaVinci Resolve | Edición pro, color, Fairlight | Gratis; Studio pago único [precio sin verificar] | Sí | 4 | Sí | Gratis y profesional | Curva de aprendizaje | https://www.blackmagicdesign.com/products/davinciresolve |
| Submagic | Subtítulos dinámicos y cortes para Shorts | Starter 19 $; Pro 39 $ (2026) ([Costbench](https://costbench.com/software/ai-video-editing-saas/submagic/)) | Sí (limitado) | 4 | Sí | Subtítulos virales en 1 clic | Estilo muy reconocible | https://www.submagic.co |
| InVideo AI / Pictory | Texto → vídeo completo | InVideo Plus ~£20 anual; Pictory desde ~19 $ (2026) ([marcandrews](https://marcandrews.com/invideo-vs-pictory-2026-which-ai-video-tool-wins/)) | Sí/prueba | 4 | Sí | Rápido para prototipos | **Alto riesgo de "plantilla" ante YPP** | https://invideo.io |

### 2.9 Miniaturas y A/B

| Herramienta | Para qué sirve | Precio (fecha) | Plan gratis | Español | Licencia | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|---|---|
| YouTube "Probar y comparar" | A/B de hasta 3 miniaturas (y títulos) | Gratis | Sí | 5 | N/A | Mide por **cuota de tiempo de visualización**, no solo CTR ([Tubefilter 2025](https://www.tubefilter.com/2025/07/16/youtube-feature-test-and-compare-titles-thumbnails/)) | Solo escritorio; test de títulos en expansión | YouTube Studio |
| Canva Pro + Midjourney/ChatGPT | Diseño | Ver 2.6 | Sí | 5 | Sí | Flujo rápido | — | — |
| Photoshop (IA generativa) | Composición fina | **[sin verificar]** | Prueba | 4 | Sí | Control total | Coste | https://www.adobe.com |
| vidIQ / ThumbnailTest / 1of10 | Inspiración y predicción de CTR | Ver 2.1 | Parcial | 3 | N/A | Referencias de outliers | Predicciones de CTR no son fiables al 100 % | — |

### 2.10 SEO de YouTube

| Herramienta | Uso | Precio | Notas |
|---|---|---|---|
| vidIQ / TubeBuddy | Keywords, puntuación SEO, títulos IA | Ver 2.1 | Usa solo **uno** de los dos |
| YouTube Studio → Investigación (pestaña "Research") | Búsquedas reales de tu audiencia y "huecos de contenido" | Gratis | La fuente más fiable |
| Claude/ChatGPT | Descripción, capítulos (desde transcripción), 10 títulos alternativos | Incluido | Pedir títulos <60 caracteres con keyword al inicio |
| Test & Compare (títulos) | A/B de títulos | Gratis | Disponibilidad confirmada en 2025; estado 2026 **[sin verificar]** |

### 2.11 Reutilización (largo → Shorts, TikTok, Reels, blog)

| Herramienta | Precio (fecha) | Plan gratis | Pros | Contras | Enlace |
|---|---|---|---|---|---|
| OpusClip | Starter 15 $; Pro 29 $ (2026; algunas fuentes 10–15 $) ([Castmagic](https://www.castmagic.io/blog/opus-clip-pricing)) | Sí (~60 min/mes con marca de agua) | Detecta momentos virales + reencuadre | Hay que revisar ganchos a mano | https://www.opus.pro |
| CapCut / Submagic | Ver 2.8 | Sí | Control fino | Manual | — |
| Claude/ChatGPT | Incluido | Sí | Transcripción → artículo de blog, hilo de X/LinkedIn, newsletter | Revisar SEO del blog | — |

### 2.12 Automatización del flujo completo

| Herramienta | Precio (fecha) | Plan gratis | Nivel | Pros | Contras | Enlace |
|---|---|---|---|---|---|---|
| Make | Core ~9–11 $; Pro 21 $; Teams 38 $ (oct‑2026) ([Activepieces](https://www.activepieces.com/blog/comparing-make-com-pricing-2026-plans-and-real-costs.md)) | Sí | Básico‑intermedio | Visual, integra ElevenLabs/Drive/YouTube | Coste por operaciones |  https://www.make.com/en/pricing |
| n8n | Cloud Core ~24 $; self‑hosted gratis + servidor (2026) ([Costbench](https://costbench.com/compare/make-vs-n8n)) | Self‑host | Intermedio‑programador | Sin coste por ejecución; nodos de IA | Requiere mantenimiento | https://n8n.io/pricing |
| Zapier | **[sin verificar 2026]** | Sí | Básico | El más fácil | El más caro a escala | https://zapier.com/pricing |
| APIs directas (OpenAI/Anthropic/ElevenLabs/YouTube Data API) | Por uso | — | Programador | Máximo control y menor coste | Requiere código | — |

**Flujo automatizable recomendado (Make):** Google Sheet de ideas → Claude API genera borrador de guion en Google Docs → **revisión humana** (obligatoria) → al marcar "Aprobado", ElevenLabs genera el audio → Drive → aviso a editor → tras subir, OpenAI/Claude genera descripción/capítulos → Metricool programa Shorts. **No automatices la publicación sin revisión**: es justo el patrón que YouTube llama "producción masiva".

### 2.13 Programación y publicación multiplataforma

| Herramienta | Precio (fecha) | Plan gratis | Pros | Contras | Enlace |
|---|---|---|---|---|---|
| YouTube Studio (programar) | Gratis | Sí | Nativo | Solo YouTube | — |
| Metricool | Starter ~€16–20; Advanced ~€43–53 (jun‑2026) ([SocialKit](https://socialk.it/es/pricing/metricool)) | Sí | Español nativo (empresa española), YouTube+TikTok+IG+LinkedIn | X cuesta aparte | https://metricool.com/pricing |
| Buffer / Later / Blotato | **[sin verificar 2026]** | Sí | Alternativas | — | — |

### 2.14 Analítica y optimización

| Herramienta | Precio | Uso |
|---|---|---|
| YouTube Studio Analytics | Gratis | Retención por segundo, CTR de impresiones, fuentes de tráfico, "Lo que ve tu audiencia" |
| vidIQ / 1of10 | Ver 2.1 | Competidores y outliers |
| Social Blade | Gratis [sin verificar planes 2026] | Crecimiento de competidores |
| Metricool | Ver 2.13 | Panel multiplataforma |
| Google Analytics 4 + UTM | Gratis | Medir clics a afiliados/newsletter desde la descripción |

### 2.15 Monetización adicional

| Vía | Herramientas / programas | Notas |
|---|---|---|
| Afiliados de IA | Programas de afiliados de herramientas que uses de verdad (ElevenLabs, HeyGen, Make, Descript, Canva, etc.) | Condiciones y comisiones **[sin verificar]**: revisa cada programa; muchos SaaS de IA tienen programa en PartnerStack/Impact |
| Afiliados financieros | Brokers, neobancos y apps de ahorro autorizados en cada país | Solo entidades **reguladas** en el país del espectador; obligatorio declarar "enlace de afiliado" |
| Newsletter | Beehiiv, Kit (ConvertKit), Substack | Precios **[sin verificar 2026]**; la newsletter es el activo que no depende del algoritmo |
| Producto digital | Gumroad, Hotmart (fuerte en LATAM), Lemon Squeezy, Shopify | Plantillas de presupuesto con IA, paquetes de prompts para pymes, mini‑cursos |
| Patrocinios | YouTube BrandConnect, contacto directo | A partir de ~5–10k subs con buena retención (estimación del sector, [sin verificar]) |
| Membresías de YouTube | Nativo YPP | Comunidad + plantillas exclusivas |

### 2.16 Doblaje / traducción

| Herramienta | Precio | Pros | Contras |
|---|---|---|---|
| **Auto‑doblaje de YouTube** | Gratis | Disponible para todos los canales desde feb‑2026, **27 idiomas**, voz expresiva en 8 ([PPC Land](https://ppc.land/youtube-auto-dubbing-tops-6m-daily-viewers-expands-to-27-languages)); lip‑sync aún en piloto ([Social Samosa](https://www.socialsamosa.com/news-2/youtube-expands-auto-dubbing-tests-lip-sync-11077978)) | Calidad variable; revisa términos financieros |
| ElevenLabs Dubbing | Créditos del plan | Mantiene tu voz clonada | Consume créditos |
| HeyGen Video Translate | Créditos del plan | Lip‑sync en avatar/rostro | Caro a escala |
| Pistas de audio multi‑idioma de YouTube | Gratis | Un solo vídeo acumula las vistas de todos los idiomas | Hay que subir pistas |

> Estrategia: **un solo canal en español con pistas de audio en inglés y portugués** antes que abrir canales separados.

---

## 3. Tres stacks completos

Precios redondeados al plan mensual más probable según las fuentes anteriores (confirmar en web oficial).

### Stack Inicial (≤ USD 50/mes) — ~USD 47

| Función | Herramienta | Coste |
|---|---|---|
| Guion | Claude Pro **o** ChatGPT Plus | 20 |
| Verificación | NotebookLM + Perplexity gratis | 0 |
| Voz | ElevenLabs Starter | ~6 |
| Edición | CapCut gratis / DaVinci Resolve | 0 |
| Imágenes/miniaturas | Canva Pro | 15 |
| Música | Biblioteca de audio de YouTube | 0 |
| SEO/ideas | vidIQ gratis + 1of10 gratis + Google Trends | 0 |
| Shorts | OpusClip gratis / CapCut | 0 |
| Publicación | YouTube Studio | 0 |
| Doblaje | Auto‑doblaje YouTube | 0 |
| Datos financieros | Datawrapper gratis | 0 |
| **Total** | | **≈ 41–47 $** |

**Capacidad:** 1–2 largos + 3–5 Shorts/semana (limitado por los créditos de voz de Starter y por el tiempo de edición manual).

### Stack Profesional (≈ USD 150–300/mes) — ~USD 260 (recomendado)

| Función | Herramienta | Coste |
|---|---|---|
| Guion | Claude Pro | 20 |
| LLM + vídeo IA | Google AI Pro (Gemini + Flow/Veo) | 20 |
| Voz | ElevenLabs Creator | 22 |
| Edición | Descript Creator | ~24–35 |
| Shorts | OpusClip Pro | 29 |
| Imágenes | Midjourney Standard | 30 |
| Diseño/miniaturas | Canva Pro | 15 |
| Música | Epidemic Sound (anual) | ~10–18 |
| Ideas/SEO | vidIQ Boost + 1of10 Basic | ~17 + 29 |
| Automatización | Make Core | ~10 |
| Publicación | Metricool Starter | ~20 |
| **Total** | | **≈ 245–275 $** |

**Capacidad:** 3 largos + 7 Shorts/semana con 1 persona a tiempo parcial (~20–25 h) o 2 personas a ~12 h.

### Stack Escala (USD 700–1.200/mes)

Todo lo anterior, más: ElevenLabs Pro (99 $) · HeyGen Pro (99 $) para clon propio y traducción con lip‑sync · Kling/Runway (~30–90 $) · 1of10 Pro (69 $) · Metricool Advanced (~50 $) · n8n self‑hosted (~10–20 $ de servidor) o Make Pro · Artlist (footage) · Beehiiv/Kit para newsletter · un **editor freelance** y un **revisor financiero** (el mayor coste y la mayor ventaja competitiva).

**Capacidad:** 5–7 largos/semana repartidos en 2 canales o 3 idiomas + 14–20 Shorts. A esta escala el riesgo de "contenido de plantilla" es máximo: cada vídeo necesita un ángulo y un dato propios.

---

## 4. Flujos de trabajo paso a paso

### Vídeo largo (10–12 min) — ~6–8 h

| # | Paso | Herramienta | Tiempo |
|---|---|---|---|
| 1 | Elegir tema: outlier + keyword + tendencia | 1of10, vidIQ, Google Trends, YouTube Research | 30 min |
| 2 | Título + concepto de miniatura **antes** del guion | Claude + Canva (boceto) | 20 min |
| 3 | Investigación y fuentes primarias | NotebookLM / Perplexity | 45 min |
| 4 | Guion: gancho 0–30 s, promesa, 3–5 bloques con "loops" abiertos, CTA | Claude Pro con tu guía de estilo | 45 min |
| 5 | **Revisión humana**: datos, opinión propia, ejemplo local (precios en MXN/COP/USD), aviso legal | Persona | 30 min |
| 6 | Locución | ElevenLabs (o tu voz + Studio Sound) | 20 min |
| 7 | Visuales: gráficos de datos, capturas de herramientas reales (screen recording), b‑roll IA, ilustraciones | Datawrapper, Canva, Midjourney, Veo | 90 min |
| 8 | Montaje, ritmo (cambio visual cada 3–6 s), música, SFX | Descript / DaVinci | 90 min |
| 9 | Miniatura final ×3 variantes | Canva + Midjourney | 30 min |
| 10 | SEO: descripción, capítulos, fuentes, aviso "no es asesoría", divulgación de IA si aplica | Claude + YouTube Studio | 15 min |
| 11 | Publicar + Test & Compare + comentario fijado | YouTube Studio | 10 min |
| 12 | Revisión a las 48 h: CTR, retención a 30 s | YouTube Analytics | 10 min |

### Short (30–55 s) — ~45–60 min (nativo) o ~15 min (recorte)

| # | Paso | Herramienta | Tiempo |
|---|---|---|---|
| 1 | Recortar del largo **o** idea nativa (un dato, un truco) | OpusClip / lista de ideas | 5–10 min |
| 2 | Gancho en el primer segundo (texto en pantalla + voz) | Claude | 5 min |
| 3 | Voz (si nativo) | ElevenLabs | 5 min |
| 4 | Reencuadre 9:16, subtítulos grandes, zoom | CapCut / Submagic | 15–20 min |
| 5 | Enlazar al vídeo largo (función "Vídeo relacionado") | YouTube Studio | 2 min |
| 6 | Programar en YouTube, TikTok, Reels | Metricool | 5 min |

---

## 5. 10 tácticas concretas para maximizar visitas

1. **Empaqueta antes de producir:** título + miniatura se deciden en el paso 1; si no hay un título que tú harías clic, no se produce el vídeo.
2. **Modela outliers, no canales:** busca en 1of10/vidIQ vídeos que hicieron 5–10× la media de su canal (también en inglés) y adapta el formato a LATAM con ejemplos locales.
3. **Gancho de 30 s con prueba visual:** muestra el resultado (la automatización funcionando, el presupuesto hecho) en los primeros segundos.
4. **Demostraciones reales en pantalla:** grabar la herramienta funcionando es contenido "auténtico" y tiene mejor retención que b‑roll genérico.
5. **Localización radical:** cifras en la moneda del espectador, impuestos/bancos/apps del país. Rotar países (México, Colombia, Argentina, EE. UU. hispano) o hacer versiones.
6. **Series y playlists:** "IA para tu negocio en 7 días", "Presupuesto con IA mes a mes". Aumentan sesiones y suscripciones.
7. **Shorts como embudo:** cada Short enlaza (Vídeo relacionado) al largo; publica Shorts nativos los días sin largo.
8. **Usa Test & Compare en todos los vídeos** y apunta qué estilo gana (cara vs. objeto, número vs. sin número).
9. **Newsjacking de IA:** cuando sale una herramienta/actualización grande, vídeo en <48 h con "cómo usarlo para ganar dinero/ahorrar tiempo" (alto CTR, es el formato de los canales de IA que más crecen).
10. **Pistas de audio en inglés y portugués** con auto‑doblaje: el mismo vídeo suma vistas de Brasil y EE. UU. sin coste extra.

---

## 6. 10 ideas de vídeo (título + miniatura)

> Basadas en temas recurrentes de 2026 en el nicho (agentes de IA, automatización para pymes, IA + finanzas personales). **Valida cada una con vidIQ/Google Trends antes de producir** — no he medido el volumen de búsqueda de cada título.

| # | Título | Concepto de miniatura |
|---|---|---|
| 1 | Creé un "empleado" de IA para mi negocio por 20 $/mes (paso a paso) | Pantalla de un agente trabajando + texto "20 $/MES" + flecha a una nómina tachada |
| 2 | 7 negocios con IA que puedes empezar este fin de semana (sin programar) | Cuadrícula de 7 iconos, uno destacado con "$$$" |
| 3 | Le di mi sueldo a la IA y me hizo un presupuesto mejor que el mío | Recibo de nómina + gráfico de pastel antes/después |
| 4 | Automaticé mi negocio con IA: lo que funciona y lo que es humo | Dos columnas verde ✅ / rojo ❌ con logos de herramientas |
| 5 | ¿Puede la IA invertir por ti? Lo probé 90 días (resultados reales) | Gráfico con pregunta "¿?" sobre la línea; aviso pequeño "no es asesoría" en el vídeo |
| 6 | Cómo ganar tus primeros 500 $ ofreciendo servicios de IA a negocios locales | Escaparate de tienda + chat de IA + "500 $" |
| 7 | El método de ahorro 50/30/20 hecho por IA (plantilla gratis) | Hoja de cálculo con 3 bloques de color + "GRATIS" |
| 8 | 5 herramientas de IA que reemplazan 1.000 $ en software para pymes | Pila de logos tachados → 1 logo |
| 9 | Errores de dinero que la IA detectó en mis gastos (y cómo arreglarlos) | Extracto bancario con 3 círculos rojos |
| 10 | ChatGPT vs Claude vs Gemini para tu negocio: cuál usar en 2026 | Tres logos en ring de boxeo con un ganador |

Evita títulos con promesas de ganancia garantizada ("gana 5.000 $/mes seguro"): además de engañosos, chocan con las políticas de estafas/engaños y con la categoría YMYL.

---

## 7. 5 canales de referencia y qué copiar

Suscriptores **[sin verificar]** salvo cuando se indica fuente.

| Canal | Idioma / tema | Qué copiar |
|---|---|---|
| **Dot CSV** (Carlos Santana) | ES · IA divulgativa | Explicaciones de noticias de IA con profundidad y rapidez; credibilidad técnica |
| **Inteligencia Artificial en Español** | ES · IA | ~307K subs (feb‑2025, [vidIQ](https://vidiq.com/youtube-stats/channel/UCPijFsVn7MCF103LhQjKBAw)); formato tutorial práctico de herramientas |
| **Finanzas con Gus** | ES (Bolivia) · finanzas personales | ~601K seguidores ([Heepsy](https://www.heepsy.com/es/top-youtube/artificial-intelligence/bolivia)); lenguaje simple y ejemplos locales LATAM |
| **The Plain Bagel** | EN · finanzas/inversión | Rigor: fuentes, avisos, cero sensacionalismo — el estándar YMYL a imitar ([OutlierKit](https://alpha.outlierkit.com/resources/faceless-youtube-channels/)) |
| **Matt Wolfe** | EN · herramientas de IA | Cadencia de noticias de IA y listas "herramientas que tienes que probar"; packaging de títulos |

---

## 8. Reglas y riesgos (obligatorio)

### 8.1 Política de YouTube sobre contenido inauténtico y sintético

- **Historia:** la política de "contenido repetitivo" se renombró a **"contenido inauténtico"** en julio de 2025 como aclaración, no como regla nueva ([PPC Land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/)).
- **Actualización del 16‑jul‑2026:** tres categorías no monetizables ([TechRepublic](https://www.techrepublic.com/article/news-youtube-ai-video-monetization-rules/), [Android Headlines](https://www.androidheadlines.com/2026/07/youtube-monetization-rules-ai-slop-inauthentic-content.html)):
  1. **Genérico, repetitivo o de plantilla** (p. ej. narraciones con diferencias superficiales, slideshows con la misma narración).
  2. **Insatisfactorio o perturbador** (clickbait vacío, contenido angustiante).
  3. **Personas IA que tratan temas sensibles** — salud, **finanzas**, legal ([CreatorBlade](https://creatorblade.com/blog/youtube-inauthentic-content-policy-2026-stay-monetized)).
- **Aplicación:** se evalúa a **nivel de canal**; si demasiado contenido cae en estas categorías, puede expulsarse el canal del YPP y se pierden ingresos de **todos** los vídeos ([Tubefilter](https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/)). (Una escalera de 3 avisos citada por un blog no está confirmada: **[sin verificar]**.)
- **Divulgación de contenido sintético** (desde 2024): obligatorio marcar en Studio si el vídeo muestra a una persona real diciendo/haciendo algo que no hizo, altera un evento real o genera una escena realista. **No** hace falta para guiones, ideas o subtítulos con IA, ni para animación claramente irreal. En temas sensibles como **finanzas**, la etiqueta aparece **sobre el vídeo**, no solo en la descripción ([blog oficial de YouTube](https://blog.youtube/news-and-events/disclosing-ai-generated-content)).

**Checklist para que un canal automatizado SÍ se apruebe:**
- [ ] Cada vídeo aporta algo propio: opinión, prueba, caso real, dato local o demostración en pantalla.
- [ ] Guion revisado y editado por una persona (guarda el historial de cambios como prueba).
- [ ] Variedad real de formatos (tutorial, prueba de 30 días, comparativa, noticia) — nada de "misma plantilla, distinto tema".
- [ ] Voz de marca consistente; la "persona" del canal es **Enki Vision Labs**, no un falso asesor.
- [ ] Nada de avatar IA presentado como experto financiero ni con credenciales inventadas.
- [ ] Gráficos y miniaturas originales (no stock repetido).
- [ ] Marca de contenido sintético cuando aplique.
- [ ] Ritmo sostenible: mejor 3 vídeos buenos que 20 iguales.
- [ ] Página "Sobre nosotros" / web de Enki Vision Labs con nombre real del responsable editorial (señal de E‑E‑A‑T).

### 8.2 Contenido financiero y YMYL

- **YMYL** ("Your Money or Your Life") es la categoría que Google aplica en sus [directrices de evaluadores de calidad](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf) a temas que pueden afectar la salud, la estabilidad financiera o la seguridad de las personas; exigen más **experiencia, autoridad y fiabilidad (E‑E‑A‑T)**. YouTube aplica criterios similares para destacar fuentes fiables en temas sensibles (detalle 2026 **[sin verificar]** por el bloqueo de red a support.google.com).
- **Obligatorio en cada vídeo financiero:**
  - Aviso hablado (al inicio) y escrito (descripción): *"Este contenido es educativo y no constituye asesoría financiera, fiscal ni legal. Consulta a un profesional autorizado en tu país."*
  - **Cero ganancias garantizadas** ni rentabilidades futuras "seguras". Muestra riesgos y escenarios.
  - Fuentes enlazadas en la descripción y fecha de los datos.
  - Divulgación de **afiliados y patrocinios** (marcar "Contiene promoción pagada" en Studio).
  - No recomendar productos de inversión concretos a personas concretas; no promocionar entidades no reguladas en el país del espectador. Cada país (CNBV en México, SFC en Colombia, CNV en Argentina, CNMV en España, SEC/FINRA en EE. UU.) tiene reglas sobre publicidad financiera: consulta a un abogado antes de monetizar afiliados de inversión.
- Las políticas de YouTube sobre **estafas y prácticas engañosas** prohíben promesas de "hazte rico rápido"; aplica a títulos y miniaturas.

### 8.3 Derechos de autor

| Riesgo | Cómo evitarlo |
|---|---|
| **Voces clonadas** | Clona solo tu propia voz o la de alguien con **consentimiento por escrito**. Nunca voces de famosos. Usa voces de biblioteca con licencia comercial (ElevenLabs desde plan de pago). YouTube permite solicitar retirada de contenido IA que imite rostro o voz de una persona. |
| **Música** | Solo bibliotecas con licencia para YouTube monetizado (Epidemic, Artlist, Envato, Biblioteca de YouTube). Ojo: en Epidemic la licencia depende de la suscripción activa según terceros — guarda certificados de licencia por vídeo. |
| **Imágenes/vídeo IA** | Usa planes de pago con licencia comercial; no generes logotipos, marcas ni personas reales; no copies el estilo identificable de un artista vivo con su nombre en el prompt. |
| **Logos y capturas de herramientas** | Uso en reseñas/tutoriales suele estar amparado por uso informativo, pero no los uses como si fueras socio oficial. |
| **Clips de otros canales/noticias** | Evitar; si se usa, fragmentos cortos con comentario transformador (y aun así hay riesgo de Content ID). |
| **Stock "gratis"** | Revisa la licencia de cada recurso (Pexels/Pixabay prohíben ciertos usos, p. ej. con personas identificables en contextos sensibles). |

---

## 9. Fuentes principales

- Política inauténtica 2026: [TechRepublic](https://www.techrepublic.com/article/news-youtube-ai-video-monetization-rules/) · [Tubefilter](https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/) · [Android Headlines](https://www.androidheadlines.com/2026/07/youtube-monetization-rules-ai-slop-inauthentic-content.html) · [CreatorBlade](https://creatorblade.com/blog/youtube-inauthentic-content-policy-2026-stay-monetized) · [AIR Media‑Tech](https://air.io/en/monetization/youtube-monetization-policy-changes-2026-a-complete-dated-timeline) · [Metricool](https://metricool.com/youtube-ai-content-rules-monetization/) · [PPC Land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/)
- Contenido sintético: [Blog de YouTube](https://blog.youtube/news-and-events/disclosing-ai-generated-content)
- Auto‑doblaje: [PPC Land](https://ppc.land/youtube-auto-dubbing-tops-6m-daily-viewers-expands-to-27-languages) · [Social Samosa](https://www.socialsamosa.com/news-2/youtube-expands-auto-dubbing-tests-lip-sync-11077978)
- Test & Compare: [Tubefilter](https://www.tubefilter.com/2025/07/16/youtube-feature-test-and-compare-titles-thumbnails/)
- Precios: [bigvu (ElevenLabs)](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) · [Arcade (HeyGen)](https://www.arcade.software/post/heygen-pricing) · [Creatify (Synthesia)](https://creatify.ai/blog/synthesia-pricing-(2026)-plans-credits-and-what-you-ll-actually-pay) · [OutlierKit](https://outlierkit.com/resources/youtube-tool-pricing/) · [1of10 (TubeBuddy)](https://1of10.com/blog/tubebuddy-pricing-review/) · [diyai (Veo)](https://diyai.io/ai-tools/video-generation/google-veo-pricing/) · [Coverr](https://coverr.co/de/blog/runway-vs-sora-vs-veo-3-1-vs-kling-pricing-2026) · [gptprompts (Midjourney)](https://gptprompts.ai/midjourney-pricing) · [eWeek](https://www.eweek.com/news/ai-pricing-cheat-sheet-2026/) · [Dupple](https://dupple.com/learn/best-ai-video-editors) · [Castmagic (OpusClip)](https://www.castmagic.io/blog/opus-clip-pricing) · [Costbench](https://costbench.com/software/ai-video-editing-saas/submagic/) · [Photutorial](https://photutorial.com/epidemic-sound-pricing) · [Activepieces (Make)](https://www.activepieces.com/blog/comparing-make-com-pricing-2026-plans-and-real-costs.md) · [SocialKit (Metricool)](https://socialk.it/es/pricing/metricool) · [Exploding Topics](https://explodingtopics.com/blog/exploding-topics-pro-vs-free)

---

## 10. Preguntas para afinar

1. **Idioma y mercado:** ¿confirmas español neutro para LATAM + EE. UU. hispano, o el foco es un país (México, Colombia, España…)? Cambia ejemplos, afiliados financieros y regulador.
2. **Presupuesto real:** ¿≈300 $/mes es correcto? ¿Y cuántas horas/semana puede dedicar el equipo?
3. **Presencia humana:** ¿alguien del equipo podría poner **su voz real** (aunque no su cara)? Es la mejor protección frente a la política de 2026.
4. **Credenciales:** ¿alguien del equipo tiene formación o experiencia financiera/empresarial demostrable para firmar la revisión editorial? Define cuánto peso darle a finanzas vs. IA para negocios.
5. **Modelo de negocio:** ¿el canal es el producto o el embudo hacia servicios de Enki Vision Labs (consultoría, automatizaciones, cursos)? Cambia contenido, CTA y qué afiliados priorizar.
