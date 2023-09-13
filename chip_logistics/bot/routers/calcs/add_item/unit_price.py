"""Item unit price route."""


from decimal import DecimalException

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import send_bad_item_unit_price
from chip_logistics.bot.views.calcs.continuation_menu import (
    send_continuation_menu,
)
from chip_logistics.deta.models import model_dump
from chip_logistics.models.articles import ArticleItem
from chip_logistics.utils.decimal import parse_decimal

router = Router(name='calcs/add_item/unit_price')


@router.message(
    CalculationsState.wait_item_unit_price,
    TextMessage,
)
async def handle_item_unit_price(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Add item to the items ist in state and ask for item unit price.

    Args:
        message: Message where query from.
        text: Input unit price.
        state: Current FSM state.

    Returns:
        Ok - item unit price save successfully.
        Err - incorrect price format.
    """
    try:
        unit_price = parse_decimal(text)
    except DecimalException as convert_error:
        await send_bad_item_unit_price(message)
        return Err(
            error=str(convert_error),
            message='Incorrect item unit price format.',
        )

    if unit_price < 0:
        await send_bad_item_unit_price(message)
        return Err(
            message='Incorrect item unit price format.',
        )

    context = await state.update_data(unit_price=str(unit_price))

    article_item = ArticleItem(**context)
    context.setdefault('items', []).append(model_dump(article_item))
    articles_items = [
        ArticleItem(**article_item_data)
        for article_item_data in context.get('items', [])
    ]

    await send_continuation_menu(message, articles_items)

    await state.set_data(context)
    await state.set_state(CalculationsState.wait_continuation)
    return Ok(extra={'item': article_item})
