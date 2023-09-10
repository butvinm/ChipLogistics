"""Calculations callbacks."""

from aiogram.filters.callback_data import CallbackData


class StartCalcsCallback(CallbackData, prefix='calcs/open'):
    """Start calculation."""
