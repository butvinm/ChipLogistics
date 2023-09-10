"""Articles menu views."""


from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pricecalcbot.bot.callbacks.articles import (
    ArticlesCreateCallback,
    ArticlesOpenArticle,
    ArticlesOpenListCallback,
)
from pricecalcbot.bot.texts.articles import (
    CREATE_BTN,
    LIST_TITLE,
    OPEN_LIST_BTN,
    TITLE,
)
from pricecalcbot.core.articles.service import ArticlesService
from pricecalcbot.models.articles import ArticleInfo

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=OPEN_LIST_BTN,
            callback_data=ArticlesOpenListCallback().pack(),
        ),
    ],
    [
        InlineKeyboardButton(
            text=CREATE_BTN,
            callback_data=ArticlesCreateCallback().pack(),
        ),
    ],
])


async def show_menu(bot: Bot, chat_id: int) -> None:
    """Show articles management menu.

    Args:
        bot: Bot instance.
        chat_id: Chat id.
    """
    await bot.send_message(
        chat_id,
        text=TITLE,
        reply_markup=menu_kb,
    )


def build_articles_list_kb(
    articles: list[ArticleInfo],
) -> InlineKeyboardMarkup:
    """Create keyboard with articles buttons.

    Args:
        articles: Articles info.

    Returns:
        Inline keyboard with buttons for navigation to article menu.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=article.name,
                callback_data=ArticlesOpenArticle(
                    article_id=article.id,
                ).pack(),
            ),
        ]
        for article in articles
        if article.id is not None
    ])


async def show_articles_list(
    bot: Bot,
    chat_id: int,
    articles_service: ArticlesService,
) -> None:
    """Show articles list.

    Args:
        bot: Bot instance.
        chat_id: Chat id.
        articles_service: Articles service.
    """
    articles = await articles_service.find_articles()
    await bot.send_message(
        chat_id,
        text=LIST_TITLE,
        reply_markup=build_articles_list_kb(articles),
    )
