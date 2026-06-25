import json

from .base import PromptProvider
from .prompts import DEFAULT_FORMAT, DEFAULT_MODE

IMAGE_EXAMPLES = {
    "image_generation": "a vivid, highly detailed photograph, dramatic lighting, sharp focus, 8k",
    "text_generation": "write a short, evocative story inspired by this scene, warm tone, under 200 words",
}


class MockProvider(PromptProvider):
    """Returns placeholder prompts without calling any external API.

    Useful for local development and testing the upload/idea/improve flows
    before a real LLM_PROVIDER and API key are configured.
    """

    def _format(self, mode: str, output_format: str, **fields: str) -> str:
        if output_format == "json":
            return json.dumps({"mode": mode, **fields}, indent=2)
        return " ".join(fields.values())

    def generate_from_image(
        self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE, output_format: str = DEFAULT_FORMAT
    ) -> str:
        size_kb = len(image_bytes) / 1024
        example = IMAGE_EXAMPLES.get(mode, IMAGE_EXAMPLES["image_generation"])
        return self._format(
            mode,
            output_format,
            note=f"[mock provider] detailed {mode} prompt would appear here",
            example=example,
            received=f"received a {mime_type} image, {size_kb:.1f} KB",
            hint="set LLM_PROVIDER=anthropic, openai, or gemini with an API key to use a real model",
        )

    def generate_from_idea(self, idea: str, mode: str = DEFAULT_MODE, output_format: str = DEFAULT_FORMAT) -> str:
        return self._format(
            mode,
            output_format,
            note=f"[mock provider] detailed {mode} story prompt would appear here",
            idea=idea,
            hint="set LLM_PROVIDER=anthropic, openai, or gemini with an API key to use a real model",
        )

    def improve_prompt(self, prompt: str, mode: str = DEFAULT_MODE, output_format: str = DEFAULT_FORMAT) -> str:
        return self._format(
            mode,
            output_format,
            note=f"[mock provider] an improved version of this prompt for {mode} would appear here",
            original=prompt,
            hint="set LLM_PROVIDER=anthropic, openai, or gemini with an API key to use a real model",
        )
