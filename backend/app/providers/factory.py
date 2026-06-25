from functools import lru_cache

from ..config import settings
from .base import PromptProvider
from .mock_provider import MockProvider


@lru_cache
def get_provider() -> PromptProvider:
    provider = settings.llm_provider

    if provider == "mock":
        return MockProvider()

    if provider == "anthropic":
        if not settings.anthropic_api_key:
            raise RuntimeError("LLM_PROVIDER=anthropic requires ANTHROPIC_API_KEY to be set")
        from .anthropic_provider import AnthropicProvider

        return AnthropicProvider(settings.anthropic_api_key, settings.anthropic_model)

    if provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("LLM_PROVIDER=openai requires OPENAI_API_KEY to be set")
        from .openai_provider import OpenAIProvider

        return OpenAIProvider(settings.openai_api_key, settings.openai_model)

    if provider == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError("LLM_PROVIDER=gemini requires GEMINI_API_KEY to be set")
        from .gemini_provider import GeminiProvider

        return GeminiProvider(settings.gemini_api_key, settings.gemini_model)

    raise RuntimeError(
        f"Unknown LLM_PROVIDER: {provider!r} (expected mock, anthropic, openai, or gemini)"
    )
