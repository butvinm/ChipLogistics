"""Test AMoCRMService class."""


from typing import AsyncGenerator

import pytest

from chip_logistics.core.amocrm.repo import AmoCRMRepository
from chip_logistics.core.amocrm.service import AmoCRMService
from chip_logistics.core.amocrm.models import Credentials


class MockAmoCRMRepository(AmoCRMRepository):
    """Mock repository for the AmoCRMService tests."""

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
async def amo_service(
    amo_repo: AmoCRMRepository,
) -> AsyncGenerator[AmoCRMService, None]:
    """Return a service with a mock repository.

    Args:
        amo_repo: Mock repository.

    Yields:
        Service with a mock repository.
    """
    async with AmoCRMService.init(amo_repo) as service:
        yield service


async def test_authorize(
    amocrm_auth_code: str,
    amo_service: AmoCRMService,
) -> None:
    """Test the authorize method.

    Args:
        amocrm_auth_code: AmoCRM authorization code.
        amo_service: Service with a mock repository.
    """
    await amo_service.authorize(amocrm_auth_code)
    assert amo_service._credentials.access_token is not None
    assert amo_service._credentials.refresh_token is not None


async def test_find_contacts(
    amo_service: AmoCRMService,
) -> None:
    """Test the find_contacts method.

    Args:
        amo_service: Service with a mock repository.
    """
    contacts = await amo_service.find_contacts()
    assert len(contacts) == 3

    contacts = await amo_service.find_contacts('John')
    assert len(contacts) == 1

    contacts = await amo_service.find_contacts('jOhN')
    assert len(contacts) == 1

    contacts = await amo_service.find_contacts('Not Exist')
    assert not contacts


async def test_upload_file(
    amo_service: AmoCRMService,
) -> None:
    """Test the upload_file method.

    Args:
        amo_service: Service with a mock repository.
    """
    file_data = b'0' * 1024
    file_uuid = await amo_service.upload_file(
        'test_file.txt',
        file_data,
    )

    updated_file_uuid = await amo_service.upload_file(
        'test_file.txt',
        file_data + b'0',
        file_uuid=file_uuid,
    )
    assert updated_file_uuid == file_uuid


async def test_attach_file_to_contact(
    amo_service: AmoCRMService,
) -> None:
    """Test the attach_file_to_contact method.

    Args:
        amo_service: Service with a mock repository.
    """
    file_data = b'0' * 1024
    file_uuid = await amo_service.upload_file(
        'test_file.txt',
        file_data,
    )

    contacts = await amo_service.find_contacts()
    contact = contacts.pop(0)

    await amo_service.attach_file_to_contact(
        contact_id=contact.id,
        file_uuid=file_uuid,
    )
