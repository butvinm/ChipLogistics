"""Bot and dispatcher factories."""


from aiogram import Bot, Dispatcher
from aiogram_deta import create_dispatcher
from deta import Deta

from pricecalcbot.bot.routers.start import router as start_router


def init_bot(token: str) -> Bot:
    """Initialize aiogram bot.

    Args:
        token: Telegram bot token.

    Returns:
        Bot instance.
    """
    return Bot(token=token, parse_mode='HTML')


def init_dispatcher(deta: Deta) -> Dispatcher:
    """Initialize dispatcher with Deta FSM storage.

    Args:
        deta: Deta instance.

    Returns:
        Dispatcher instance.
    """
    dispatcher: Dispatcher = create_dispatcher(deta=deta)
    dispatcher.include_router(start_router)
    return dispatcher
