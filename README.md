# PG2000

Prompting specialist:
- Upload (or paste) an image to reverse-engineer it into a detailed prompt for AI
  image generators (Midjourney, Stable Diffusion, DALL-E, etc.) or for text-writing
  assistants based on what's in the image.
- Give a short idea to expand into a detailed video-generation prompt/story.
- Paste any existing prompt and have it improved for the selected target.
- Choose plain text or JSON output, and check the mode-aware tips panel for
  prompting techniques.

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

# or Gemini (free tier — get a key at https://aistudio.google.com/apikey)
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
```

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 — upload an image (or, for video mode, type an idea)
and click "Generate Prompt".

## API

`POST /api/prompt` — multipart form with `mode` (`image_generation` | `text_generation` |
`video_generation`), `format` (`text` | `json`, defaults to `text`), and either an `image`
file field (image-based modes) or an `idea` text field (video mode). Returns
`{"prompt": "...", "mode": "...", "format": "..."}`.

`POST /api/improve` — multipart form with `prompt`, `mode`, and `format`, returns the
improved prompt for that target.

`GET /api/health` — returns the active provider for debugging.
