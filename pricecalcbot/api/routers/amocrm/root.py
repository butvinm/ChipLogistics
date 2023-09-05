"""Root router of AmoCRM API."""

from fastapi import APIRouter

from pricecalcbot.api.routers.amocrm import auth

router = APIRouter(prefix='/amocrm', tags=['AmoCRM'])
router.include_router(auth.router)
