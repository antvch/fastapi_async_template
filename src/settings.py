from pydantic_settings import BaseSettings


class Postgres(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: int

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'DB_'

    def get_dsn(self) -> str:
        """
        Возвращает dsn строку для подключения к базе данных через SQLAlchemy.

        :returns: str
        """
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'  # noqa: E501, WPS221


class Settings(BaseSettings):
    """Init settings."""

    postgres: Postgres = Postgres()

    # frontend
    frontend_urls: str | list[str] | None

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
