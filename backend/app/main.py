from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from .config import settings
from .providers.factory import get_provider
from .providers.prompts import DEFAULT_MODE, MODE_PROMPTS

app = FastAPI(title="PG2000 Prompt Generator")

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"


@app.post("/api/prompt")
async def generate_prompt(image: UploadFile, mode: str = Form(DEFAULT_MODE)):
    if mode not in MODE_PROMPTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported mode: {mode!r} (expected one of {sorted(MODE_PROMPTS)})",
        )

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty")
    if len(image_bytes) > settings.max_image_bytes:
        raise HTTPException(status_code=413, detail="Image exceeds maximum allowed size")

    try:
        provider = get_provider()
        prompt = provider.generate_prompt(image_bytes, image.content_type, mode)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"prompt": prompt, "mode": mode}


@app.get("/api/health")
async def health():
    return {"status": "ok", "provider": settings.llm_provider}


if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
