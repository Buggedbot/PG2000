from abc import ABC, abstractmethod


class ImagePromptProvider(ABC):
    """Analyzes an image and writes a detailed prompt for image-generation tools."""

    @abstractmethod
    def generate_prompt(self, image_bytes: bytes, mime_type: str) -> str:
        ...
