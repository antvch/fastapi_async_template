from fastapi import APIRouter, Depends

from exceptions import NotFoundError
from modules.user.middlewares.example_middleware import example_middleware
from modules.user.schemas.user_response import UserResponse
from modules.user.services.users_service import UsersService, get_users_service

router = APIRouter(
    prefix='/users',
    tags=['ModuleName'],
)


@router.get('')
async def get_users(
        users_service: UsersService = Depends(get_users_service),  # noqa: B008, WPS404
) -> list[UserResponse]:
    """
    Возвращает список пользователей.

    :param users_service: Сервис пользователей
    :type users_service: UsersService

    :returns: list[UserResponse]
    """
    return [UserResponse(**user.as_dict()) for user in await users_service.get_all_users()]


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        users_service: UsersService = Depends(get_users_service),  # noqa: B008, WPS404
) -> UserResponse:
    """
    Возвращает пользователя по id.

    :param user_id: Айди пользователя
    :type user_id: int

    :param users_service: Сервис пользователей
    :type users_service: UsersService

    :returns: UserResponse

    :raises NotFoundError: Пользователь не найден
    """
    user = await users_service.get_user(user_id=user_id)

    if not user:
        raise NotFoundError('Пользователь не найден')

    return UserResponse(**user.as_dict())


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        users_service: UsersService = Depends(get_users_service),  # noqa: B008, WPS404
        example_middleware=Depends(example_middleware),  # noqa: B008, WPS404, WPS442
) -> dict:
    """
    Удаляет пользователя по id.

    :param user_id: Айди пользователя
    :type user_id: int

    :param users_service: Сервис пользователей
    :type users_service: UsersService

    :param example_middleware: Мидлварь

    :returns: dict

    :raises NotFoundError: Пользователь не найден
    """
    user = await users_service.get_user(user_id=user_id)
    if not user:
        raise NotFoundError('Пользователь не найден')

    await users_service.delete_user(user_id=user_id)
    return {'success': 1}
