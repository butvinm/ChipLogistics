"""Bot and dispatcher factories."""


from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_deta import create_dispatcher
from deta import Deta

from chip_logistics.bot.routers.articles.root import router as articles_router
from chip_logistics.bot.routers.calcs.root import router as calcs_router
from chip_logistics.bot.routers.menu import router as menu_router
from chip_logistics.bot.routers.start import router as start_router


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
        start_router,
        menu_router,
        articles_router,
        calcs_router,
    )
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware(pre=True))
    return dispatcher
