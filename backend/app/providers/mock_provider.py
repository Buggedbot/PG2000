from .base import ImagePromptProvider


class MockProvider(ImagePromptProvider):
    """Returns a placeholder prompt without calling any external API.

    Useful for local development and testing the upload/response flow
    before a real LLM_PROVIDER and API key are configured.
    """

    def generate_prompt(self, image_bytes: bytes, mime_type: str) -> str:
        size_kb = len(image_bytes) / 1024
        return (
            f"[mock provider] detailed image-generation prompt would appear here, "
            f"e.g. \"a vivid, highly detailed photograph, dramatic lighting, sharp focus, 8k\" "
            f"(received a {mime_type} image, {size_kb:.1f} KB). "
            f"Set LLM_PROVIDER=anthropic or LLM_PROVIDER=openai with an API key to use a real model."
        )
