"""Item name route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.back import BackCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import send_item_count_request
from chip_logistics.bot.views.calcs.continuation_menu import (
    send_continuation_menu,
)
from chip_logistics.core.articles.models import ArticleItem

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
    await send_item_count_request(message)
    await state.update_data(name=text)
    await state.set_state(CalculationsState.wait_item_count)
    return Ok(extra={'name': text})


@router.callback_query(
    CalculationsState.wait_item_name,
    BackCallback.filter(),
    ExtractMessage,
)
async def back_to_continuation_menu(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Go back to the continuation menu.

    Args:
        callback_query: Handled query.
        message: Message query from.
        state: Current FCM state.

    Returns:
        Always success.
    """
    context = await state.get_data()
    articles_items = [
        ArticleItem(**article)
        for article in context.get('items', [])
    ]
    await send_continuation_menu(message, articles_items)
    await state.set_state(CalculationsState.wait_continuation)
    return Ok()
