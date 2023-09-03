"""AmoCRM service.

Encapsulates AmoCRM API calls.
"""


from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiohttp import ClientSession

from pricecalcbot.core.amocrm.repo import AmoCRMRepository
from pricecalcbot.core.amocrm.responses import AuthResponse
from pricecalcbot.models.amocrm import Credentials


class AmoCRMService(object):
    """AmoCRM service.

    AmoCRM Service utilize AmoCRm API to interact with AmoCRM.
    See https://www.amocrm.ru/developers for reference.
    """

    def __init__(
        self,
        host: str,
        credentials: Credentials,
        repo: AmoCRMRepository,
    ) -> None:
        """Initialize AmoCRM service.

        That constructor is not intended to be used directly.
        Use `with_credentials` method to build service instance.

        Args:
            host: AmoCRM account host.
            credentials: AmoCRM service credentials.
            repo: AmoCRM service data repository.
        """
        self._credentials = credentials
        self._repo = repo
        self._session = ClientSession(base_url=host)

    @classmethod
    @asynccontextmanager
    async def init(
        cls,
        host: str,
        repo: AmoCRMRepository,
    ) -> AsyncGenerator['AmoCRMService', None]:
        """Initialize AmoCRM service with credentials.

        Args:
            host: AmoCRM account host.
            repo: AmoCRM service data repository.

        Yields:
            AmoCRM service instance.
        """
        credentials = await repo.get_credentials()
        service = cls(host, credentials, repo)
        try:
            yield service
        finally:
            await service._session.close()  # noqa: WPS437

    async def authorize(self, auth_code: str) -> None:
        """Authorize service in AmoCRM.

        See https://www.amocrm.ru/developers/content/oauth/step-by-step

        Args:
            auth_code: Authorization code.
        """
        async with self._session.post(
            '/oauth2/access_token',
            data={
                'grant_type': 'authorization_code',
                'client_id': self._credentials.client_id,
                'client_secret': self._credentials.client_secret,
                'code': auth_code,
                'redirect_uri': self._credentials.redirect_uri,
            },
        ) as response:
            response.raise_for_status()
            response_data = AuthResponse(**await response.json())
            self._credentials.access_token = response_data.access_token
            self._credentials.refresh_token = response_data.refresh_token
            await self._repo.save_credentials(self._credentials)

    async def refresh_access_token(self) -> None:
        """Update access token.

        See https://www.amocrm.ru/developers/content/oauth/step-by-step#Получение-нового-access-token-по-его-истечении for details. # noqa: E501
        """
        async with self._session.post(
            '/oauth2/access_token',
            data={
                'grant_type': 'refresh_token',
                'client_id': self._credentials.client_id,
                'client_secret': self._credentials.client_secret,
                'refresh_token': self._credentials.refresh_token,
                'redirect_uri': self._credentials.redirect_uri,
            },
        ) as response:
            response.raise_for_status()
            response_data = AuthResponse(**await response.json())
            self._credentials.access_token = response_data.access_token
            self._credentials.refresh_token = response_data.refresh_token
            await self._repo.save_credentials(self._credentials)
