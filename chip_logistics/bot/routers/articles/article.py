"""Article panel routes."""


from aiogram import Router
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.articles import (
    DeleteArticleCallback,
    OpenArticleCallback,
)
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.views.articles.article import (
    send_article_menu,
    send_deleted_article,
)
from chip_logistics.core.articles import articles
from chip_logistics.core.articles.repo import ArticlesRepo

router = Router(name='articles/article')


@router.callback_query(
    OpenArticleCallback.filter(),
    ExtractMessage,
)
async def open_article(
    callback_query: CallbackQuery,
    callback_data: OpenArticleCallback,
    message: Message,
    articles_repo: ArticlesRepo,
) -> HandlerResult:
    """Open article menu.

    Args:
        callback_query: Open menu query.
        callback_data: Callback with article id.
        message: Message where query from.
        articles_repo: Articles storage.

    Returns:
        Ok - Article menu opened successfully.
        Err - Article not found.
    """
    article = await articles.get_article(
        articles_repo,
        callback_data.article_id,
    )
    if article is None:
        return Err(
            message='Article {article_id} not found'.format(
                article_id=callback_data.article_id,
            ),
        )

    await send_article_menu(
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
    articles_repo: ArticlesRepo,
) -> HandlerResult:
    """Delete article.

    Args:
        callback_query: Open menu query.
        callback_data: Callback with article id.
        message: Message where query from.
        articles_repo: Articles storage.

    Returns:
        Ok - Deleted successfully.
        Err - Article not found.
    """
    deleted = await articles.delete_article(
        articles_repo,
        article_id=callback_data.article_id,
    )
    if not deleted:
        return Err(
            message='Article {article_id} not found'.format(
                article_id=callback_data.article_id,
            ),
        )

    await send_deleted_article(message)
    return Ok()
