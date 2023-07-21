from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from asyncio import current_task

from .settings import env_vars


class ModelBase(DeclarativeBase):
    pass

DB_URL = (
    f"postgresql+asyncpg://" \
    f"{env_vars.db_user}:" \
    f"{env_vars.db_password}@" \
    f"{env_vars.db_host}:" \
    f"{env_vars.db_port}/" \
    f"{env_vars.db_name}"
)


engine = create_async_engine(
    DB_URL,
    echo=True,  # SQL query to terminal
    future=True,
)


async def get_session() -> AsyncSession:
    async_session = async_scoped_session(
        async_sessionmaker(
            engine,
            class_=AsyncSession,
        ),
        scopefunc=current_task
    )

    async with async_session() as session:
        yield session
