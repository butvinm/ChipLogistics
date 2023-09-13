"""Aiogram routers dependencies."""


from typing import Annotated, AsyncGenerator, Optional

from aiogram import Bot, Dispatcher
from deta import Deta
from fastapi import Depends

from chip_logistics.bot.factory import init_bot, init_dispatcher
from chip_logistics.config import get_bot_token
from chip_logistics.core.articles.repo import ArticlesRepository
from chip_logistics.core.articles.service import ArticlesService
from chip_logistics.deta.articles.repo import DetaArticlesRepository
from chip_logistics.deta.deta import get_deta


async def get_bot(
    token: Annotated[str, Depends(get_bot_token)],
) -> Bot:
    """Get aiogram bot instance.

    Args:
        token: Telegram bot token.

    Returns:
        Aiogram bot.
    """
    return init_bot(token)


dispatcher: Optional[Dispatcher] = None


async def get_dispatcher(
    deta: Annotated[Deta, Depends(get_deta)],
) -> Dispatcher:
    """Get dispatcher instance.

    Dispatcher should be a singleton to prevent error on routers re-attachment.

    It is quite a hack to make dependency system consistent.

    Actually, in the Deta Space runtime it will never be called twice
    because application starts on each request.

    It is temporary solution and should be reimplemented.

    Args:
        deta: Deta API.

    Returns:
        Aiogram dispatcher instance.
    """
    global dispatcher  # noqa: WPS420
    if dispatcher is None:
        dispatcher = init_dispatcher(deta)  # noqa: WPS442

    return dispatcher


async def get_articles_repo(
    deta: Annotated[Deta, Depends(get_deta)],
) -> AsyncGenerator[ArticlesRepository, None]:
    """Get articles repository instance.

    Args:
        deta: Deta API.

    Yields:
        Articles repository.
    """
    async with DetaArticlesRepository(deta) as repo:
        yield repo


async def get_articles_service(
    repo: Annotated[ArticlesRepository, Depends(get_articles_repo)],
) -> ArticlesService:
    """Get articles service instance.

    Args:
        repo: Articles repository.

    Returns:
        Articles service.
    """
    return ArticlesService(repo)
