from .base import PromptProvider
from .prompts import DEFAULT_MODE

IMAGE_EXAMPLES = {
    "image_generation": "a vivid, highly detailed photograph, dramatic lighting, sharp focus, 8k",
    "text_generation": "write a short, evocative story inspired by this scene, warm tone, under 200 words",
}


class MockProvider(PromptProvider):
    """Returns placeholder prompts without calling any external API.

    Useful for local development and testing the upload/idea/improve flows
    before a real LLM_PROVIDER and API key are configured.
    """

    def generate_from_image(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        size_kb = len(image_bytes) / 1024
        example = IMAGE_EXAMPLES.get(mode, IMAGE_EXAMPLES["image_generation"])
        return (
            f"[mock provider] detailed {mode} prompt would appear here, "
            f'e.g. "{example}" '
            f"(received a {mime_type} image, {size_kb:.1f} KB). "
            f"Set LLM_PROVIDER=anthropic or LLM_PROVIDER=openai with an API key to use a real model."
        )

    def generate_from_idea(self, idea: str, mode: str = DEFAULT_MODE) -> str:
        return (
            f'[mock provider] detailed {mode} story prompt expanding on "{idea}" would appear here. '
            f"Set LLM_PROVIDER=anthropic or LLM_PROVIDER=openai with an API key to use a real model."
        )

    def improve_prompt(self, prompt: str, mode: str = DEFAULT_MODE) -> str:
        return (
            f'[mock provider] an improved version of "{prompt}" for {mode} would appear here. '
            f"Set LLM_PROVIDER=anthropic or LLM_PROVIDER=openai with an API key to use a real model."
        )
