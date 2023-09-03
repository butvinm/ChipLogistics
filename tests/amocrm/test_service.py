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


@pytest.fixture
def amo_repo(credentials: Credentials) -> AmoCRMRepository:
    """Return a mock repository.

    Args:
        credentials: Test credentials.

    Returns:
        Mock repository.
    """
    return MockAmoCRMRepository(credentials)


@pytest.fixture
async def amo_service(
    amocrm_api_host: str,
    amo_repo: AmoCRMRepository,
) -> AsyncGenerator[AmoCRMService, None]:
    """Return a service with a mock repository.

    Args:
        amocrm_api_host: AmoCRM API host.
        amo_repo: Mock repository.

    Yields:
        Service with a mock repository.
    """
    async with AmoCRMService.init(amocrm_api_host, amo_repo) as service:
        yield service


@pytest.mark.asyncio
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
