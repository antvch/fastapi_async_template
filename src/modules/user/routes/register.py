from fastapi import APIRouter, Depends

from modules.user.schemas.user_request import UserRequest
from modules.user.services.users_service import UsersService, get_users_service

router = APIRouter(
    prefix="/users",
    tags=["ModuleName"]
)


@router.post("")
async def create_user(
        user_request: UserRequest,
        users_service: UsersService = Depends(get_users_service),
):
    """
    Добавление нового пользователя
    """
    user = await users_service.create_user(name=user_request.name)
    return {"success": 1, "user": user}
