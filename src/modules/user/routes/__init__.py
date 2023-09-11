from fastapi import APIRouter

from .register import router as register_router
from .user import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(register_router)