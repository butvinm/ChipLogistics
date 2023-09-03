"""Shared fixtures for amocrm tests."""


from os import environ

import pytest
from dotenv import load_dotenv

from pricecalcbot.models.amocrm import Credentials

load_dotenv()


@pytest.fixture
def amocrm_api_host() -> str:
    """Get AmoCRM API host.

    Returns:
        AmoCRM API host.
    """
    return environ['AMOCRM_API_HOST']


@pytest.fixture
def amocrm_auth_code() -> str:
    """Get AmoCRM authorization code.

    Returns:
        AmoCRM authorization code.
    """
    return environ['AMOCRM_AUTH_CODE']


@pytest.fixture
def credentials() -> Credentials:
    """Get test credentials.

    See .env.example and CONTRIBUTING.md for details.

    Returns:
        Test credentials.
    """
    return Credentials(
        client_id=environ['AMOCRM_CLIENT_ID'],
        client_secret=environ['AMOCRM_CLIENT_SECRET'],
        redirect_uri=environ['AMOCRM_REDIRECT_URI'],
        access_token=None,
        refresh_token=None,
    )
