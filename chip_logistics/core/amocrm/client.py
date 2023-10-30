"""AmoCRM client.

Structure with data for accessing AmoCRm API.
See https://www.amocrm.ru/developers for reference.
"""


from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiohttp import ClientSession
from pydantic import BaseModel, ConfigDict

from chip_logistics.core.amocrm.models import Credentials
from chip_logistics.core.amocrm.repo import AmoCRMRepo


class AmoCRMClient(BaseModel):
    """AmoCRM client data.

    Contains data for interacting with AmoCRM API.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # API credentials.
    credentials: Credentials

    # Repository where client info stored.
    repo: AmoCRMRepo

    # Session with AmoCRM API related to current account.
    api_session: ClientSession

    # Session with AmoCRM drive related to current account.
    drive_session: ClientSession


@asynccontextmanager
async def init_client(
    repo: AmoCRMRepo,
) -> AsyncGenerator[AmoCRMClient, None]:
    """Initialize AmoCRM client with credentials.

    Args:
        repo: AmoCRM client data repository.

    Yields:
        AmoCRM client instance.
    """
    credentials = await repo.get_credentials()
    api_session = ClientSession(base_url=credentials.api_url)
    drive_session = ClientSession(base_url=credentials.drive_url)
    service = AmoCRMClient(
        credentials=credentials,
        repo=repo,
        api_session=api_session,
        drive_session=drive_session,
    )
    try:
        yield service
    finally:
        await api_session.close()
        await drive_session.close()


def get_auth_headers(client: AmoCRMClient) -> dict[str, str]:
    """Return Bearer authorization headers.

    Args:
        client: Client data for API access.

    Returns:
        Bearer auth header with access_token.
    """
    bearer = 'Bearer {token}'.format(token=client.credentials.access_token)
    return {'Authorization': bearer}
