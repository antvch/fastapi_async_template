from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from asyncio import current_task

import os

class ModelBase(DeclarativeBase): pass

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DB_URL = "postgresql+asyncpg://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME

engine = create_async_engine(
    DB_URL,
    echo=True,
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