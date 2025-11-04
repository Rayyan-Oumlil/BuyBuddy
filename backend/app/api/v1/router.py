from fastapi import APIRouter
from .endpoints import health, search, chat, history

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(search.router, tags=["search"])
router.include_router(chat.router, tags=["chat"])
router.include_router(history.router, tags=["history"])

