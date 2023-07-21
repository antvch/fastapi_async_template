from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db import get_session
from ..models.user import User
from ..schemas.user_request import UserRequest

router = APIRouter(
    prefix="/user",
    tags=["ModuleName"]
)

@router.post("")
async def create_user(
    user_request: UserRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Добавление нового пользователя
    """
    user = User(name=user_request.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"success": 1, "user": user}