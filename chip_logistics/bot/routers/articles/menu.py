"""Articles menu route."""


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.articles import OpenArticlesMenuCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.views.articles.menu import send_articles_menu

router = Router(name='articles/menu')


@router.callback_query(
    OpenArticlesMenuCallback.filter(),
    ExtractMessage,
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Open articles menu.

    Args:
        callback_query: Callback query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_articles_menu(message)
    await state.clear()
    return Ok()
