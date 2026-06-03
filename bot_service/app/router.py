from fastapi import APIRouter

from app.bot.dispatcher import router as handlers_router

router = APIRouter()
router.include_router(handlers_router)
