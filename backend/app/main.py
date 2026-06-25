from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from .config import settings
from .providers.factory import get_provider
from .providers.prompts import DEFAULT_MODE, IMAGE_INPUT_MODES, MODE_PROMPTS

app = FastAPI(title="PG2000 Prompt Generator")

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"


def _validate_mode(mode: str) -> None:
    if mode not in MODE_PROMPTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported mode: {mode!r} (expected one of {sorted(MODE_PROMPTS)})",
        )


@app.post("/api/prompt")
async def generate_prompt(
    mode: str = Form(DEFAULT_MODE),
    image: UploadFile | None = None,
    idea: str | None = Form(None),
):
    _validate_mode(mode)

    try:
        provider = get_provider()
        if mode in IMAGE_INPUT_MODES:
            if image is None or not image.content_type or not image.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="This mode requires an image upload")

            image_bytes = await image.read()
            if not image_bytes:
                raise HTTPException(status_code=400, detail="Uploaded image is empty")
            if len(image_bytes) > settings.max_image_bytes:
                raise HTTPException(status_code=413, detail="Image exceeds maximum allowed size")

            prompt = provider.generate_from_image(image_bytes, image.content_type, mode)
        else:
            if not idea or not idea.strip():
                raise HTTPException(status_code=400, detail="This mode requires an 'idea' text field")

            prompt = provider.generate_from_idea(idea.strip(), mode)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"prompt": prompt, "mode": mode}


@app.post("/api/improve")
async def improve_prompt(prompt: str = Form(...), mode: str = Form(DEFAULT_MODE)):
    _validate_mode(mode)

    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt to improve must not be empty")

    try:
        provider = get_provider()
        improved = provider.improve_prompt(prompt.strip(), mode)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"prompt": improved, "mode": mode}


@app.get("/api/health")
async def health():
    return {"status": "ok", "provider": settings.llm_provider}


if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
