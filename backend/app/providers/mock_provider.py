from .base import ImagePromptProvider
from .prompts import DEFAULT_MODE


class MockProvider(ImagePromptProvider):
    """Returns a placeholder prompt without calling any external API.

    Useful for local development and testing the upload/response flow
    before a real LLM_PROVIDER and API key are configured.
    """

    def generate_prompt(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        size_kb = len(image_bytes) / 1024
        example = (
            "a vivid, highly detailed photograph, dramatic lighting, sharp focus, 8k"
            if mode == "image_generation"
            else "write a short, evocative story inspired by this scene, warm tone, under 200 words"
        )
        return (
            f"[mock provider] detailed {mode} prompt would appear here, "
            f'e.g. "{example}" '
            f"(received a {mime_type} image, {size_kb:.1f} KB). "
            f"Set LLM_PROVIDER=anthropic or LLM_PROVIDER=openai with an API key to use a real model."
        )
