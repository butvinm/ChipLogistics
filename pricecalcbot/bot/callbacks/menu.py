"""Main menu callbacks."""


from aiogram.filters.callback_data import CallbackData


class OpenMenuCallback(CallbackData, prefix='menu/open'):
    """Open main menu."""
