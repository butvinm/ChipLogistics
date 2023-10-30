"""Telegram webhook router."""


from typing import Annotated

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import SecretStr

from chip_logistics.api.routers.bot.deps import (
    get_articles_repo,
    get_bot,
    get_currencies_service,
    get_dispatcher,
)
from chip_logistics.api.routers.deps import get_amocrm_client
from chip_logistics.bot.handler_result import HandlerResult
from chip_logistics.config import get_bot_secret
from chip_logistics.core.amocrm.client import AmoCRMClient
from chip_logistics.core.articles.currencies import CurrenciesService
from chip_logistics.core.articles.repo import ArticlesRepository

router = APIRouter(prefix='/webhook')


SecretHeader = Header(alias='X-Telegram-Bot-Api-Secret-Token')


ArticlesRepoDep = Annotated[ArticlesRepository, Depends(get_articles_repo)]
CurrenciesServiceDep = Annotated[
    CurrenciesService,
    Depends(get_currencies_service),
]
AmoCRMServiceDep = Annotated[AmoCRMClient, Depends(get_amocrm_client)]


@router.post('/')
async def handle_update(  # noqa: WPS211
    update: Update,
    secret: Annotated[SecretStr, SecretHeader],
    bot: Annotated[Bot, Depends(get_bot)],
    dispatcher: Annotated[Dispatcher, Depends(get_dispatcher)],
    expected_secret: Annotated[str, Depends(get_bot_secret)],
    articles_repo: ArticlesRepoDep,
    currencies_service: CurrenciesServiceDep,
    amocrm_client: AmoCRMServiceDep,
) -> HandlerResult:
    """Handle telegram update and propagate to aiogram dispatcher.

    See https://core.telegram.org/bots/api
    and https://docs.aiogram.dev/en/latest/dispatcher/index.html
    for details about update.

    Args:
        update: Telegram event update.
        bot: Aiogram Bot instance.
        dispatcher: Aiogram dispatcher instance.
        expected_secret: Secret for request verification. See `config.py`.
        secret: Request secret.
        articles_repo: Articles storage.
        currencies_service: Currencies operations provider.
        amocrm_client: AmoCRM client.

    Raises:
        HTTPException: 401 if secret is invalid.

    Returns:
        Result of update processing.
    """
    if secret.get_secret_value() != expected_secret:
        raise HTTPException(
            detail='Invalid secret',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return await dispatcher.feed_update(  # type: ignore
        bot,
        update=update,
        articles_repo=articles_repo,
        currencies_service=currencies_service,
        amocrm_client=amocrm_client,
    )
