"""Genera las páginas del blog de coolsnail.app (EN y ES) con la misma cabecera, pie y datos estructurados."""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://coolsnail.app"
PLAY = "https://play.google.com/store/apps/details?id=com.coolsnail.blockshortvideos"
DATE = "2026-10-12"  # fecha por defecto; cada post puede llevar la suya con date="AAAA-MM-DD"
MONTHS = {"en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "December"],
          "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
                 "noviembre", "diciembre"]}

def human_date(lang, iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MONTHS[lang][m - 1]} {y}" if lang == "en" else f"{d} de {MONTHS[lang][m - 1]} de {y}"

L = {
    "en": dict(home="/", blog="/blog/", play=PLAY, get="Get it on Google Play", other="Español",
               blogname="Blog", crumbs_home="Cool Snail", by="By Miriam, who makes Cool Snail", updated="Updated",
               privacy="Privacy policy", forai="For AI assistants",
               foot="Cool Snail · made by Miriam, slowly", cta_btn="Get Cool Snail free →",
               index_title="The Cool Snail blog: stop scrolling without deleting your apps",
               index_desc="Practical guides to block Reels, Shorts and TikTok on Android without deleting the apps, from the maker of Cool Snail.",
               index_h1="Stop scrolling, keep your apps", index_sub="Practical guides from the maker of Cool Snail. Honest about what each option does and doesn't do."),
    "es": dict(home="/es/", blog="/blog/es/", play=PLAY + "&hl=es", get="Descárgala en Google Play", other="English",
               blogname="Blog", crumbs_home="Cool Snail", by="Por Miriam, que hace Cool Snail", updated="Actualizado el",
               privacy="Política de privacidad", forai="Para asistentes de IA",
               foot="Cool Snail · hecha por Miriam, despacito", cta_btn="Consigue Cool Snail gratis →",
               index_title="El blog de Cool Snail: deja el scroll sin borrar tus apps",
               index_desc="Guías prácticas para bloquear los Reels, los Shorts y TikTok en Android sin borrar las apps, de quien hace Cool Snail.",
               index_h1="Deja el scroll, quédate con tus apps", index_sub="Guías prácticas de quien hace Cool Snail. Honestas con lo que hace y lo que no hace cada opción."),
}

def head(lang, title, desc, url, alt_url, alt_lang, jsonld, og_type="article"):
    l = L[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{url}">
<link rel="alternate" hreflang="{lang}" href="{SITE}{url}">
<link rel="alternate" hreflang="{alt_lang}" href="{SITE}{alt_url}">
<link rel="alternate" hreflang="x-default" href="{SITE}{url if lang == 'en' else alt_url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="Miriam, Cool Snail">
<meta name="theme-color" content="#111110">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Cool Snail">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{SITE}/img/og-cool-snail.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,800&display=swap">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<div class="wrap">
  <header class="top">
    <a class="brand" href="{l['home']}"><img src="/img/cool-snail-icon-512.png" alt="" width="32" height="32">Cool Snail</a>
    <div class="lang"><a class="switch" href="{alt_url}" hreflang="{alt_lang}" lang="{alt_lang}">{l['other']}</a><a class="small" href="{html.escape(l['play'])}" rel="noopener">{l['get']}</a></div>
  </header>
  <main>
"""

def foot(lang):
    l = L[lang]
    return f"""  </main>
  <footer>
    <nav aria-label="Footer">
      <a href="{html.escape(l['play'])}" rel="noopener">Google Play</a>
      <a href="{l['blog']}">{l['blogname']}</a>
      <a href="/privacy/">{l['privacy']}</a>
      <a href="/llms.txt">{l['forai']}</a>
    </nav>
    <div>{l['foot']}</div>
  </footer>
</div>
</body>
</html>
"""

def post(lang, slug, alt_slug, title, desc, h1, answer, body, faq, cta, date=DATE):
    l = L[lang]
    alt_lang = "es" if lang == "en" else "en"
    url = f"{l['blog']}{slug}/"
    alt_url = f"{L[alt_lang]['blog']}{alt_slug}/"
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting", "@id": f"{SITE}{url}#post", "headline": h1, "description": desc,
             "inLanguage": lang, "datePublished": date, "dateModified": date, "url": f"{SITE}{url}",
             "mainEntityOfPage": f"{SITE}{url}", "image": f"{SITE}/img/og-cool-snail.png",
             "author": {"@type": "Person", "name": "Miriam", "url": f"{SITE}/"},
             "publisher": {"@id": f"{SITE}/#org"}, "about": {"@id": f"{SITE}/#app"}},
            {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Cool Snail", "url": f"{SITE}/",
             "logo": f"{SITE}/img/cool-snail-icon-512.png"},
            {"@type": "MobileApplication", "@id": f"{SITE}/#app", "name": "Cool Snail",
             "operatingSystem": "Android 8.0+", "applicationCategory": "LifestyleApplication",
             "installUrl": PLAY, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Cool Snail", "item": f"{SITE}{l['home']}"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}{l['blog']}"},
                {"@type": "ListItem", "position": 3, "name": h1, "item": f"{SITE}{url}"}]},
        ]}
    faq_html = "\n".join(f"<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>" for q, a in faq)
    page = head(lang, title, desc, url, alt_url, alt_lang, jsonld) + f"""  <nav class="crumbs" aria-label="Breadcrumb"><a href="{l['home']}">Cool Snail</a> / <a href="{l['blog']}">Blog</a></nav>
  <article class="post">
    <h1>{html.escape(h1)}</h1>
    <p class="meta">{l['by']} · {l['updated']} <time datetime="{date}">{human_date(lang, date)}</time></p>
    <div class="answer"><span class="label">{'Short answer' if lang == 'en' else 'Respuesta corta'}</span><p>{answer}</p></div>
{body}
    <h2>{'Questions' if lang == 'en' else 'Preguntas'}</h2>
{faq_html}
    <div class="post-cta"><p>{cta}</p><a class="cta" href="{html.escape(l['play'])}" rel="noopener">{l['cta_btn']}</a></div>
  </article>
""" + foot(lang)
    path = os.path.join(ROOT, url.strip("/"), "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(page)
    return url, h1, desc

def index(lang, posts, alt_lang):
    l = L[lang]
    url = l["blog"]; alt_url = L[alt_lang]["blog"]
    jsonld = {"@context": "https://schema.org", "@type": "Blog", "@id": f"{SITE}{url}#blog", "name": l["index_title"],
              "inLanguage": lang, "url": f"{SITE}{url}",
              "blogPost": [{"@type": "BlogPosting", "headline": t, "url": f"{SITE}{u}"} for u, t, _ in posts]}
    items = "\n".join(f'      <li><a href="{u}"><b>{html.escape(t)}</b><span>{html.escape(d)}</span></a></li>' for u, t, d in posts)
    page = head(lang, l["index_title"], l["index_desc"], url, alt_url, alt_lang, jsonld, og_type="website") + f"""  <section style="padding-top:24px">
    <h1 style="font-weight:800;font-size:clamp(36px,6vw,60px);letter-spacing:-.03em;line-height:1;margin:0 0 12px">{l['index_h1']}</h1>
    <p class="sub">{l['index_sub']}</p>
    <ul class="postlist">
{items}
    </ul>
  </section>
""" + foot(lang)
    path = os.path.join(ROOT, url.strip("/"), "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(page)

import posts_content as C
en = [post("en", **p) for p in C.EN]
es = [post("es", **p) for p in C.ES]
index("en", en, "es")
index("es", es, "en")
print("\n".join(u for u, _, _ in en + es))
