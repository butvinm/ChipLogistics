"""AmoCRM dependencies."""


from typing import Annotated, AsyncGenerator

from deta import Deta
from fastapi import Depends

from chip_logistics.core.amocrm.client import AmoCRMClient, init_client
from chip_logistics.core.amocrm.repo import AmoCRMRepo
from chip_logistics.deta.amocrm.repo import DetaAmoCRMRepo
from chip_logistics.deta.deta import get_deta


async def get_amocrm_repo(
    deta: Annotated[Deta, Depends(get_deta)],
) -> AsyncGenerator[AmoCRMRepo, None]:
    """Get AmoCRM repository based on Deta Base.

    Args:
        deta: Deta API.

    Yields:
        AmoCRMRepo
    """
    async with DetaAmoCRMRepo(deta) as repo:
        yield repo


async def get_amocrm_client(
    repo: Annotated[AmoCRMRepo, Depends(get_amocrm_repo)],
) -> AsyncGenerator[AmoCRMClient, None]:
    """Get AmoCRMClient instance.

    Args:
        repo: AmoCRM repository

    Yields:
        AsyncGenerator[AmoCRMClient, None]: AMOCrm client.
    """
    async with init_client(repo) as service:
        yield service
