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


class OpenContactSelectCallback(CallbackData, prefix='calcs/contact/open'):
    """Open contact select menu."""


class SearchContactCallback(CallbackData, prefix='calcs/contact/search'):
    """Ask query for contact search."""


class SkipContactCallback(CallbackData, prefix='calcs/contact/skip'):
    """Skip contact selecting."""


class SelectContactCallback(CallbackData, prefix='calcs/contact/select'):
    """Select contact."""

    contact_id: int
