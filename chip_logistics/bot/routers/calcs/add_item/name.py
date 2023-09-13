"""Item name route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import send_item_count_request

router = Router(name='calcs/add_item/name')


@router.message(
    CalculationsState.wait_item_name,
    TextMessage,
)
async def handle_item_name(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Save item name to state and ask for item count.

    Args:
        message: Message where query from.
        text: Entered item name.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await state.update_data(name=text)
    await state.set_state(CalculationsState.wait_item_count)
    await send_item_count_request(message)
    return Ok(extra={'name': text})
