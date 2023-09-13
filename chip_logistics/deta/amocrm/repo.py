"""AmoCRMRepository implementation based on Deta Base."""


from typing import Any

from deta import Deta

from chip_logistics.core.amocrm.repo import AmoCRMRepository
from chip_logistics.models.amocrm import Credentials


class DetaAmoCRMRepository(AmoCRMRepository):
    """AmoCRMRepository implementation based on Deta Base."""

    def __init__(self, deta: Deta) -> None:
        """Initialize repo and connect deta base.

        Args:
            deta: Deta API instance.
        """
        super().__init__()

        self._base = deta.AsyncBase('amocrm')

    async def get_credentials(self) -> Credentials:
        """Get AmoCRM integration credentials from the `amocrm` base.

        Currently, only one AmoCRM account supported, so
        we just pull single base item.

        Returns:
            AmoCRM integration credentials.
        """
        credentials_result = await self._base.fetch()
        credentials_item: dict[str, Any] = credentials_result.items.pop()
        return Credentials(**credentials_item)

    async def save_credentials(self, credentials: Credentials) -> None:
        """Save AmoCRM integration credentials to the `amocrm` base.

        Client id field is used as key to achieve idempotency of get operation.

        Args:
            credentials: AmoCRM integration credentials.
        """
        await self._base.put(
            data=credentials.model_dump(),
            key=credentials.client_id,
        )

    async def close(self) -> None:
        """Close Deta Base connection."""
        await self._base.close()
