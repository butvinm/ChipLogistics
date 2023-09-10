"""Main menu routes."""


from aiogram import Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.menu import OpenMenuCallback
from pricecalcbot.bot.filters.extract_message import ExtractMessage
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.menu import show_menu

router = Router(name='menu')


@router.callback_query(
    OpenMenuCallback.filter(),
    ExtractMessage,
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
) -> HandlerResult:
    """Open main menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.

    Returns:
        Always Success.
    """
    await show_menu(message)
    return Ok()
