"""Entry point of application.

Telegram Bot and FastAPI instances are created and
services and dependencies initialized there.
"""

from deta import Deta

from pricecalcbot import config
from pricecalcbot.api.factory import init_app
from pricecalcbot.bot.factory import init_bot, init_dispatcher

deta = Deta()
bot = init_bot(config.get_bot_token())
dispatcher = init_dispatcher(deta)
app = init_app(
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=config.get_bot_secret(),
)
