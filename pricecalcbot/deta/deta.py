"""Deta API instance factory."""

from deta import Deta


async def get_deta() -> Deta:
    """Get Deta API instance.

    Returns:
        Deta API for current runtime.
    """
    return Deta()
