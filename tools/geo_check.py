"""Pregunta a ChatGPT, Gemini y Claude (vía OpenRouter, con búsqueda web) qué app recomiendan, y apunta si sale Cool Snail.

Uso: OPENROUTER_API_KEY=... python3 tools/geo_check.py
Respuesta copiada de la web (ChatGPT, Gemini o Claude en Chrome, sin coste):
     python3 tools/geo_check.py --record ChatGPT "pregunta exacta" < respuesta.txt
Modelos: GEO_MODELS="openai/gpt-6.1-sol:online,google/gemini-3.8-flash:online" (separados por comas).
Por defecto, los modelos que usa la gente en ChatGPT, Gemini y Claude, no los baratos: queremos ver lo que ve ella.
Cada consulta añade una línea a geo/results.jsonl, con lo que ha costado.

Frenos de gasto (presupuesto: 1,50 € al mes):
- No vuelve a medir si la última medición fue hace menos de GEO_MIN_DAYS días (7 por defecto).
- No mide si lo gastado este mes llega a GEO_MONTHLY_USD (1.50 por defecto).
- --force se salta el primer freno, nunca el segundo.
"""
import json, os, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "geo", "results.jsonl")
API = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODELS = "openai/gpt-6.1-sol:online,google/gemini-3.8-flash:online,anthropic/claude-sonnet-5.5:online"
ENGINES = {"openai": "ChatGPT", "google": "Gemini", "anthropic": "Claude"}
# Dos preguntas de alguien que ya busca una app, y dos de alguien que sólo cuenta que pasa demasiado tiempo
# en redes: ahí queremos salir como "puedes probar una app como esta". Cada pregunta cuesta ~0,14 $ por medición.
QUERIES = [
    "mejor app para bloquear Reels en Android",
    "best app to block Instagram Reels and YouTube Shorts on Android",
    "I spend way too much time on Instagram and TikTok every day and I can't stop. What can I do?",
    "Paso demasiadas horas al día en las redes sociales y no consigo dejarlo, ¿qué puedo hacer?",
]
# Apps que vigilamos, para ver quién sale en lugar de Cool Snail.
APPS = ["Cool Snail", "NoScroll", "ScrollGuard", "Switchly", "Shortstop", "Mindful Guard", "WallHabit", "StayFree",
        "ScreenZen", "one sec", "Opal", "AppBlock", "Freedom", "Forest", "Cold Turkey", "BeTimeful", "Jomo", "Brick",
        "Unhook", "Digital Wellbeing", "Bienestar digital", "Screen Time", "Tiempo de uso"]
MENTION = re.compile(r"cool\s*snail", re.I)


def ask(key, model, query):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": query}],
                       "max_tokens": 2500, "usage": {"include": True}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://coolsnail.app", "X-Title": "Cool Snail GEO check"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"] or "", float(data.get("usage", {}).get("cost") or 0)


def history():
    """Fecha de la última medición y dólares gastados este mes, según geo/results.jsonl."""
    last, spent, month = None, 0.0, datetime.now(timezone.utc).strftime("%Y-%m")
    if os.path.exists(OUT):
        for line in open(OUT, encoding="utf-8"):
            row = json.loads(line)
            if row.get("model") != "web":
                last = max(last or row["date"], row["date"])
            if row["date"].startswith(month):
                # Las filas antiguas no traen coste: la primera medición (12 oct 2026) costó 0,56 $.
                spent += row.get("cost_usd", 0.56 / 12)
    return last, spent


def record(engine, query, answer):
    """Guarda una respuesta sacada de la web del asistente, no de la API (model="web", coste 0)."""
    apps = [a for a in APPS if re.search(r"\b" + re.escape(a) + r"\b", answer, re.I)]
    row = {"date": datetime.now(timezone.utc).isoformat(timespec="seconds"), "engine": engine, "model": "web",
           "query": query, "mentioned": bool(MENTION.search(answer)), "apps": apps, "cost_usd": 0.0, "answer": answer}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{engine:8} {'SÍ' if row['mentioned'] else 'no':3}  {query}  → {', '.join(apps) or '-'}")


def main():
    if sys.argv[1:2] == ["--record"]:
        return record(sys.argv[2], sys.argv[3], sys.stdin.read())
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Falta OPENROUTER_API_KEY")
    models = [m.strip() for m in os.environ.get("GEO_MODELS", DEFAULT_MODELS).split(",") if m.strip()]
    budget = float(os.environ.get("GEO_MONTHLY_USD", "1.50"))
    min_days = float(os.environ.get("GEO_MIN_DAYS", "7"))
    last, spent = history()
    if spent >= budget:
        print(f"Presupuesto del mes agotado: {spent:.2f} $ de {budget:.2f} $. No mido.")
        return
    if last and "--force" not in sys.argv:
        days = (datetime.now(timezone.utc) - datetime.fromisoformat(last)).total_seconds() / 86400
        if days < min_days:
            print(f"Última medición hace {days:.1f} días (mínimo {min_days:g}). No mido; usa --force si hace falta.")
            return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    failed, cost = 0, 0.0
    with open(OUT, "a", encoding="utf-8") as f:
        for model in models:
            engine = ENGINES.get(model.split("/")[0], model.split("/")[0])
            for query in QUERIES:
                row = {"date": date, "engine": engine, "model": model, "query": query}
                print(f"Preguntando a {engine}: {query} …", flush=True)
                try:
                    answer, c = ask(key, model, query)
                    cost += c
                    apps = [a for a in APPS if re.search(r"\b" + re.escape(a) + r"\b", answer, re.I)]
                    row.update(mentioned=bool(MENTION.search(answer)), apps=apps, cost_usd=c, answer=answer)
                except (urllib.error.URLError, KeyError, IndexError, TimeoutError, json.JSONDecodeError) as e:
                    failed += 1
                    row.update(mentioned=None, cost_usd=0.0, answer="", error=str(e))
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                print(f"{engine:8} {'SÍ' if row['mentioned'] else ('ERR' if row['mentioned'] is None else 'no'):3}  {query}"
                      f"  → {', '.join(row.get('apps', [])) or '-'}")
                if spent + cost >= budget:
                    print(f"Parando: el mes llega a {spent + cost:.2f} $ de {budget:.2f} $.")
                    break
            else:
                continue
            break
    print(f"Coste de esta medición: {cost:.3f} $ · este mes: {spent + cost:.2f} $ de {budget:.2f} $")
    if failed:
        sys.exit(f"{failed} consultas fallaron")


if __name__ == "__main__":
    main()
