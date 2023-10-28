"""Test AMOCrm API module."""


from typing import AsyncGenerator

import pytest

from chip_logistics.core.amocrm.api import (
    attach_file_to_contact,
    authorize,
    find_contacts,
    upload_file,
)
from chip_logistics.core.amocrm.client import AmoCRMClient, init_client
from chip_logistics.core.amocrm.models import Credentials
from chip_logistics.core.amocrm.repo import AmoCRMRepository


class MockAmoCRMRepository(AmoCRMRepository):
    """Mock of the repository."""

    def __init__(self, credentials: Credentials) -> None:
        """Initialize the mock repository.

        Args:
            credentials: Test credentials.
        """
        self._credentials = credentials

    async def get_credentials(self) -> Credentials:
        """Return credentials from test environment variables.

        Returns:
            Test credentials.
        """
        return self._credentials

    async def save_credentials(self, credentials: Credentials) -> None:
        """Save credentials.

        Args:
            credentials: Credentials to save.
        """
        self._credentials = credentials

    async def close(self) -> None:
        """Delete credentials."""
        self._credentials = None  # type: ignore


@pytest.fixture(scope='module')
async def amo_repo(
    credentials: Credentials,
) -> AsyncGenerator[AmoCRMRepository, None]:
    """Return a mock repository.

    Args:
        credentials: Test credentials.

    Yields:
        Mock repository.
    """
    async with MockAmoCRMRepository(credentials) as repo:
        yield repo


@pytest.fixture(scope='module')
async def amo_client(
    amo_repo: AmoCRMRepository,
) -> AsyncGenerator[AmoCRMClient, None]:
    """Return a clinet with a mock repository.

    Args:
        amo_repo: Mock repository.

    Yields:
        Client with a mock repository.
    """
    async with init_client(amo_repo) as client:
        yield client


async def test_authorize(
    amocrm_auth_code: str,
    amo_client: AmoCRMClient,
) -> None:
    """Test the authorize function.

    Args:
        amocrm_auth_code: AmoCRM authorization code.
        amo_client: Client with a mock repository.
    """
    await authorize(amo_client, amocrm_auth_code)
    assert amo_client.credentials.access_token is not None
    assert amo_client.credentials.refresh_token is not None


async def test_find_contacts(
    amo_client: AmoCRMClient,
) -> None:
    """Test the find_contacts function.

    Args:
        amo_client: Client with a mock repository.
    """
    contacts = await find_contacts(amo_client)
    assert len(contacts) == 3

    contacts = await find_contacts(amo_client, 'John')
    assert len(contacts) == 1

    contacts = await find_contacts(amo_client, 'jOhN')
    assert len(contacts) == 1

    contacts = await find_contacts(amo_client, 'Not Exist')
    assert not contacts


async def test_upload_file(
    amo_client: AmoCRMClient,
) -> None:
    """Test the upload_file function.

    Args:
        amo_client: Client with a mock repository.
    """
    file_data = b'0' * 1024
    file_uuid = await upload_file(
        amo_client,
        'test_file.txt',
        file_data,
    )

    updated_file_uuid = await upload_file(
        amo_client,
        'test_file.txt',
        file_data[:-1],
        file_uuid=file_uuid,
    )
    assert updated_file_uuid == file_uuid


async def test_attach_file_to_contact(
    amo_client: AmoCRMClient,
) -> None:
    """Test the attach_file_to_contact function.

    Args:
        amo_client: Client with a mock repository.
    """
    file_data = b'0' * 1024
    file_uuid = await upload_file(
        amo_client,
        'test_file.txt',
        file_data,
    )

    contacts = await find_contacts(amo_client)
    contact = contacts.pop(0)

    await attach_file_to_contact(
        amo_client,
        contact_id=contact.id,
        file_uuid=file_uuid,
    )
