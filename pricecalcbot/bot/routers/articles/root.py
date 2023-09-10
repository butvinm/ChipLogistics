"""Root router for articles management."""

from aiogram import Router

from pricecalcbot.bot.routers.articles import article, articles_list, menu

router = Router(name='articles')
router.include_routers(
    article.router,
    articles_list.router,
    menu.router,
)
