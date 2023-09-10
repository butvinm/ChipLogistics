"""Articles menu views."""


from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pricecalcbot.bot.callbacks.articles import (
    ArticlesCreateCallback,
    ArticlesOpenListCallback,
)
from pricecalcbot.bot.texts.articles import CREATE_BTN, OPEN_LIST_BTN, TITLE

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=OPEN_LIST_BTN,
            callback_data=ArticlesOpenListCallback().pack(),
        ),
    ],
    [
        InlineKeyboardButton(
            text=CREATE_BTN,
            callback_data=ArticlesCreateCallback().pack(),
        ),
    ],
])


async def show_menu(bot: Bot, chat_id: int) -> None:
    """Show articles management menu.

    Args:
        bot: Bot instance.
        chat_id: Chat id.
    """
    await bot.send_message(
        chat_id,
        text=TITLE,
        reply_markup=menu_kb,
    )
