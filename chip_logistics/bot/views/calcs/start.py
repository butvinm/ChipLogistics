"""Start view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from chip_logistics.bot.callbacks.calcs import AddItemCallback
from chip_logistics.bot.callbacks.menu import OpenMenuCallback
from chip_logistics.bot.texts.calcs import ADD_ITEM_BTN, BACK_TO_MENU, START

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


async def send_start_menu(message: Message) -> None:
    """Send start menu with button for item adding.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=START,
        reply_markup=start_kb,
    )
