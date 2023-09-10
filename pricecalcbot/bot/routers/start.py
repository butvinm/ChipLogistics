"""Start router."""


from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types.message import Message

from pricecalcbot.bot.handler_result import HandlerResult, Ok
from pricecalcbot.bot.views.greet import greet

router = Router(name='start')


@router.message(CommandStart())
async def start(message: Message, bot: Bot) -> HandlerResult:
    """Greet user.

    Args:
        message: `/start` command.
        bot: Bot instance.

    Returns:
        Always success.
    """
    await greet(bot, message.chat.id)
    return Ok()
