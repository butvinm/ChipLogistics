"""Root aiogram api router."""


from fastapi import APIRouter

from chip_logistics.api.routers.bot.webhook import router as webhook_router

router = APIRouter(prefix='/bot', tags=['Bot'])
router.include_router(webhook_router)
