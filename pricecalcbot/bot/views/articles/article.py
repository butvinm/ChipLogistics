"""Article panel view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.articles import (
    DeleteArticleCallback,
    OpenArticlesListCallback,
)
from pricecalcbot.bot.texts.articles import (
    ARTICLE_DESCRIPTION,
    BACK_TO_LIST,
    DELETE_BTN,
    DELETED_MESSAGE,
)
from pricecalcbot.models.articles import ArticleInfo

back_to_list_btns = [
    [
        InlineKeyboardButton(
            text=BACK_TO_LIST,
            callback_data=OpenArticlesListCallback().pack(),
        ),
    ],
]


def build_article_kb(article_id: str) -> InlineKeyboardMarkup:
    """Create keyboard for article menu.

    Args:
        article_id: Article id.

    Returns:
        Keyboard with delete button.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DELETE_BTN,
                    callback_data=DeleteArticleCallback(
                        article_id=article_id,
                    ).pack(),
                ),
            ],
        ] + back_to_list_btns,
    )


def build_article_text(article: ArticleInfo) -> str:
    """Create text with article description.

    Args:
        article: Article data.

    Returns:
        Article description.
    """
    return ARTICLE_DESCRIPTION.format(
        name=article.name,
        duty_fee_ratio=article.duty_fee_ratio,
    )


async def send_article_menu(
    message: Message,
    article_id: str,
    article: ArticleInfo,
) -> None:
    """Send article info and delete button.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        article_id: Article id.
        article: Article info.
    """
    await message.answer(
        text=build_article_text(article),
        reply_markup=build_article_kb(article_id),
    )

deleted_article_kb = InlineKeyboardMarkup(inline_keyboard=back_to_list_btns)


async def send_deleted_article(message: Message) -> None:
    """Send article deleting message.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=DELETED_MESSAGE,
        reply_markup=deleted_article_kb,
    )
