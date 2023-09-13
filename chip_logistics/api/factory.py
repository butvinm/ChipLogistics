"""FastAPI application factory."""

from fastapi import FastAPI

from chip_logistics.api.routers.amocrm.root import router as amocrm_router
from chip_logistics.api.routers.bot.root import router as bot_router


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
