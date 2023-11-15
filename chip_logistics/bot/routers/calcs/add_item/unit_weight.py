"""Item unit weight route."""


from decimal import DecimalException

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.back import BackCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import (
    send_bad_item_unit_weight,
    send_item_count_request,
    send_item_price_currency_request,
)
from chip_logistics.utils.decimal import parse_decimal

router = Router(name='calcs/add_item/unit_weight')


@router.message(
    CalculationsState.wait_item_unit_weight,
    TextMessage,
)
async def handle_item_unit_weight(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Save item unit_weight to state and ask for item unit price.

    Args:
        message: Message where query from.
        text: Input unit weight.
        state: Current FSM state.

    Returns:
        Ok - item unit weight save successfully.
        Err - incorrect weight format.
    """
    try:
        unit_weight = parse_decimal(text)
    except DecimalException as convert_error:
        await send_bad_item_unit_weight(message)
        return Err(
            error=str(convert_error),
            message='Incorrect item unit weight format.',
        )

    if unit_weight < 0:
        await send_bad_item_unit_weight(message)
        return Err(
            message='Incorrect item unit weight format.',
        )

    await send_item_price_currency_request(message)

    await state.update_data(unit_weight=str(unit_weight))
    await state.set_state(CalculationsState.wait_item_price_currency)
    return Ok(extra={'unit_weight': unit_weight})


@router.callback_query(
    CalculationsState.wait_item_unit_weight,
    BackCallback.filter(),
    ExtractMessage,
)
async def back_to_item_count_request(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Go back to the item count request.

    Args:
        callback_query: Handled query.
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    await send_item_count_request(message)
    await state.set_state(CalculationsState.wait_item_count)
    return Ok()
