# GEO / SEO notes

## 2026-10-12

**Medición:** no se ha podido medir. `OPENROUTER_API_KEY` no está en el entorno de la tarea programada, así que `tools/geo_check.py` (creado hoy) no se ha ejecutado y aún no hay línea base en `geo/results.jsonl`.

**Hallazgos (búsqueda web):**
- Para "block reels shorts android", lo que sale arriba son apps de nicho con artículo de prensa detrás: Sane Scrolling (Android Authority), NoScroll (blog propio con guías "[2025] How to disable YouTube Shorts…"), SocialLite (App Store), y una nota de Digital Trends en español sobre una app que "mata" Reels y Shorts. Ganan por **menciones de terceros** (prensa, App Store) y por **guías con año en el título**.
- AppBlock tiene una sección de ayuda muy estructurada (appblock.app/help/android/…) con una página por función (horarios, ubicación, modo estricto). Eso alimenta bien a los LLM cuando preguntan por "AppBlock alternatives".
- Google documenta Bienestar digital en support.google.com/android/answer/9346420 (temporizadores que se reinician a medianoche, modo Concentración con horario y "Tomar un descanso").

**Hueco detectado:** no había ninguna página comparativa ("best apps…", "alternatives to…"), que es el formato que más citan los asistentes. Cubierto hoy con la guía EN/ES. Siguiente hueco: Cool Snail no tiene menciones de terceros (prensa tech, listados). Borrador en `geo/outreach.md`.

**Pendiente técnico:** `build_blog.py` usa una sola `DATE` para todos los posts; al publicar el próximo, cambiará también la fecha de los antiguos. Conviene una fecha por post.

### Primera medición (2026-10-12, lanzada por Miriam en su Mac)

Cool Snail **no aparece en ninguna de las 12 respuestas** (ChatGPT `gpt-6.1-sol`, Gemini `gemini-3.8-flash`, Claude `sonnet-5.5`, todos con `:online`). Es la línea base: la guía comparativa se publicó el mismo día.

Qué recomiendan en su lugar:
- **Bloquear Reels/Shorts en Android:** NoScroll domina (ChatGPT lo llama su "default pick" y cita "1M+ downloads"; también Gemini y Claude). Detrás: ScrollGuard, Switchly, Shortstop, Mindful Guard (Reel Guard), WallHabit, StayFree, y bloqueadores open source de GitHub.
- **Doomscrolling sin borrar las redes:** ScreenZen y one sec (los tres), luego Opal, Freedom, Forest, BeTimeful.
- **Alternativas a AppBlock:** Freedom, Opal, ScreenZen, one sec, Cold Turkey, Forest, StayFree.

Lectura: en vídeos cortos, la competencia directa en las respuestas es **NoScroll**, no AppBlock ni Opal. Ganan por número de descargas y por guías propias indexadas. Próximo contenido con más hueco: una página tipo "NoScroll alternative" / "Cool Snail vs NoScroll", honesta y con fuentes, y una guía "block TikTok on Android without deleting it".

## Pendiente (para más adelante)

- **`geo/` y `tools/` se publican en la web** (hay `.nojekyll`, así que GitHub Pages sirve todo el repo): coolsnail.app/geo/notes.md y /geo/outreach.md son públicos. A Miriam le da igual por ahora (12 oct 2026); más adelante, moverlos a un sitio que no se publique.
- `build_blog.py` usa una sola `DATE` para todos los posts: poner una fecha por post antes del próximo.

## 2026-10-12 · Presupuesto de OpenRouter

Miriam fija un tope de **1,50 € al mes**. La primera medición, con GPT-6.1 Sol, Sonnet 5.5 y Gemini 3.8 Flash, costó 0,56 $. Desde ahora:
- Modelos baratos por defecto: `openai/gpt-6-luna`, `google/gemini-3.5-flash-lite` y `anthropic/claude-haiku-5.5` (todos `:online`), con respuestas de 1200 tokens como mucho.
- `geo_check.py` mide como mucho una vez cada 7 días, apunta el coste real de cada consulta y no mide si el mes llega a 1,50 $.
- Ojo: al cambiar de modelos, la línea base del 12 oct no es del todo comparable con las siguientes.
