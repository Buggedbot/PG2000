import base64

from .base import ImagePromptProvider
from .prompts import DEFAULT_MODE, MODE_PROMPTS


class AnthropicProvider(ImagePromptProvider):
    def __init__(self, api_key: str, model: str):
        from anthropic import Anthropic

        self._client = Anthropic(api_key=api_key)
        self._model = model

    def generate_prompt(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        encoded = base64.standard_b64encode(image_bytes).decode("utf-8")
        response = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=MODE_PROMPTS[mode],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": encoded,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Write the detailed prompt for this image.",
                        },
                    ],
                }
            ],
        )
        return "".join(block.text for block in response.content if block.type == "text").strip()
