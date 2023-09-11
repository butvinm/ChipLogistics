"""Articles menu view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.articles import (
    CreateArticleCallback,
    OpenArticlesListCallback,
)
from pricecalcbot.bot.callbacks.menu import OpenMenuCallback
from pricecalcbot.bot.texts.articles import (
    BACK_TO_MENU,
    CREATE_BTN,
    OPEN_LIST_BTN,
    TITLE,
)

back_to_menu_btns = [
    [
        InlineKeyboardButton(
            text=BACK_TO_MENU,
            callback_data=OpenMenuCallback().pack(),
        ),
    ],
]

articles_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OPEN_LIST_BTN,
                callback_data=OpenArticlesListCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=CREATE_BTN,
                callback_data=CreateArticleCallback().pack(),
            ),
        ],
    ] + back_to_menu_btns,
)


async def send_articles_menu(message: Message) -> None:
    """Send articles management menu.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=TITLE,
        reply_markup=articles_menu_kb,
    )
