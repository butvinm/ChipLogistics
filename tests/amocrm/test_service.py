"""Test AMoCRMService class."""


from typing import AsyncGenerator

import pytest

from pricecalcbot.core.amocrm.repo import AmoCRMRepository
from pricecalcbot.core.amocrm.service import AmoCRMService
from pricecalcbot.models.amocrm import Credentials


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


@pytest.fixture(scope='module')
def amo_repo(credentials: Credentials) -> AmoCRMRepository:
    """Return a mock repository.

    Args:
        credentials: Test credentials.

    Returns:
        Mock repository.
    """
    return MockAmoCRMRepository(credentials)


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


async def test_find_customers(
    amo_service: AmoCRMService,
) -> None:
    """Test the find_customers method.

    Args:
        amo_service: Service with a mock repository.
    """
    customers = await amo_service.find_customers()
    assert len(customers) == 3

    customers = await amo_service.find_customers('John')
    assert len(customers) == 1

    customers = await amo_service.find_customers('jOhN')
    assert len(customers) == 1

    customers = await amo_service.find_customers('Not Exist')
    assert not customers


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
