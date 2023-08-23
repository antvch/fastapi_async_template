from typing import Any, Generic, Type, TypeVar, Union, cast

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.elements import BinaryExpression

from models.base import DatabaseModel

ASTERISK = '*'

SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=DatabaseModel)
ExpressionType = Union[BinaryExpression, ClauseElement, bool]


class DatabaseService(Generic[SQLAlchemyModel]):  # noqa: WPS214
    model: Type[SQLAlchemyModel]

    def __init__(
            self,
            async_session: async_sessionmaker[AsyncSession],
            query_model: Type[SQLAlchemyModel] | None = None,
    ) -> None:
        self.async_session = async_session
        self.model = query_model or self.model

    async def _add(
            self,
            **values: Any,  # noqa: WPS110
    ) -> SQLAlchemyModel | None:
        async with self.async_session() as session:
            model_to_add = self.model(**values)
            session.add(model_to_add)
            await session.commit()
            await session.refresh(model_to_add)
        return model_to_add

    async def _get_all(  # noqa: WPS210
            self,
            *clauses: ExpressionType,
            loads: tuple[tuple[Any, Any | None]] | None = None,
    ) -> list[SQLAlchemyModel]:
        statement = select(self.model).where(*clauses)
        if loads is not None:
            for joined_model, subquery_model in loads:
                if subquery_model is None:
                    statement = statement.options(joinedload(joined_model))
                else:
                    statement = statement.options(
                        joinedload(joined_model).subqueryload(subquery_model),
                    )

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            scalars = session_result.scalars().unique().all()

        return cast(list[SQLAlchemyModel], scalars)

    async def _get_all_with_limit_and_offset(
            self,
            *clauses: ExpressionType,
            page_size: int,
            page: int,
            load: Any | None = None,
    ) -> list[SQLAlchemyModel]:
        statement = select(
            self.model,
        ).where(
            *clauses,
        ).limit(
            page_size,
        ).offset(
            (page - 1) * page_size,
        )
        if load is not None:
            statement = statement.options(joinedload(load))

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            scalars = session_result.scalars().unique().all()
        return cast(list[SQLAlchemyModel], scalars)

    async def _get_one(
            self,
            *clauses: ExpressionType,
            load: Any | None = None,
            loads: Any | None = None,
    ) -> SQLAlchemyModel | None:
        statement = select(self.model).where(*clauses)
        if load is not None:
            statement = statement.options(joinedload(load))
        if loads is not None:
            for _ in loads:
                statement = statement.options(joinedload(_))

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            first_scalar_result = session_result.scalars().first()
        return first_scalar_result

    async def _update(self, *clauses: ExpressionType, **values: Any) -> None:  # noqa: WPS110
        async with self.async_session() as session:
            statement = update(self.model).where(*clauses).values(**values)
            await session.execute(statement)
            await session.commit()

    async def _exists(self, *clauses: ExpressionType) -> bool:
        async with self.async_session() as session:
            statement = exists(self.model).where(*clauses).select()
            session_result = (await session.execute(statement)).scalar()
        return cast(bool, session_result)

    async def _delete(self, *clauses: ExpressionType) -> list[SQLAlchemyModel]:
        async with self.async_session() as session:
            statement = delete(self.model).where(*clauses).returning(ASTERISK)
            session_result = (await session.execute(statement)).scalars().all()
            await session.commit()
        return cast(list[SQLAlchemyModel], session_result)

    async def _count(self, *clauses: ExpressionType) -> int:
        statement = select(
            func.count(ASTERISK),
        ).select_from(
            self.model,
        ).where(
            *clauses,
        )

        async with self.async_session() as session:
            async_result = await session.execute(statement)
        return cast(int, async_result.scalar())
