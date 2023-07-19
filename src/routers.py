from fastapi import APIRouter

from .modules.user.router import router as user_router

router = APIRouter()

router.include_router(user_router)