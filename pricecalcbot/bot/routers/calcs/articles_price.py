"""Articles prices calculation routes."""


from aiogram import Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.calcs import StartCalcsCallback
from pricecalcbot.bot.filters.extract_message import ExtractMessage
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.calcs.articles_price import show_start_menu

router = Router(name='calcs/articles_price')


@router.callback_query(
    StartCalcsCallback.filter(),
    ExtractMessage,
)
async def start_calcs(
    callback_query: CallbackQuery,
    message: Message,
) -> HandlerResult:
    """Show start message.

    Args:
        callback_query: Open menu query.
        message: Message where query from.

    Returns:
        Always success.
    """
    await show_start_menu(message)
    return Ok()
