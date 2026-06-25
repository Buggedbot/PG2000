import base64

from .base import ImagePromptProvider
from .prompts import SYSTEM_PROMPT


class OpenAIProvider(ImagePromptProvider):
    def __init__(self, api_key: str, model: str):
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key)
        self._model = model

    def generate_prompt(self, image_bytes: bytes, mime_type: str) -> str:
        encoded = base64.standard_b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{encoded}"
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Write the detailed image-generation prompt for this image.",
                        },
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                },
            ],
        )
        return (response.choices[0].message.content or "").strip()
