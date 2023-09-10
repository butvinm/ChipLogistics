"""Calculations callbacks."""

from aiogram.filters.callback_data import CallbackData


class CalcsOpenMenuCallback(CallbackData, prefix='calcs/open'):
    """Callback for starting calculations."""
