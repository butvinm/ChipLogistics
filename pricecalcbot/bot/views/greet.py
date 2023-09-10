"""Greeting view."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from pricecalcbot.bot.callbacks.menu import MenuOpenCallback
from pricecalcbot.bot.texts.greet import GREET, OPEN_MENU_BTN

greet_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=OPEN_MENU_BTN,
            callback_data=MenuOpenCallback().pack(),
        ),
    ],
])


async def greet(message: Message) -> None:
    """Greet user.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=GREET,
        reply_markup=greet_kb,
    )
