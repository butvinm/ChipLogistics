"""AmoCRM client data repository interface."""


from typing import Protocol, runtime_checkable

from chip_logistics.core.amocrm.models import Credentials
from chip_logistics.utils.closing import AClosing


@runtime_checkable
class AmoCRMRepo(AClosing, Protocol):
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
