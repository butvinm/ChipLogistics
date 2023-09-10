"""Root calculations router."""


from aiogram import Router

from pricecalcbot.bot.routers.calcs import article_select, item_data, start

router = Router(name='calcs')
router.include_routers(start.router)
router.include_routers(article_select.router)
router.include_routers(item_data.router)
