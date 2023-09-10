"""Main menu view."""


from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pricecalcbot.bot.callbacks.articles import ArticlesOpenMenuCallback
from pricecalcbot.bot.callbacks.calcs import CalcsOpenMenuCallback
from pricecalcbot.bot.texts.menu import OPEN_ARTICLES_BTN, OPEN_CALC_BTN, TITLE

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=OPEN_ARTICLES_BTN,
            callback_data=ArticlesOpenMenuCallback().pack(),
        ),
    ],
    [
        InlineKeyboardButton(
            text=OPEN_CALC_BTN,
            callback_data=CalcsOpenMenuCallback().pack(),
        ),
    ],
])


async def show_menu(bot: Bot, chat_id: int) -> None:
    """Show main menu with navigation buttons.

    Main menu contains buttons for navigate to
    articles management menu and price calculation.

    Args:
        bot: Bot instance.
        chat_id: Chat id.
    """
    await bot.send_message(
        chat_id,
        text=TITLE,
        reply_markup=menu_kb,
    )
