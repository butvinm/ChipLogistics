"""Calculations callbacks."""

from aiogram.filters.callback_data import CallbackData


class StartCalcsCallback(CallbackData, prefix='calcs/open'):
    """Start calculation."""


class AddItemCallback(CallbackData, prefix='calcs/add'):
    """Start item calculations."""


class SelectArticleCallback(CallbackData, prefix='calcs/article/select'):
    """Select article from list."""

    article_id: str


class ManualArticleCallback(CallbackData, prefix='calcs/article/manual'):
    """Start manual input of article data."""


class OpenContactSelect(CallbackData, prefix='calcs/contact/open'):
    """Open contact select menu."""
