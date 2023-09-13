"""Root router for articles management."""

from aiogram import Router

from chip_logistics.bot.routers.articles import (
    article,
    articles_list,
    create,
    menu,
)

router = Router(name='articles')
router.include_routers(
    article.router,
    articles_list.router,
    create.router,
    menu.router,
)
