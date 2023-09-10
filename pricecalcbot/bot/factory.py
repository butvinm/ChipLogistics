"""Bot and dispatcher factories."""


from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_deta import create_dispatcher
from deta import Deta

from pricecalcbot.bot.routers.articles import router as articles_router
from pricecalcbot.bot.routers.menu import router as menu_router
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
    dispatcher.include_routers(
        articles_router,
        start_router,
        menu_router,
    )
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    return dispatcher
