"""Greeting view."""


from aiogram.types.message import Message

from pricecalcbot.bot import messages
from pricecalcbot.bot.handler_result import HandlerResult, Ok


async def greet(message: Message) -> HandlerResult:
    """Greet user.

    Args:
        message: Any user message.

    Returns:
        Always success.
    """
    await message.answer(messages.greet)
    return Ok()
