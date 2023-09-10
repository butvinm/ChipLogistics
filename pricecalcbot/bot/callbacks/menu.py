"""Main menu callbacks."""


from aiogram.filters.callback_data import CallbackData


class MenuOpenCallback(CallbackData, prefix='menu/open'):
    """Menu open callback."""
