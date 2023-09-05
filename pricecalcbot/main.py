"""Entry point of application.

Telegram Bot and FastAPI instances are created and
services and dependencies initialized there.
"""


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


app = init_app()
