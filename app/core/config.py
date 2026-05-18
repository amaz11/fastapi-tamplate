from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central place for app settings. Override via .env (see .env.example)."""

    app_name: str = "FastAPI Template"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    secret_key: str = Field(default="dev-only-change-me")
    access_token_expire_minutes: int = 30
    jwt_algorithm: str = "HS256"

    # Default: local SQLite. For MySQL: mysql+pymysql://user:pass@host:3306/dbname
    database_url: str = "sqlite:///./dev.db"
    database_track_modifications: bool = False

    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_headers: list[str] = Field(default_factory=lambda: ["*"])

    log_level: str = "INFO"
    enable_demo_middleware: bool = False
    default_page_size: int = 20
    max_page_size: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
