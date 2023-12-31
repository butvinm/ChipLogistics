"""Start calculations route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.calcs import StartCalcsCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.customer import send_customer_name_request

router = Router(name='calcs/start')


@router.callback_query(
    StartCalcsCallback.filter(),
    ExtractMessage,
)
async def start_calcs(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Send start message.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_customer_name_request(message)
    await state.clear()
    await state.set_state(CalculationsState.wait_customer_name)
    return Ok()
