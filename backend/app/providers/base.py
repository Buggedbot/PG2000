from abc import ABC, abstractmethod

from .prompts import DEFAULT_MODE


class PromptProvider(ABC):
    """Writes detailed prompts for image/text/video generation tools, either by
    reverse-engineering an uploaded image, expanding a short text idea, or
    improving a prompt the user already has."""

    @abstractmethod
    def generate_from_image(self, image_bytes: bytes, mime_type: str, mode: str = DEFAULT_MODE) -> str:
        ...

    @abstractmethod
    def generate_from_idea(self, idea: str, mode: str = DEFAULT_MODE) -> str:
        ...

    @abstractmethod
    def improve_prompt(self, prompt: str, mode: str = DEFAULT_MODE) -> str:
        ...
