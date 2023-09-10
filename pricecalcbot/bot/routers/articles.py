"""Articles menu routes."""


from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from pricecalcbot.bot.callbacks.articles import ArticlesOpenMenuCallback
from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.articles import show_menu

router = Router(name='articles')


@router.callback_query(
    ArticlesOpenMenuCallback.filter(),
    F.message.as_('message'),
)
async def open_menu(
    callback_query: CallbackQuery,
    message: Message,
    bot: Bot,
) -> HandlerResult:
    """Open articles menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        bot: Bot instance.

    Returns:
        Always success.
    """
    await show_menu(bot, message.chat.id)
    return Ok()
