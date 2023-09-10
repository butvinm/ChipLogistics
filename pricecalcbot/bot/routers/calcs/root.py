"""Root calculations router."""


from aiogram import Router

from pricecalcbot.bot.routers.calcs import articles_price

router = Router(name='calcs')
router.include_routers(articles_price.router)
