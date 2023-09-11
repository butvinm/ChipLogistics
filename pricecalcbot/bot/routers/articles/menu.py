"""Articles menu route."""


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from pricecalcbot.bot.callbacks.articles import OpenArticlesMenuCallback
from pricecalcbot.bot.filters.extract_message import ExtractMessage
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.texts.greet import OPEN_MENU_BTN
from pricecalcbot.bot.views.articles.menu import send_articles_menu

router = Router(name='articles/menu')


@router.callback_query(
    OpenArticlesMenuCallback.filter(),
    ExtractMessage,
)
@router.message(
    F.text == OPEN_MENU_BTN,
)
async def open_menu(
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Open articles menu.

    Args:
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_articles_menu(message)
    await state.clear()
    return Ok()
