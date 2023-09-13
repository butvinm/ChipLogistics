"""AmoCRM dependencies."""


from typing import Annotated, AsyncGenerator

from deta import Deta
from fastapi import Depends

from chip_logistics.core.amocrm.repo import AmoCRMRepository
from chip_logistics.core.amocrm.service import AmoCRMService
from chip_logistics.deta.amocrm.repo import DetaAmoCRMRepository
from chip_logistics.deta.deta import get_deta


async def get_amocrm_repo(
    deta: Annotated[Deta, Depends(get_deta)],
) -> AsyncGenerator[AmoCRMRepository, None]:
    """Get AmoCRM repository based on Deta Base.

    Args:
        deta: Deta API.

    Yields:
        AmoCRMRepository
    """
    async with DetaAmoCRMRepository(deta) as repo:
        yield repo


async def get_amocrm_service(
    repo: Annotated[AmoCRMRepository, Depends(get_amocrm_repo)],
) -> AsyncGenerator[AmoCRMService, None]:
    """Get AmoCRMService instance.

    Args:
        repo: AmoCRM repository

    Yields:
        AsyncGenerator[AmoCRMService, None]: _description_
    """
    async with AmoCRMService.init(repo) as service:
        yield service
