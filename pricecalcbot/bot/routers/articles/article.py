"""Article panel routes."""


from aiogram import Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import (
    DeleteArticleCallback,
    OpenArticleCallback,
)
from pricecalcbot.bot.filters.extract_message import ExtractMessage
from pricecalcbot.bot.handler_result import Err, HandlerResult, Ok
from pricecalcbot.bot.views.articles.article import (
    show_article_menu,
    show_deleted_article,
)
from pricecalcbot.core.articles.service import ArticlesService

router = Router(name='articles/article')


@router.callback_query(
    OpenArticleCallback.filter(),
    ExtractMessage,
)
async def open_article(
    callback_query: CallbackQuery,
    callback_data: OpenArticleCallback,
    message: Message,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Open article menu.

    Args:
        callback_query: Open menu query.
        callback_data: Callback with article id.
        message: Message where query from.
        articles_service: Articles service.

    Returns:
        Ok - Article menu opened successfully.
        Err - Article not found.
    """
    article = await articles_service.get_article(callback_data.article_id)
    if article is None:
        return Err(
            message='Article {article_id} not found'.format(
                article_id=callback_data.article_id,
            ),
        )

    await show_article_menu(
        message,
        article_id=callback_data.article_id,
        article=article,
    )
    return Ok()


@router.callback_query(
    DeleteArticleCallback.filter(),
    ExtractMessage,
)
async def delete_article(
    callback_query: CallbackQuery,
    callback_data: DeleteArticleCallback,
    message: Message,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Delete article.

    Args:
        callback_query: Open menu query.
        callback_data: Callback with article id.
        message: Message where query from.
        articles_service: Articles service.

    Returns:
        Ok - Deleted successfully.
        Err - Article not found.
    """
    deleted = await articles_service.delete_article(
        article_id=callback_data.article_id,
    )
    if not deleted:
        return Err(
            message='Article {article_id} not found'.format(
                article_id=callback_data.article_id,
            ),
        )

    await show_deleted_article(message)
    return Ok()
