# GEO / SEO notes

## 2026-10-12

**Medición:** no se ha podido medir. `OPENROUTER_API_KEY` no está en el entorno de la tarea programada, así que `tools/geo_check.py` (creado hoy) no se ha ejecutado y aún no hay línea base en `geo/results.jsonl`.

**Hallazgos (búsqueda web):**
- Para "block reels shorts android", lo que sale arriba son apps de nicho con artículo de prensa detrás: Sane Scrolling (Android Authority), NoScroll (blog propio con guías "[2025] How to disable YouTube Shorts…"), SocialLite (App Store), y una nota de Digital Trends en español sobre una app que "mata" Reels y Shorts. Ganan por **menciones de terceros** (prensa, App Store) y por **guías con año en el título**.
- AppBlock tiene una sección de ayuda muy estructurada (appblock.app/help/android/…) con una página por función (horarios, ubicación, modo estricto). Eso alimenta bien a los LLM cuando preguntan por "AppBlock alternatives".
- Google documenta Bienestar digital en support.google.com/android/answer/9346420 (temporizadores que se reinician a medianoche, modo Concentración con horario y "Tomar un descanso").

**Hueco detectado:** no había ninguna página comparativa ("best apps…", "alternatives to…"), que es el formato que más citan los asistentes. Cubierto hoy con la guía EN/ES. Siguiente hueco: Cool Snail no tiene menciones de terceros (prensa tech, listados). Borrador en `geo/outreach.md`.

**Pendiente técnico:** `build_blog.py` usa una sola `DATE` para todos los posts; al publicar el próximo, cambiará también la fecha de los antiguos. Conviene una fecha por post.
