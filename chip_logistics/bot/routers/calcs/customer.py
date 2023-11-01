"""Customer info routes."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.back import BackCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.continuation_menu import (
    send_continuation_menu,
)
from chip_logistics.bot.views.menu import send_menu

router = Router(name='calcs/customer')


@router.message(
    CalculationsState.wait_customer_name,
    TextMessage,
)
async def handler_customer_name(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Save customer name to state and ask for item.

    Args:
        message: Message with customer name.
        text: Entered customer name.
        state: Current FCM state.

    Returns:
        Always success.
    """
    await send_continuation_menu(message, [])
    await state.update_data(customer_name=text)
    await state.set_state(CalculationsState.wait_continuation)
    return Ok(extra={'customer_name': text})


@router.callback_query(
    CalculationsState.wait_customer_name,
    BackCallback.filter(),
    ExtractMessage,
)
async def back_to_menu(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Go back to the start menu.

    Args:
        callback_query: Handled query.
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    await send_menu(message)
    await state.clear()
    return Ok()
