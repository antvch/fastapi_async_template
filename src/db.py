from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from settings import settings


class ModelBase(DeclarativeBase):
    """Базовая модель SQLAlchemy."""


engine = create_async_engine(
    settings.postgres.get_dsn(),
    echo=True,  # SQL query to terminal
    future=True,
)


async def get_async_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """
    Возвращает SQLAlchemy сессию.

    :returns: async_sessionmaker[AsyncSession]
    """
    return async_sessionmaker(engine, expire_on_commit=False)
