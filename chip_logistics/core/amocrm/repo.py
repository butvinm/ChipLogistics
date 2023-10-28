"""AmoCRM client data repository interface."""


from typing import Any, Protocol, runtime_checkable

from chip_logistics.core.amocrm.models import Credentials


@runtime_checkable
class AmoCRMRepository(Protocol):
    """AmoCRM client data repository interface."""

    async def get_credentials(self) -> Credentials:
        """Get AmoCRM integration credentials.

        Returns:
            AmoCRM integration credentials.
        """

    async def save_credentials(self, credentials: Credentials) -> None:
        """Save AmoCRM integration credentials.

        Args:
            credentials: AmoCRM integration credentials.
        """

    async def close(self) -> None:
        """Close repository and clean resources."""

    async def __aenter__(self) -> 'AmoCRMRepository':
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
        await self.close()
