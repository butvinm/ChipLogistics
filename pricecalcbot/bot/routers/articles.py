"""Articles menu routes."""


from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import (
    ArticlesOpenListCallback,
    ArticlesOpenMenuCallback,
)
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.articles import show_articles_list, show_menu
from pricecalcbot.core.articles.service import ArticlesService

router = Router(name='articles')


@router.callback_query(
    ArticlesOpenMenuCallback.filter(),
    F.message.as_('message'),
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
    bot: Bot,
) -> HandlerResult:
    """Open articles menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        bot: Bot instance.

    Returns:
        Always success.
    """
    await show_menu(bot, message.chat.id)
    return Ok()


@router.callback_query(
    ArticlesOpenListCallback.filter(),
    F.message.as_('message'),
)
async def open_articles_list(
    callback_query: CallbackQuery,
    message: Message,
    bot: Bot,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Open articles list.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        bot: Bot instance.
        articles_service: Articles service.

    Returns:
        Always success.
    """
    await show_articles_list(bot, message.chat.id, articles_service)
    return Ok()
