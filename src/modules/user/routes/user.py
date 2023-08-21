from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db import get_session
from modules.user.exceptions import NotFoundException
from modules.user.middlewares.example_middleware import example_middleware
from modules.user.models.user import User
from modules.user.schemas.user_response import UserResponse

router = APIRouter(
    prefix="/user",
    tags=["ModuleName"]
)


@router.get("")
async def get_users(
        session: AsyncSession = Depends(get_session)
):
    """
    Возвращает список пользователей
    """
    result = await session.execute(select(User))
    users = result.scalars().all()

    return users


@router.get("/{id}")
async def get_user(
        id: int,
        session: AsyncSession = Depends(get_session)
) -> UserResponse:
    """
    Возвращает пользователя по id
    """
    user = await session.get(User, id)

    if not user:
        raise NotFoundException("Пользователь не найден")

    return user


@router.delete("/{id}")
async def delete_user(
        id: int,
        session: AsyncSession = Depends(get_session),
        example_middleware=Depends(example_middleware)
):
    """
    Удаление пользователя по id
    """
    user = await session.get(User, id)

    if not user:
        raise NotFoundException("Пользователь не найден")

    await session.execute(delete(User).where(User.id == id))
    await session.commit()

    return {"success": 1}
