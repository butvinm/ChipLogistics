"""Start view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from chip_logistics.bot.callbacks.calcs import AddItemCallback
from chip_logistics.bot.texts.calcs import ADD_ITEM_BTN, START

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ADD_ITEM_BTN,
                callback_data=AddItemCallback().pack(),
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
