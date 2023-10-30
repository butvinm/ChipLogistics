"""Helpers to create auto-closing classes."""

from typing import Protocol

from typing_extensions import Any, Self


class Closing(Protocol):
    """Auto-closing class mixin."""

    def __enter__(self) -> Self:
        """Enter context manager and return repo instance.

        Args:
            Initialized instance.

        Returns:
            Initialized instance.
        """
        return self

    def __exit__(self, *args: Any) -> None:
        """Clean resources.

        Args:
            args: Exceptions info, if exception was caused.
        """
        self.close()

    def close(self) -> None:
        """Close object resources."""


class AClosing(Protocol):
    """Auto-closing async class mixin."""

    async def __aenter__(self) -> Self:
        """Enter context manager and return repo instance.

        Args:
            Initialized instance.

        Returns:
            Initialized instance.
        """
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Clean resources.

        Args:
            args: Exceptions info, if exception was caused.
        """
        await self.aclose()

    async def aclose(self) -> None:
        """Close object resources."""
