"""FastAPI application factory."""

from fastapi import FastAPI

from pricecalcbot.api.routers.amocrm.root import router as amocrm_router
from pricecalcbot.api.routers.bot.root import router as bot_router


def init_app() -> FastAPI:
    """Initialize FastAPI application.

    Include API routers and set up dependencies.

    Returns:
        Application instance.
    """
    app = FastAPI()
    app.include_router(amocrm_router)
    app.include_router(bot_router)
    return app
