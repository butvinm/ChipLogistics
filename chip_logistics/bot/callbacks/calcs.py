"""Calculations callbacks."""

from aiogram.filters.callback_data import CallbackData

from chip_logistics.models.articles import Currency


class StartCalcsCallback(CallbackData, prefix='calcs/open'):
    """Start calculation."""


class AddItemCallback(CallbackData, prefix='calcs/add'):
    """Start item calculations."""


class ItemPriceCurrencyCallback(CallbackData, prefix='calcs/article/currency'):
    """Select article item price currency."""

    currency: Currency


class SelectArticleCallback(CallbackData, prefix='calcs/article/select'):
    """Select article from list."""

    article_id: str


class ManualArticleCallback(CallbackData, prefix='calcs/article/manual'):
    """Start manual input of article data."""


class OpenContactSelectCallback(CallbackData, prefix='calcs/contact/open'):
    """Open contact select menu."""


class SearchContactCallback(CallbackData, prefix='calcs/contact/search'):
    """Ask query for contact search."""


class SelectContactCallback(CallbackData, prefix='calcs/contact/select'):
    """Select contact."""

    contact_id: int


class FinishCalcsCallback(CallbackData, prefix='calcs/finish'):
    """Finish calculations."""
