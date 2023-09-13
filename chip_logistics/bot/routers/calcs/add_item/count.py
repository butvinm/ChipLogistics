"""Item count route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import (
    send_bad_item_count,
    send_item_unit_weight_request,
)

router = Router(name='calcs/add_item/count')


@router.message(
    CalculationsState.wait_item_count,
    TextMessage,
)
async def handle_item_count(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Save item count to state and ask for item unit weight.

    Args:
        message: Message where query from.
        text: Input count.
        state: Current FSM state.

    Returns:
        Ok - item count save successfully.
        Err - incorrect count format.
    """
    try:
        count = int(text)
    except ValueError as convert_error:
        await send_bad_item_count(message)
        return Err(
            error=str(convert_error),
            message='Incorrect item count format.',
        )

    await state.update_data(count=count)
    await state.set_state(CalculationsState.wait_item_unit_weight)
    await send_item_unit_weight_request(message)
    return Ok(extra={'count': count})
