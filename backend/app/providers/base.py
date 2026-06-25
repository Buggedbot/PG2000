from abc import ABC, abstractmethod

from .prompts import DEFAULT_MODE


class ImagePromptProvider(ABC):
    """Analyzes an image and writes a detailed prompt for the given target mode
    (e.g. image_generation, text_generation)."""

    @abstractmethod
    def generate_prompt(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        ...
