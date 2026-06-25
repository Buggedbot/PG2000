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


def _get_provider():
    try:
        return get_provider()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _run_provider_call(fn, *args):
    try:
        return fn(*args)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {exc}") from exc


@app.post("/api/prompt")
async def generate_prompt(
    mode: str = Form(DEFAULT_MODE),
    image: UploadFile | None = None,
    idea: str | None = Form(None),
):
    _validate_mode(mode)
    provider = _get_provider()

    if mode in IMAGE_INPUT_MODES:
        if image is None or not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="This mode requires an image upload")

        image_bytes = await image.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded image is empty")
        if len(image_bytes) > settings.max_image_bytes:
            raise HTTPException(status_code=413, detail="Image exceeds maximum allowed size")

        prompt = _run_provider_call(provider.generate_from_image, image_bytes, image.content_type, mode)
    else:
        if not idea or not idea.strip():
            raise HTTPException(status_code=400, detail="This mode requires an 'idea' text field")

        prompt = _run_provider_call(provider.generate_from_idea, idea.strip(), mode)

    return {"prompt": prompt, "mode": mode}


@app.post("/api/improve")
async def improve_prompt(prompt: str = Form(...), mode: str = Form(DEFAULT_MODE)):
    _validate_mode(mode)

    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt to improve must not be empty")

    provider = _get_provider()
    improved = _run_provider_call(provider.improve_prompt, prompt.strip(), mode)

    return {"prompt": improved, "mode": mode}


@app.get("/api/health")
async def health():
    return {"status": "ok", "provider": settings.llm_provider}


if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
