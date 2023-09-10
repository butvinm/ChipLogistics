"""Greeting view."""


from aiogram import Bot

from pricecalcbot.bot import messages


async def greet(bot: Bot, chat_id: int) -> None:
    """Greet user.

    Args:
        bot: Bot instance.
        chat_id: Chat id.
    """
    await bot.send_message(chat_id, messages.greet)
