from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Central place for app settings."""

    app_name: str = "My FastAPI Learning App"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    fake_secret_key: str = "learning-secret"
    database_url: str = "mysql+pymysql://admin:StrongPassword123!@localhost/fastapi_db"
    database_track_modifications: bool = False
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_headers: list[str] = Field(default_factory=lambda: ["*"])

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
