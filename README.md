# Multi-Agent Customer Support

A small full-stack customer support system. An LLM-based router
classifies each incoming message into one or more intents (billing,
technical, product, complaint, faq) and dispatches it to the
matching specialist agent, which answers using context retrieved
from local company documents (`data/*.md`).

## Stack

- **Backend:** FastAPI (`main.py`), OpenAI API for the LLM calls
- **Frontend:** static HTML/CSS/JS chat UI (`static/`), served by the
  same FastAPI app
- **Retrieval:** lightweight keyword-overlap retriever over
  `data/*.md` — no external vector DB required

## Project layout

```
agents/            intent detection, router, and per-topic agents
rag/retriever.py   local keyword-based context retrieval
data/*.md          source documents the agents retrieve context from
static/            frontend (index.html, style.css, script.js)
main.py            FastAPI app: /api/chat, /api/health, static hosting
config.py          reads OPENAI_API_KEY / LLM_MODEL from env
```

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate        # on Windows
pip install -r requirements-dev.txt

copy .env.example .env        # then fill in OPENAI_API_KEY
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

Without an `OPENAI_API_KEY` set, the app still runs — the health
check reports `llm_configured: false` and the chat endpoint replies
with a friendly message instead of calling OpenAI.

## Tests

```bash
pytest
```

## Deploy on Render

This repo includes a `render.yaml` blueprint.

1. Push this repo to GitHub.
2. On [Render](https://dashboard.render.com), click **New > Blueprint**
   and select this repo.
3. Render reads `render.yaml` and creates a web service automatically
   (build: `pip install -r requirements.txt`, start:
   `uvicorn main:app --host 0.0.0.0 --port $PORT`).
4. In the service's **Environment** tab, set `OPENAI_API_KEY` to your
   real key (it's intentionally left out of `render.yaml`/git).
5. Deploy. Your chat UI will be live at the Render-provided URL.
