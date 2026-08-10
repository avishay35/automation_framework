import os
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base URLs
    base_url: HttpUrl = "https://demo.realworld.show"
    api_base_url: HttpUrl = "https://demo.realworld.show/api"

    # Timeouts (in milliseconds for Playwright, seconds for HTTPX)
    default_timeout_ms: int = 10000
    api_timeout_sec: float = 10.0

    # Test User Credentials (overridable via .env)
    user_email: str = "testuser_conduit@example.com"
    user_password: str = "TestPassword123!"

    # Execution Settings
    headless: bool = True
    slow_mo: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Global settings instance
settings = Settings()