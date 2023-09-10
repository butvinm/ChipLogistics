"""Articles menu routes."""


from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import (
    ArticlesOpenArticleCallback,
    ArticlesOpenListCallback,
    ArticlesOpenMenuCallback,
)
from pricecalcbot.bot.handler_result import Err, HandlerResult, Ok
from pricecalcbot.bot.views.articles import (
    show_article_menu,
    show_articles_list,
    show_menu,
)
from pricecalcbot.core.articles.service import ArticlesService

router = Router(name='articles')


@router.callback_query(
    ArticlesOpenMenuCallback.filter(),
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
    await show_menu(message)
    return Ok()


@router.callback_query(
    ArticlesOpenListCallback.filter(),
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
    ArticlesOpenArticleCallback.filter(),
    F.message.as_('message'),
)
async def open_article(
    callback_query: CallbackQuery,
    callback_data: ArticlesOpenArticleCallback,
    message: Message,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Open article menu.

    Args:
        callback_query: Open menu query.
        callback_data: Callback with article query.
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
