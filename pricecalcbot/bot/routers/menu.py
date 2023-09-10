"""Main menu routes."""


from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.menu import MenuOpenCallback
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.menu import show_menu

router = Router(name='menu')


@router.callback_query(
    MenuOpenCallback.filter(),
    F.message.as_('message'),
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
    bot: Bot,
) -> HandlerResult:
    """Open main menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        bot: Bot instance.

    Returns:
        Always Success.
    """
    await show_menu(bot, message.chat.id)
    return Ok()
