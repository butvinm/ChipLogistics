"""Shared fixtures."""


import asyncio
from asyncio import AbstractEventLoop
from typing import Generator

import pytest


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Create event loop for async tests.

    Yields:
        Event loop.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
