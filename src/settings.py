from pydantic_settings import BaseSettings


class Postgres(BaseSettings):
    NAME: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = 'DB_'

    def get_dsn(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'  # noqa: E501


class Settings(BaseSettings):
    """Init settings."""

    POSTGRES: Postgres = Postgres()

    # frontend
    frontend_urls: str | list[str] | None

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
