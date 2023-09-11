"""Main menu routes."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.menu import OpenMenuCallback
from pricecalcbot.bot.filters.extract_message import ExtractMessage
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.menu import send_menu

router = Router(name='menu')


@router.callback_query(
    OpenMenuCallback.filter(),
    ExtractMessage,
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Open main menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always Success.
    """
    await send_menu(message)
    await state.clear()
    return Ok()
