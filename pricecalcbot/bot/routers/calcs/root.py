"""Root calculations router."""


from aiogram import Router

from pricecalcbot.bot.routers.calcs import (
    article_select,
    contact_select,
    finish,
    item_data,
    start,
)

router = Router(name='calcs')
router.include_routers(
    article_select.router,
    contact_select.router,
    finish.router,
    item_data.router,
    start.router,
)
