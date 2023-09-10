"""Articles menu views."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.articles import (
    ArticlesCreateCallback,
    ArticlesDeleteArticleCallback,
    ArticlesOpenArticleCallback,
    ArticlesOpenListCallback,
)
from pricecalcbot.bot.texts.articles import (
    ARTICLE_DESCRIPTION,
    ARTICLE_NOT_FOUND,
    CREATE_BTN,
    DELETE_BTN,
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


async def show_menu(message: Message) -> None:
    """Show articles management menu.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
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
                callback_data=ArticlesOpenArticleCallback(
                    article_id=article.id,
                ).pack(),
            ),
        ]
        for article in articles
        if article.id is not None
    ])


async def show_articles_list(
    message: Message,
    articles_service: ArticlesService,
) -> None:
    """Show articles list.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        articles_service: Articles service.
    """
    articles = await articles_service.find_articles()
    await message.answer(
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
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=DELETE_BTN,
                callback_data=ArticlesDeleteArticleCallback(
                    article_id=article_id,
                ).pack(),
            ),
        ],
    ])


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
    articles_service: ArticlesService,
) -> bool:
    """Show article info and delete button.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        article_id: Article id.
        articles_service: Articles service.

    Returns:
        True, if article opened successfully.
    """
    article = await articles_service.get_article(article_id)
    if article is None:
        await message.answer(
            text=ARTICLE_NOT_FOUND,
        )
        return False

    await message.answer(
        text=build_article_text(article),
        reply_markup=build_article_kb(article_id),
    )
    return True
