from asyncio import current_task

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from settings import settings


class ModelBase(DeclarativeBase):
    """Базовая модель SQLAlchemy."""


engine = create_async_engine(
    settings.postgres.get_dsn(),
    echo=True,  # SQL query to terminal
    future=True,
)


async def get_session() -> AsyncSession:
    """
    Возвращает SQLAlchemy сессию.

    :yields: AsyncSession
    """
    async_session = async_scoped_session(
        async_sessionmaker(
            engine,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )

    async with async_session() as session:
        yield session
