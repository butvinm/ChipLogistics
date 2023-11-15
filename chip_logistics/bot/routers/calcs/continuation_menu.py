"""Continuation menu routes."""

from typing import Any

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.back import BackCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import (
    send_item_unit_price_request,
)
from chip_logistics.bot.views.calcs.customer import send_customer_name_request
from chip_logistics.core.articles.models import Currency

router = Router(name='calcs/continuation')


@router.callback_query(
    CalculationsState.wait_continuation,
    BackCallback.filter(),
    ExtractMessage,
)
async def back_to_previous_item(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Go to the previous step.

    Go back to the beginning of calculations dialog
    or to the last item unit price request.

    Args:
        callback_query: Handled query.
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    context = await state.get_data()
    currency = context.get('price_currency')
    articles_items_data = context.get('items', [])
    if not articles_items_data or currency is None:
        return await back_to_the_beginning(message, state)

    return await back_to_item_unit_price(
        articles_items_data,
        currency,
        message,
        state,
    )


async def back_to_the_beginning(
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Clear state and go the first item name request.

    Args:
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    await send_customer_name_request(message)
    await state.clear()
    await state.set_state(CalculationsState.wait_customer_name)
    return Ok()


async def back_to_item_unit_price(
    articles_items_data: list[dict[str, Any]],
    currency: Currency,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Go back to the item unit price request.

    Args:
        articles_items_data: Data of previously entered items.
        currency: Previously entered currency.
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    articles_items_data = articles_items_data[:-1]  # pop last item
    await state.update_data(items=articles_items_data)
    await send_item_unit_price_request(message, currency)
    await state.set_state(CalculationsState.wait_item_unit_price)
    return Ok()
