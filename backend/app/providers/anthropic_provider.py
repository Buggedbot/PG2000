import base64

from .base import PromptProvider
from .prompts import DEFAULT_MODE, MODE_PROMPTS, improve_prompt_system_prompt


class AnthropicProvider(PromptProvider):
    def __init__(self, api_key: str, model: str):
        from anthropic import Anthropic

        self._client = Anthropic(api_key=api_key)
        self._model = model

    def _complete(self, system: str, user_text: str, image: tuple[str, str] | None = None) -> str:
        content = []
        if image is not None:
            mime_type, encoded = image
            content.append(
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": mime_type, "data": encoded},
                }
            )
        content.append({"type": "text", "text": user_text})

        response = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": content}],
        )
        return "".join(block.text for block in response.content if block.type == "text").strip()

    def generate_from_image(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        encoded = base64.standard_b64encode(image_bytes).decode("utf-8")
        return self._complete(
            MODE_PROMPTS[mode],
            "Write the detailed prompt for this image.",
            image=(mime_type, encoded),
        )

    def generate_from_idea(self, idea: str, mode: str = DEFAULT_MODE) -> str:
        return self._complete(MODE_PROMPTS[mode], f"My idea: {idea}")

    def improve_prompt(self, prompt: str, mode: str = DEFAULT_MODE) -> str:
        return self._complete(improve_prompt_system_prompt(mode), prompt)
