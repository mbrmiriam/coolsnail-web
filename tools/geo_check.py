"""Pregunta a ChatGPT, Gemini y Claude (vía OpenRouter, con búsqueda web) qué app recomiendan, y apunta si sale Cool Snail.

Uso: OPENROUTER_API_KEY=... python3 tools/geo_check.py
Modelos: GEO_MODELS="openai/gpt-6.1-sol:online,google/gemini-3.8-flash:online" (separados por comas).
Cada consulta añade una línea a geo/results.jsonl.
"""
import json, os, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "geo", "results.jsonl")
API = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODELS = "openai/gpt-6.1-sol:online,google/gemini-3.8-flash:online,anthropic/claude-sonnet-5.5:online"
ENGINES = {"openai": "ChatGPT", "google": "Gemini", "anthropic": "Claude"}
QUERIES = [
    "mejor app para bloquear Reels en Android",
    "best app to block Instagram Reels and YouTube Shorts on Android",
    "app to stop doomscrolling without deleting social media",
    "alternatives to AppBlock for blocking social media addiction",
]
MENTION = re.compile(r"cool\s*snail", re.I)


def ask(key, model, query):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": query}]}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://coolsnail.app", "X-Title": "Cool Snail GEO check"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["choices"][0]["message"]["content"] or ""


def main():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Falta OPENROUTER_API_KEY")
    models = [m.strip() for m in os.environ.get("GEO_MODELS", DEFAULT_MODELS).split(",") if m.strip()]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    failed = 0
    with open(OUT, "a", encoding="utf-8") as f:
        for model in models:
            engine = ENGINES.get(model.split("/")[0], model.split("/")[0])
            for query in QUERIES:
                row = {"date": date, "engine": engine, "model": model, "query": query}
                print(f"Preguntando a {engine}: {query} …", flush=True)
                try:
                    answer = ask(key, model, query)
                    row.update(mentioned=bool(MENTION.search(answer)), answer=answer)
                except (urllib.error.URLError, KeyError, IndexError, TimeoutError, json.JSONDecodeError) as e:
                    failed += 1
                    row.update(mentioned=None, answer="", error=str(e))
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                print(f"{engine:8} {'SÍ' if row['mentioned'] else ('ERR' if row['mentioned'] is None else 'no'):3}  {query}")
    if failed:
        sys.exit(f"{failed} consultas fallaron")


if __name__ == "__main__":
    main()
