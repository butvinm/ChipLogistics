"""Articles management callbacks."""

from aiogram.filters.callback_data import CallbackData


class ArticlesOpenMenuCallback(CallbackData, prefix='articles/open'):
    """Callback for opening articles management menu."""
