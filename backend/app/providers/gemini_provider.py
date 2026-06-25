from .base import PromptProvider
from .prompts import DEFAULT_MODE, MODE_PROMPTS, improve_prompt_system_prompt


class GeminiProvider(PromptProvider):
    def __init__(self, api_key: str, model: str):
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self._genai = genai
        self._model_name = model

    def _complete(self, system: str, user_text: str, image: tuple[str, bytes] | None = None) -> str:
        model = self._genai.GenerativeModel(model_name=self._model_name, system_instruction=system)
        parts = []
        if image is not None:
            mime_type, image_bytes = image
            parts.append({"mime_type": mime_type, "data": image_bytes})
        parts.append(user_text)

        response = model.generate_content(parts)
        return response.text.strip()

    def generate_from_image(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        return self._complete(
            MODE_PROMPTS[mode],
            "Write the detailed prompt for this image.",
            image=(mime_type, image_bytes),
        )

    def generate_from_idea(self, idea: str, mode: str = DEFAULT_MODE) -> str:
        return self._complete(MODE_PROMPTS[mode], f"My idea: {idea}")

    def improve_prompt(self, prompt: str, mode: str = DEFAULT_MODE) -> str:
        return self._complete(improve_prompt_system_prompt(mode), prompt)
