"""Start item data collecting route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.calcs import AddItemCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.add_item import send_item_name_request

router = Router(name='calcs/add_item/start')


@router.callback_query(
    CalculationsState.wait_continuation,
    AddItemCallback.filter(),
    ExtractMessage,
)
async def start_item_data_dialog(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Ask item count.

    Args:
        callback_query: Callback query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_item_name_request(message)
    await state.set_state(CalculationsState.wait_item_name)
    return Ok()
