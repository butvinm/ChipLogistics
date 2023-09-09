"""Aiogram routers dependencies."""


from typing import Annotated, Optional

from aiogram import Bot, Dispatcher
from deta import Deta
from fastapi import Depends

from pricecalcbot.bot.factory import init_bot, init_dispatcher
from pricecalcbot.config import get_bot_token
from pricecalcbot.deta.deta import get_deta


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
