import os


class Settings:
    def __init__(self) -> None:
        self.llm_provider = os.environ.get("LLM_PROVIDER", "mock").lower()
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.anthropic_model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.openai_model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        self.max_image_bytes = int(os.environ.get("MAX_IMAGE_BYTES", 10 * 1024 * 1024))


settings = Settings()
