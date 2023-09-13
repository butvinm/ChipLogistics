"""Main menu routes."""


from typing import Union

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.menu import OpenMenuCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.texts.greet import OPEN_MENU_BTN
from chip_logistics.bot.views.menu import send_menu

router = Router(name='menu')


@router.callback_query(
    OpenMenuCallback.filter(),
    ExtractMessage,
)
@router.message(
    F.text == OPEN_MENU_BTN,
    F.as_('message'),
)
async def open_menu(
    event: Union[CallbackQuery, Message],
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Open main menu.

    Args:
        event: Event, that trigger menu.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always Success.
    """
    await send_menu(message)
    await state.clear()
    return Ok()
