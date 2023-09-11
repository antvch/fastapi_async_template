from fastapi import Depends

from db import get_async_sessionmaker
from modules.user.models.user import UserModel
from services.base_postgres import DatabaseService


class UsersService(DatabaseService):
    """Сервис, инкапсулирующий в себе всю логику по работе с пользователем в базе данных."""

    model = UserModel

    async def create_user(self, name: str) -> UserModel:
        """
        Создаёт пользователя.

        :param name: Имя пользователя
        :type name: str

        :returns: UserModel
        """
        return await self._add(name=name)

    async def get_all_users(self) -> list[UserModel]:
        """
        Возвращает всех пользователей.

        :returns: list[UserModel]
        """
        return await self._get_all()

    async def get_user(self, user_id: int) -> UserModel | None:
        """
        Возвращает пользователя по его id.

        :param user_id: Айди юзера
        :type user_id: int

        :returns: UserModel | None
        """
        return await self._get_one(self.model.id == user_id)

    async def delete_user(self, user_id: int):
        """
        Удаляет пользователя по его id.

        :param user_id: Айди юзера
        :type user_id: int
        """
        await self._delete(self.model.id == user_id)


def get_users_service(
        async_session=Depends(get_async_sessionmaker),  # noqa: WPS404, B008
) -> UsersService:
    """
    Функция используется для Dependency-injection. Возвращает сервис пользователей.

    :param async_session: Сессия SQLAlchemy
    :returns: UsersService
    """
    return UsersService(async_session=async_session)
