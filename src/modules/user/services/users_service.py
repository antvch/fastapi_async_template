from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db import get_session
from modules.user.models.user import User


class UsersService:
    """Сервис, инкапсулирующий в себе всю логику по работе с пользователем в базе данных."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name: str) -> User:
        """
        Создаёт пользователя.

        :param name: Имя пользователя
        :type name: str

        :returns: User
        """
        user = User(name=name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all_users(self) -> list[User]:
        """
        Возвращает всех пользователей.

        :returns: list[User]
        """
        db_result = await self.session.execute(select(User))
        return db_result.scalars().all()

    async def get_user(self, user_id: int) -> User | None:
        """
        Возвращает пользователя по его id.

        :param user_id: Айди юзера
        :type user_id: int

        :returns: User | None
        """
        return await self.session.get(User, user_id)

    async def delete_user(self, user_id: int):
        """
        Удаляет пользователя по его id.

        :param user_id: Айди юзера
        :type user_id: int
        """
        await self.session.execute(
            delete(User).where(User.id == user_id),
        )
        await self.session.commit()


def get_users_service(
        session: AsyncSession = Depends(get_session),  # noqa: B008, WPS404
) -> UsersService:
    """
    Функция используется для Dependency-injection. Возвращает сервис пользователей.

    :param session: Сессия SQLAlchemy
    :type session: AsyncSession
    :returns: UsersService
    """
    return UsersService(session=session)
