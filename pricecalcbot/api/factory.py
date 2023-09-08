"""FastAPI application factory."""

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from pricecalcbot.api.routers.bot.root import router as bot_router
from pricecalcbot.api.routers.root import router as root_router
from pricecalcbot.api.stubs.bot import BotStub, DispatcherStub, SecretStub


def init_app(
    bot: Bot,
    dispatcher: Dispatcher,
    webhook_secret: str,
) -> FastAPI:
    """Initialize FastAPI application.

    Include API routers and set up dependencies.

    Args:
        bot: Aiogram bot. Dependency of webhook router.
        dispatcher: Aiogram dispatcher. Dependency of webhook router.
        webhook_secret: Telegram webhook secret. Dependency of webhook router.

    Returns:
        Application instance.
    """
    app = FastAPI()
    app.dependency_overrides.update({
        BotStub: lambda: bot,
        DispatcherStub: lambda: dispatcher,
        SecretStub: lambda: webhook_secret,
    })
    app.include_router(root_router)
    app.include_router(bot_router)
    return app
