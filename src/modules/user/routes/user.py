from fastapi import APIRouter, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db import get_session
from ..models.user import User
from ..schemas.user_response import UserResponse
from ..exceptions.not_found import NotFoundException
from ..middlewares.example_middleware import example_middleware

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
    example_middleware = Depends(example_middleware)
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
