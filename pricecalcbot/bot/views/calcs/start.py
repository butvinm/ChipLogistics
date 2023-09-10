"""Start view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.calcs import AddItemCallback
from pricecalcbot.bot.callbacks.menu import OpenMenuCallback
from pricecalcbot.bot.texts.calcs import ADD_ITEM_BTN, BACK_TO_MENU, START

add_item_btns = [
    [
        InlineKeyboardButton(
            text=ADD_ITEM_BTN,
            callback_data=AddItemCallback().pack(),
        ),
    ],
]
start_kb = InlineKeyboardMarkup(
    inline_keyboard=add_item_btns + [
        [
            InlineKeyboardButton(
                text=BACK_TO_MENU,
                callback_data=OpenMenuCallback().pack(),
            ),
        ],
    ],
)


async def show_start_menu(message: Message) -> None:
    """Show start menu with button for item adding.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.edit_text(
        text=START,
        reply_markup=start_kb,
    )
