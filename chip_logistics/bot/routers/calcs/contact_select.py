"""Contact select routes."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.calcs import (
    OpenContactSelectCallback,
    SearchContactCallback,
    SelectContactCallback,
)
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.contact_select import (
    send_contact_select_menu,
    send_contact_selected,
    send_search_query_request,
    send_search_result,
)
from chip_logistics.core.amocrm.service import AmoCRMService

router = Router(name='calcs/contacts')


@router.callback_query(
    CalculationsState.wait_continuation,
    OpenContactSelectCallback.filter(),
    ExtractMessage,
)
async def open_contact_select(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Send contact select menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_contact_select_menu(message)
    await state.set_state(CalculationsState.wait_contact_select)
    return Ok()


@router.callback_query(
    CalculationsState.wait_contact_select,
    SearchContactCallback.filter(),
    ExtractMessage,
)
async def start_contact_search(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Ask for search query.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_search_query_request(message)
    await state.set_state(CalculationsState.wait_contact_search)
    return Ok()


@router.message(
    CalculationsState.wait_contact_search,
    TextMessage,
)
async def handle_search_query(
    message: Message,
    text: str,
    state: FSMContext,
    amocrm_service: AmoCRMService,
) -> HandlerResult:
    """Ask for search query.

    Args:
        message: Message where query from.
        text: Search query.
        state: Current FSM state.
        amocrm_service: AmoCRM service.

    Returns:
        Ok - search finish successfully.
        Err - search failed.
    """
    contacts = await amocrm_service.find_contacts(query=text)
    await send_search_result(message, contacts)
    await state.set_state(CalculationsState.wait_contact_select)
    return Ok(extra={'query': text, 'contacts': contacts})


@router.callback_query(
    CalculationsState.wait_contact_select,
    SelectContactCallback.filter(),
    ExtractMessage,
)
async def select_contact(
    callback_query: CallbackQuery,
    callback_data: SelectContactCallback,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Save selected contact to state and offer complete calcs.

    Args:
        callback_query: Open menu query.
        callback_data: Callback data with contact id.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_contact_selected(message)
    await state.update_data(contact_id=callback_data.contact_id)
    return Ok()
