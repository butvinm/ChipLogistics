"""Root calculations router."""


from aiogram import Router

from chip_logistics.bot.routers.calcs import (
    contact_select,
    finish,
    item_data,
    start,
)

router = Router(name='calcs')
router.include_routers(
    contact_select.router,
    finish.router,
    item_data.router,
    start.router,
)
