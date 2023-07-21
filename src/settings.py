import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Init settings."""

    # database
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    # frontend
    frontend_urls: str | list[str] | None

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

env_vars = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
