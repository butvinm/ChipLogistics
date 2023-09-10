"""Greeting view."""


from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


async def greet(bot: Bot, chat_id: int) -> None:
    """Greet user.

    Args:
        bot: Bot instance.
        chat_id: Chat id.
    """
    await bot.send_message(
        chat_id,
        text=GREET,
        reply_markup=greet_kb,
    )
