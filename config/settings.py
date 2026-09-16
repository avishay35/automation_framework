import os
from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base URLs
    base_url: HttpUrl = Field(
        default="https://demo.realworld.show",
        env="BASE_URL"
    )
    api_base_url: HttpUrl = Field(
        default="https://demo.realworld.show/api",
        env="API_BASE_URL"
    )

    # Timeouts
    default_timeout_ms: int = 10000
    api_timeout_sec: float = 10.0

    # Auth
    user_email: str = Field(
        default="testuser_conduit@example.com",
        env="USER_EMAIL"
    )
    user_password: str = Field(
        default="TestPassword123!",
        env="USER_PASSWORD"
    )

    # Execution Settings
    headless: bool = Field(default=True, env="HEADLESS")
    slow_mo: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )


settings = Settings()
