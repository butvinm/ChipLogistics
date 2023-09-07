"""FastAPI application factory."""

from fastapi import FastAPI

from pricecalcbot.api.routers.root import router as root_router


def init_app() -> FastAPI:
    """Initialize FastAPI application.

    Returns:
        Application instance.
    """
    app = FastAPI()
    app.include_router(root_router)
    return app
