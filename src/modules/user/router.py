from fastapi import APIRouter
from .routes.user import router as user_router
from .routes.register import router as register_router

router = APIRouter()

router.include_router(user_router)
router.include_router(register_router)