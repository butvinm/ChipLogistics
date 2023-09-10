"""Greeting view."""


from aiogram import Bot

from pricecalcbot.bot import messages
from pricecalcbot.bot.handler_result import HandlerResult, Ok


async def greet(bot: Bot, chat_id: int) -> HandlerResult:
    """Greet user.

    Args:
        bot: Bot instance.
        chat_id: Chat id.

    Returns:
        Always success.
    """
    await bot.send_message(chat_id, messages.greet)
    return Ok()
