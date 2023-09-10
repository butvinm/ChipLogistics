"""Articles list routes."""


from aiogram import Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import OpenArticlesListCallback
from pricecalcbot.bot.filters.extract_message import ExtractMessage
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.articles.articles_list import show_articles_list
from pricecalcbot.core.articles.service import ArticlesService

router = Router(name='articles/list')


@router.callback_query(
    OpenArticlesListCallback.filter(),
    ExtractMessage,
)
async def open_articles_list(
    callback_query: CallbackQuery,
    message: Message,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Open articles list.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        articles_service: Articles service.

    Returns:
        Always success.
    """
    articles = await articles_service.find_articles()
    await show_articles_list(message, articles)
    return Ok()
