from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # AI Provider Configuration
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(None, env="ANTHROPIC_API_KEY")
    ai_provider: str = Field("openai", env="AI_PROVIDER")
    ai_model: str = Field("gpt-4o-mini", env="AI_MODEL")

    # Output Configuration
    output_dir: str = Field("output", env="OUTPUT_DIR")

    # Processing Configuration
    max_transcript_length: int = Field(10000, env="MAX_TRANSCRIPT_LENGTH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
