"""Articles list view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from chip_logistics.bot.callbacks.articles import (
    OpenArticleCallback,
    OpenArticlesMenuCallback,
)
from chip_logistics.bot.texts.articles import BACK_TO_ARTICLES_MENU, LIST_TITLE
from chip_logistics.models.articles import ArticleInfo

back_to_articles_menu_kb = [
    [
        InlineKeyboardButton(
            text=BACK_TO_ARTICLES_MENU,
            callback_data=OpenArticlesMenuCallback().pack(),
        ),
    ],
]


def build_articles_list_kb(
    articles: list[ArticleInfo],
) -> InlineKeyboardMarkup:
    """Create keyboard with articles buttons.

    Args:
        articles: Articles info.

    Returns:
        Inline keyboard with buttons for navigation to article menu.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=article.name,
                    callback_data=OpenArticleCallback(
                        article_id=article.id,
                    ).pack(),
                ),
            ]
            for article in articles
            if article.id is not None
        ] + back_to_articles_menu_kb,
    )


async def send_articles_list(
    message: Message,
    articles: list[ArticleInfo],
) -> None:
    """Send articles list.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        articles: Articles list.
    """
    await message.answer(
        text=LIST_TITLE,
        reply_markup=build_articles_list_kb(articles),
    )
