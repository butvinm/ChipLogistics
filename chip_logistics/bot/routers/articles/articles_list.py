"""Articles list routes."""


from aiogram import Router
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.articles import OpenArticlesListCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.views.articles.articles_list import send_articles_list
from chip_logistics.core.articles.articles import find_articles
from chip_logistics.core.articles.repo import ArticlesRepository

router = Router(name='articles/list')


@router.callback_query(
    OpenArticlesListCallback.filter(),
    ExtractMessage,
)
async def open_articles_list(
    callback_query: CallbackQuery,
    message: Message,
    articles_repo: ArticlesRepository,
) -> HandlerResult:
    """Open articles list.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        articles_repo: Articles storage.

    Returns:
        Always success.
    """
    articles = await find_articles(articles_repo)
    await send_articles_list(message, articles)
    return Ok()
