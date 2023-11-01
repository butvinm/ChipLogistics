"""Item count route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.back import BackCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import (
    send_bad_item_count,
    send_item_name_request,
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

    if count < 0:
        await send_bad_item_count(message)
        return Err(
            message='Incorrect item count format.',
        )

    await send_item_unit_weight_request(message)
    await state.update_data(count=count)
    await state.set_state(CalculationsState.wait_item_unit_weight)
    return Ok(extra={'count': count})


@router.callback_query(
    CalculationsState.wait_item_count,
    BackCallback.filter(),
    ExtractMessage,
)
async def back_to_item_name(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Go back to the item name request.

    Args:
        callback_query: Handled query.
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    await send_item_name_request(message)
    await state.set_state(CalculationsState.wait_item_name)
    return Ok()
