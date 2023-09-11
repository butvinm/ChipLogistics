"""Start router."""


from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.greet import send_greet

router = Router(name='start')


@router.message(CommandStart())
async def start(
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Greet user.

    Args:
        message: `/start` command.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_greet(message)
    await state.clear()
    return Ok()
