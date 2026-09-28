from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration read from environment variables (or a .env file), like Rails credentials + ENV."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://kb:kb@localhost:5432/kb"
    api_key: SecretStr = SecretStr("dev-key")  # required in the X-API-Key header for write endpoints
    github_token: SecretStr | None = None  # SecretStr: masked when printed or logged


@lru_cache
def get_settings() -> Settings:
    return Settings()
