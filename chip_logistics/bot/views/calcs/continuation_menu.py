"""Continuation menu view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from chip_logistics.bot.callbacks.calcs import (
    AddItemCallback,
    OpenContactSelectCallback,
)
from chip_logistics.bot.texts.calcs import (
    ADD_ITEM_BTN,
    CONTINUATION_MENU,
    ITEM_DATA,
    STOP_BTN,
)
from chip_logistics.core.articles.models import ArticleItem


def build_continuation_menu_text(articles_items: list[ArticleItem]) -> str:
    """Build items list.

    Args:
        articles_items: Added items.

    Returns:
        List of added items.
    """
    items_data = '\n\n'.join(
        ITEM_DATA.format(**article_item.model_dump())
        for article_item in articles_items
    )
    return CONTINUATION_MENU.format(
        items_data=items_data,
    )


continuation_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ADD_ITEM_BTN,
                callback_data=AddItemCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=STOP_BTN,
                callback_data=OpenContactSelectCallback().pack(),
            ),
        ],
    ],
)


async def send_continuation_menu(
    message: Message,
    articles_items: list[ArticleItem],
) -> None:
    """Send articles list with continue and stop buttons.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        articles_items: Added items.
    """
    await message.answer(
        text=build_continuation_menu_text(articles_items),
        reply_markup=continuation_menu_kb,
    )
