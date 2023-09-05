"""Root application API router."""


from fastapi import APIRouter

from pricecalcbot.api.routers.amocrm.root import router as amocrm_router

router = APIRouter(prefix='/api/v1')
router.include_router(amocrm_router)
