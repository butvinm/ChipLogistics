"""Back button callbacks."""

from aiogram.filters.callback_data import CallbackData


class BackCallback(CallbackData, prefix='back'):
    """Back to the next step in current dialog context."""
