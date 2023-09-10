"""Telegram webhook router."""


from typing import Annotated

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import SecretStr

from pricecalcbot.api.routers.bot.deps import (
    get_articles_service,
    get_bot,
    get_dispatcher,
)
from pricecalcbot.bot.handler_result import HandlerResult
from pricecalcbot.config import get_bot_secret
from pricecalcbot.core.articles.service import ArticlesService

router = APIRouter(prefix='/webhook')


SecretHeader = Header(alias='X-Telegram-Bot-Api-Secret-Token')


@router.post('/')
async def handle_update(  # noqa: WPS211
    update: Update,
    secret: Annotated[SecretStr, SecretHeader],
    bot: Annotated[Bot, Depends(get_bot)],
    dispatcher: Annotated[Dispatcher, Depends(get_dispatcher)],
    expected_secret: Annotated[str, Depends(get_bot_secret)],
    service: Annotated[ArticlesService, Depends(get_articles_service)],
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
        service: Articles service.

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
        articles_service=service,
    )
