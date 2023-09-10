"""Articles menu route."""


from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import OpenArticlesMenuCallback
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.articles.menu import show_articles_menu

router = Router(name='articles/menu')


@router.callback_query(
    OpenArticlesMenuCallback.filter(),
    F.message.as_('message'),
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
) -> HandlerResult:
    """Open articles menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.

    Returns:
        Always success.
    """
    await show_articles_menu(message)
    return Ok()
