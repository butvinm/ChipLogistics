"""Root calculations router."""


from aiogram import Router

from chip_logistics.bot.routers.calcs import contact_select, finish, start
from chip_logistics.bot.routers.calcs.add_item import root as add_item

router = Router(name='calcs')
router.include_routers(
    contact_select.router,
    finish.router,
    add_item.router,
    start.router,
)
