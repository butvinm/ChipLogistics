"""Article creation view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.articles import (
    ConfirmArticleCreateCallback,
    OpenArticlesMenuCallback,
)
from pricecalcbot.bot.texts.articles import (
    ASK_DUTY_FEE_RATIO,
    ASK_NAME,
    BACK_TO_ARTICLES_MENU,
    CONFIRM_ARTICLE_CREATION,
    CONFIRM_CREATION_BTN,
    CREATED_ARTICLE,
    DISMISS_CREATION_BTN,
    BAD_DUTY_FEE_RATIO,
)
from pricecalcbot.models.articles import ArticleInfo


async def send_name_request(message: Message) -> None:
    """Ask user for article name.

    Args:
        message: Message to answer.
    """
    await message.answer(text=ASK_NAME)


async def send_duty_fee_ratio_request(message: Message) -> None:
    """Ask user for duty fee ratio.

    Args:
        message: Message to answer.
    """
    await message.answer(text=ASK_DUTY_FEE_RATIO)


async def send_bad_duty_fee_ratio(message: Message) -> None:
    """Warn about bad fee format.

    Args:
        message: Message to answer.
    """
    await message.answer(text=BAD_DUTY_FEE_RATIO)


def build_confirmation_text(article: ArticleInfo) -> str:
    """Build text with article data and confirmation request.

    Args:
        article: Article that will be created.

    Returns:
        Confirmation text.
    """
    return CONFIRM_ARTICLE_CREATION.format(
        name=article.name,
        duty_fee_ratio=article.duty_fee_ratio,
    )


confirmation_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=DISMISS_CREATION_BTN,
                callback_data=OpenArticlesMenuCallback().pack(),
            ),
            InlineKeyboardButton(
                text=CONFIRM_CREATION_BTN,
                callback_data=ConfirmArticleCreateCallback().pack(),
            ),
        ],
    ],
)


async def send_confirmation_request(
    message: Message,
    article: ArticleInfo,
) -> None:
    """Send confirmation request.

    Args:
        message: Message to answer.
        article: Article that will be created.
    """
    await message.answer(
        text=build_confirmation_text(article),
        reply_markup=confirmation_kb,
    )


def build_created_article_text(article: ArticleInfo) -> str:
    """Build text with article info.

    Args:
        article: Article that was created.

    Returns:
        Article info text.
    """
    return CREATED_ARTICLE.format(
        name=article.name,
        duty_fee_ratio=article.duty_fee_ratio,
    )


created_article_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BACK_TO_ARTICLES_MENU,
                callback_data=OpenArticlesMenuCallback().pack(),
            ),
        ],
    ],
)


async def send_created_article(
    message: Message,
    article: ArticleInfo,
) -> None:
    """Send info about created article.

    Args:
        message: Message to answer.
        article: Article that was created.
    """
    await message.answer(
        text=build_created_article_text(article),
        reply_markup=created_article_kb,
    )
