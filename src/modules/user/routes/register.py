from fastapi import APIRouter, Depends

from modules.user.schemas.user_request import UserRequest
from modules.user.schemas.user_response import UserResponse
from modules.user.services.users_service import UsersService, get_users_service

router = APIRouter(
    prefix='/users',
    tags=['ModuleName'],
)


@router.post('')
async def create_user(
        user_request: UserRequest,
        users_service: UsersService = Depends(get_users_service),  # noqa: B008, WPS404
) -> dict:
    """
    Добавление нового пользователя.

    :param user_request: Параметры для создания нового пользователя
    :type user_request: UserRequest

    :param users_service: Сервис пользователей
    :type users_service: UsersService

    :returns: dict
    """
    user = await users_service.create_user(name=user_request.name)
    return {'success': 1, 'user': UserResponse(**user.as_dict())}
