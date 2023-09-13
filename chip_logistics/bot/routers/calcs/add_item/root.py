"""Root item adding router."""


from aiogram import Router

from chip_logistics.bot.routers.calcs.add_item import (
    count,
    start,
    unit_price,
    unit_weight,
)

router = Router(name='calcs/add_item')
router.include_routers(
    start.router,
    count.router,
    unit_weight.router,
    unit_price.router,
)
