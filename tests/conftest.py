"""Shared fixtures."""


import asyncio
from asyncio import AbstractEventLoop

import pytest


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    """Create event loop for async tests.

    Returns:
        Event loop.
    """
    return asyncio.get_event_loop()
