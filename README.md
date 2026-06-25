# PG2000

Prompting specialist — upload an image and get back a detailed prompt you can feed
into AI image generators (Midjourney, Stable Diffusion, DALL-E, etc.). Image-generation
prompts are the first supported mode; more prompt types (text, video, ...) are planned.

## Project structure

```
backend/   FastAPI app (image upload, LLM call, JSON API)
frontend/  Static HTML/CSS/JS UI, served by the backend
```

## Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

By default `LLM_PROVIDER=mock`, so the app runs end-to-end with a placeholder
response and no API key required. To use a real model, edit `.env`:

```bash
# Anthropic (Claude vision)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# or OpenAI (GPT-4o vision)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 — upload an image and click "Generate Prompt".

## API

`POST /api/prompt` — multipart form with an `image` file field, returns `{"prompt": "..."}`.
`GET /api/health` — returns the active provider for debugging.
