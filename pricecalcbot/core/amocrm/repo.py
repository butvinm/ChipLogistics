"""AmoCRM Service data repository interface."""


from typing import Protocol

from pricecalcbot.models.amocrm import Credentials


class AmoCRMRepository(Protocol):
    """AmoCRM Service data repository interface."""

    async def get_credentials(self) -> Credentials:
        """Get AmoCRM integration credentials.

        Returns:
            Credentials: AmoCRM integration credentials.
        """

    async def save_credentials(self, credentials: Credentials) -> None:
        """Save AmoCRM integration credentials.

        Args:
            credentials: AmoCRM integration credentials.
        """
