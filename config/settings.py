import os
from pydantic import HttpUrl
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base URLs
    base_url: HttpUrl = "https://demo.realworld.show"
    api_base_url: HttpUrl = "https://demo.realworld.show/api"

    # Timeouts (in milliseconds for Playwright, seconds for HTTPX)
    default_timeout_ms: int = 10000
    api_timeout_sec: float = 10.0

    user_email: str = Field(
        default="testuser_conduit@example.com",
        env="USER_EMAIL"
    )
    user_password: str = Field(
        default="TestPassword123!",
        env="USER_PASSWORD"
    )

    # Execution Settings
    headless: bool = True
    slow_mo: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,  # Ignores empty env strings if they slip through
        extra="ignore"
    )


# Global settings instance
settings = Settings()
