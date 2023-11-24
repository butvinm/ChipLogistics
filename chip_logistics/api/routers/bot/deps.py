"""Aiogram routers dependencies."""


from typing import Annotated, AsyncGenerator, Optional

from aiogram import Bot, Dispatcher
from deta import Deta
from fastapi import Depends

from chip_logistics.bot.factory import init_bot, init_dispatcher
from chip_logistics.config import (
    get_bot_token,
    get_fixer_api_key,
    get_repo_template_name,
)
from chip_logistics.core.articles.currencies import CurrenciesService
from chip_logistics.core.articles.repo import ArticlesRepo, ReportTemplateRepo
from chip_logistics.deta.articles.repo import (
    DetaArticlesRepo,
    DetaReportTemplateRepo,
)
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
) -> AsyncGenerator[ArticlesRepo, None]:
    """Get articles repository instance.

    Args:
        deta: Deta API.

    Yields:
        Articles repository.
    """
    async with DetaArticlesRepo(deta) as repo:
        yield repo


async def get_currencies_service(
    fixer_api_key: Annotated[str, Depends(get_fixer_api_key)],
) -> AsyncGenerator[CurrenciesService, None]:
    """Get currencies service instance.

    Args:
        fixer_api_key: Fixer API key.

    Yields:
        Currencies service.
    """
    async with CurrenciesService(fixer_api_key) as service:
        yield service


async def get_report_template_repo(
    template: Annotated[str, Depends(get_repo_template_name)],
    deta: Annotated[Deta, Depends(get_deta)],
) -> AsyncGenerator[ReportTemplateRepo, None]:
    """Get report templates repo instance.

    Args:
        template: Currently used template.
        deta: Deta API.

    Yields:
        Templates repository.
    """
    async with DetaReportTemplateRepo(template, deta) as repo:
        yield repo
