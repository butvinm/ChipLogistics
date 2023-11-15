"""Articles selection views."""

from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from chip_logistics.bot.callbacks.calcs import (
    ManualArticleCallback,
    SelectArticleCallback,
)
from chip_logistics.bot.texts.calcs import (
    ARTICLE_MANUAL_INPUT,
    ARTICLE_SELECT,
    ASK_DUTY_FEE_RATIO,
    ASK_NAME,
    BAD_DUTY_FEE_RATIO,
)
from chip_logistics.core.articles.models import ArticleInfo


def build_article_select_kb(
    articles: list[ArticleInfo],
) -> InlineKeyboardMarkup:
    """Build kb with articles and manual input button.

    Args:
        articles: Articles to select.

    Returns:
        Articles select kb
    """
    builder = InlineKeyboardBuilder()
    for article in articles:
        if article.id is not None:
            builder.button(
                text=article.name,
                callback_data=SelectArticleCallback(
                    article_id=article.id,
                ),
            )

    builder.button(
        text=ARTICLE_MANUAL_INPUT,
        callback_data=ManualArticleCallback().pack(),
    )

    # Articles aligned in two columns.
    rows_sizes = [2 for _ in range(len(articles) // 2)]
    # If article lost, single column used
    if len(articles) % 2 == 1:
        rows_sizes.append(1)

    # Manual button aligned in separated row
    rows_sizes.append(1)

    builder.adjust(*rows_sizes)
    return builder.as_markup()


async def send_article_request(
    message: Message,
    articles: list[ArticleInfo],
) -> None:
    """Send articles list and manual input buttons.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        articles: Articles to select.
    """
    await message.answer(
        text=ARTICLE_SELECT,
        reply_markup=build_article_select_kb(articles),
    )


async def send_name_request(
    message: Message,
) -> None:
    """Ask article name.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_NAME)


async def send_duty_fee_ratio_request(
    message: Message,
) -> None:
    """Ask article duty fee ratio.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_DUTY_FEE_RATIO)


async def send_bad_duty_fee_ratio(
    message: Message,
) -> None:
    """Warn about bad duty fee ratio format.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=BAD_DUTY_FEE_RATIO)
