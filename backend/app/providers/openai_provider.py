import base64

from .base import PromptProvider
from .prompts import DEFAULT_MODE, MODE_PROMPTS, improve_prompt_system_prompt


class OpenAIProvider(PromptProvider):
    def __init__(self, api_key: str, model: str):
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key)
        self._model = model

    def _complete(self, system: str, user_text: str, image: tuple[str, str] | None = None) -> str:
        user_content = [{"type": "text", "text": user_text}]
        if image is not None:
            mime_type, encoded = image
            user_content.append(
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded}"}}
            )

        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
        )
        return (response.choices[0].message.content or "").strip()

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
