"""Articles menu routes."""


from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import (
    DeleteArticleCallback,
    OpenArticleCallback,
    OpenArticlesListCallback,
    OpenArticlesMenuCallback,
)
from pricecalcbot.bot.handler_result import Err, HandlerResult, Ok
from pricecalcbot.bot.views.articles import (
    show_article_menu,
    show_articles_list,
    show_articles_menu,
    show_deleted_article,
)
from pricecalcbot.core.articles.service import ArticlesService

router = Router(name='articles')


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


@router.callback_query(
    OpenArticlesListCallback.filter(),
    F.message.as_('message'),
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


@router.callback_query(
    OpenArticleCallback.filter(),
    F.message.as_('message'),
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
    F.message.as_('message'),
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
