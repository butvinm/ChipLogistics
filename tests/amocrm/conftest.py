"""Shared fixtures for amocrm tests."""


from os import environ

import pytest
from dotenv import load_dotenv

from chip_logistics.models.amocrm import Credentials

load_dotenv('./tests/amocrm/.env')


@pytest.fixture(scope='package')
def amocrm_auth_code() -> str:
    """Get AmoCRM authorization code.

    Returns:
        AmoCRM authorization code.
    """
    return environ['AMOCRM_AUTH_CODE']


@pytest.fixture(scope='package')
def credentials() -> Credentials:
    """Get test credentials.

    See .env.example and CONTRIBUTING.md for details.

    Returns:
        Test credentials.
    """
    return Credentials(
        api_url=environ['AMOCRM_API_URL'],
        drive_url=environ['AMOCRM_DRIVE_URL'],
        client_id=environ['AMOCRM_CLIENT_ID'],
        client_secret=environ['AMOCRM_CLIENT_SECRET'],
        redirect_uri=environ['AMOCRM_REDIRECT_URI'],
        access_token=None,
        refresh_token=None,
    )
