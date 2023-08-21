from fastapi import APIRouter

from modules.user.routes import router as user_router

router = APIRouter()

router.include_router(user_router)
