from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db import get_session
from modules.user.models.user import User


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name: str) -> User:
        """Создаёт пользователя."""

        user = User(name=name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all_users(self) -> list[User]:
        """Возвращает всех пользователей."""

        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_user(self, user_id: int) -> User | None:
        """Возвращает пользователя по его id."""

        user = await self.session.get(User, user_id)
        return user

    async def delete_user(self, user_id: int):
        """Удаляет пользователя по его id."""

        await self.session.execute(delete(User).where(User.id == user_id))
        await self.session.commit()


def get_users_service(
        session: AsyncSession = Depends(get_session)
) -> UsersService:
    return UsersService(session=session)
