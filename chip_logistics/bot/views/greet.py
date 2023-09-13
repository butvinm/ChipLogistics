"""Greeting view."""


from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from chip_logistics.bot.texts.greet import GREET, OPEN_MENU_BTN

greet_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=OPEN_MENU_BTN,
            ),
        ],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


async def send_greet(message: Message) -> None:
    """Greet user.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=GREET,
        reply_markup=greet_kb,
    )
