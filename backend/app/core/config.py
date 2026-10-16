from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Every value comes from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_version: str = "0.1.0"

    # Postgres (database `qa_app`, with the pgvector extension)
    database_url: str = "postgresql://postgres:postgres@localhost:5432/qa_app"

    # LiteLLM proxy: the only way the app talks to an LLM provider
    litellm_base_url: str = "http://localhost:4000"
    litellm_api_key: str = ""

    # Langfuse
    langfuse_host: str = "http://localhost:3000"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
