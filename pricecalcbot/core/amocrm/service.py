"""AmoCRM service.

Encapsulates AmoCRM API calls.
"""


from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncGenerator

from aiohttp import ClientSession

from pricecalcbot.core.amocrm.repo import AmoCRMRepository
from pricecalcbot.core.amocrm.responses import AuthResponse, CustomersResponse
from pricecalcbot.models.amocrm import Credentials, Customer


class AmoCRMService(object):
    """AmoCRM service.

    AmoCRM Service utilize AmoCRm API to interact with AmoCRM.
    See https://www.amocrm.ru/developers for reference.
    """

    def __init__(
        self,
        credentials: Credentials,
        repo: AmoCRMRepository,
    ) -> None:
        """Initialize AmoCRM service.

        That constructor is not intended to be used directly.
        Use `with_credentials` method to build service instance.

        Args:
            credentials: AmoCRM service credentials.
            repo: AmoCRM service data repository.
        """
        self._credentials = credentials
        self._repo = repo
        self._session = ClientSession(base_url=credentials.api_url)

    @classmethod
    @asynccontextmanager
    async def init(
        cls,
        repo: AmoCRMRepository,
    ) -> AsyncGenerator['AmoCRMService', None]:
        """Initialize AmoCRM service with credentials.

        Args:
            repo: AmoCRM service data repository.

        Yields:
            AmoCRM service instance.
        """
        credentials = await repo.get_credentials()
        service = AmoCRMService(credentials, repo)
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
            response_data = AuthResponse.from_json(await response.json())
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
            response_data = AuthResponse.from_json(await response.json())
            self._credentials.access_token = response_data.access_token
            self._credentials.refresh_token = response_data.refresh_token
            await self._repo.save_credentials(self._credentials)

    async def find_customers(self, query: str = '') -> list[Customer]:
        """Find customers by fields data.

        Args:
            query: Value to search in fields.

        Returns:
            List of found customers.
        """
        async with self._session.get(
            '/api/v4/customers?query={query}'.format(query=query),
            headers=self._get_auth_header(),
        ) as response:
            response.raise_for_status()
            if response.status == HTTPStatus.OK:
                response_data = CustomersResponse.from_json(
                    json=await response.json(),
                )
            else:
                response_data = CustomersResponse(page=0, customers=[])

            return response_data.customers

    def _get_auth_header(self) -> dict[str, str]:
        """Return Bearer authorization header.

        Returns:
            Bearer auth header with access_token.
        """
        bearer = 'Bearer {token}'.format(token=self._credentials.access_token)
        return {'Authorization': bearer}
