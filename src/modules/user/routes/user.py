from fastapi import APIRouter, Depends

from exceptions import NotFoundException
from modules.user.middlewares.example_middleware import example_middleware
from modules.user.schemas.user_response import UserResponse
from modules.user.services.users_service import UsersService, get_users_service

router = APIRouter(
    prefix="/users",
    tags=["ModuleName"]
)


@router.get("")
async def get_users(
        users_service: UsersService = Depends(get_users_service),
):
    """
    Возвращает список пользователей
    """

    users = await users_service.get_all_users()
    return users


@router.get("/{user_id}")
async def get_user(
        user_id: int,
        users_service: UsersService = Depends(get_users_service),
) -> UserResponse:
    """
    Возвращает пользователя по id
    """

    user = await users_service.get_user(user_id=user_id)

    if not user:
        raise NotFoundException("Пользователь не найден")

    return user


@router.delete("/{id}")
async def delete_user(
        user_id: int,
        users_service: UsersService = Depends(get_users_service),
        example_middleware=Depends(example_middleware)
):
    """
    Удаление пользователя по id
    """

    user = await users_service.get_user(user_id=user_id)
    if not user:
        raise NotFoundException("Пользователь не найден")

    await users_service.delete_user(user_id=user_id)
    return {"success": 1}
