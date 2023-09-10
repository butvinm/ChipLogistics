"""Articles menu views."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.articles import (
    ArticlesCreateCallback,
    ArticlesDeleteArticleCallback,
    ArticlesOpenArticleCallback,
    ArticlesOpenListCallback,
    ArticlesOpenMenuCallback,
)
from pricecalcbot.bot.callbacks.menu import MenuOpenCallback
from pricecalcbot.bot.texts.articles import (
    ARTICLE_DESCRIPTION,
    BACK_TO_ARTICLES_MENU,
    BACK_TO_LIST,
    BACK_TO_MENU,
    CREATE_BTN,
    DELETE_BTN,
    DELETED_MESSAGE,
    LIST_TITLE,
    OPEN_LIST_BTN,
    TITLE,
)
from pricecalcbot.models.articles import ArticleInfo

back_to_menu_btns = [
    [
        InlineKeyboardButton(
            text=BACK_TO_MENU,
            callback_data=MenuOpenCallback().pack(),
        ),
    ],
]
back_to_articles_menu_kb = [
    [
        InlineKeyboardButton(
            text=BACK_TO_ARTICLES_MENU,
            callback_data=ArticlesOpenMenuCallback().pack(),
        ),
    ],
]
back_to_list_btns = [
    [
        InlineKeyboardButton(
            text=BACK_TO_LIST,
            callback_data=ArticlesOpenListCallback().pack(),
        ),
    ],
]


articles_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
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
    ] + back_to_menu_btns,
)


async def show_articles_menu(message: Message) -> None:
    """Show articles management menu.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.edit_text(
        text=TITLE,
        reply_markup=articles_menu_kb,
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
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=article.name,
                    callback_data=ArticlesOpenArticleCallback(
                        article_id=article.id,
                    ).pack(),
                ),
            ]
            for article in articles
            if article.id is not None
        ] + back_to_articles_menu_kb,
    )


async def show_articles_list(
    message: Message,
    articles: list[ArticleInfo],
) -> None:
    """Show articles list.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        articles: Articles list.
    """
    await message.edit_text(
        text=LIST_TITLE,
        reply_markup=build_articles_list_kb(articles),
    )


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
                    callback_data=ArticlesDeleteArticleCallback(
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


async def show_article_menu(
    message: Message,
    article_id: str,
    article: ArticleInfo,
) -> None:
    """Show article info and delete button.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        article_id: Article id.
        article: Article info.
    """
    await message.edit_text(
        text=build_article_text(article),
        reply_markup=build_article_kb(article_id),
    )


deleted_article_kb = InlineKeyboardMarkup(inline_keyboard=back_to_list_btns)


async def show_deleted_article(message: Message) -> None:
    """Show article deleting message.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.edit_text(
        text=DELETED_MESSAGE,
        reply_markup=deleted_article_kb,
    )
