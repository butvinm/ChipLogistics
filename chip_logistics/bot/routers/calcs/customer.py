"""Customer info routes."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.continuation_menu import (
    send_continuation_menu,
)

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
