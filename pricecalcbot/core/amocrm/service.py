"""AmoCRM service.

Encapsulates AmoCRM API calls.
"""


from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncGenerator, Optional, Union

from aiohttp import ClientSession

from pricecalcbot.core.amocrm.repo import AmoCRMRepository
from pricecalcbot.core.amocrm.responses import (
    AuthResponse,
    CustomersResponse,
    FileSessionResponse,
    FileUploadResponse,
    PartUploadResponse,
)
from pricecalcbot.models.amocrm import Credentials, Customer


class AmoCRMService(object):  # noqa: WPS214
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
        self._drive_session = ClientSession(base_url=credentials.drive_url)

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
            await service._drive_session.close()  # noqa: WPS437

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

    async def upload_file(
        self,
        file_name: str,
        file_data: bytes,
        file_uuid: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> str:
        """Upload file to account drive.

        Args:
            file_name: File name
            file_data: File content,
            file_uuid: File identifier. \
                Corresponding file will be updated, if specified.
            content_type: MIME-type of file.

        Returns:
            UUID of uploaded file.

        Raises:
            RuntimeError: If file uploading failed.
        """
        session_data = await self._open_file_upload_session(
            file_name=file_name,
            file_size=len(file_data),
            file_uuid=file_uuid,
            content_type=content_type,
        )
        upload_url = session_data.upload_url
        while file_data:
            part_data = file_data[:session_data.max_part_size]
            file_data = file_data[session_data.max_part_size:]
            upload_data = await self._upload_file_part(
                upload_url=upload_url,
                part_data=part_data,
            )
            if isinstance(upload_data, PartUploadResponse):
                upload_url = upload_data.next_url
            else:
                return upload_data.uuid

        raise RuntimeError('File uploading failed')

    async def _open_file_upload_session(
        self,
        file_name: str,
        file_size: int,
        file_uuid: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> FileSessionResponse:
        """Open file upload session.

        See https://www.amocrm.ru/developers/content/files/files-api#Создание-сессии-загрузки-файла for reference. # noqa: E501

        Args:
            file_name: File name
            file_size: File size
            file_uuid: File identifier. \
                Corresponding file will be updated, if specified.
            content_type: MIME-type of file.

        Returns:
            File upload session data.
        """
        async with self._drive_session.post(
            '/v1.0/sessions',
            json={
                'file_name': file_name,
                'file_size': file_size,
                'file_uuid': file_uuid,
                'content_type': content_type,
            },
            headers=self._get_auth_header(),
        ) as response:
            response.raise_for_status()
            return FileSessionResponse.from_json(await response.json())

    async def _upload_file_part(
        self,
        upload_url: str,
        part_data: bytes,
    ) -> Union[PartUploadResponse, FileUploadResponse]:
        upload_url = upload_url.replace(self._credentials.drive_url, '')
        async with self._drive_session.post(
            upload_url,
            data=part_data,
            headers=self._get_auth_header(),
        ) as response:
            response.raise_for_status()
            if response.status == HTTPStatus.ACCEPTED:
                return PartUploadResponse.from_json(await response.json())

            return FileUploadResponse.from_json(await response.json())

    def _get_auth_header(self) -> dict[str, str]:
        """Return Bearer authorization header.

        Returns:
            Bearer auth header with access_token.
        """
        bearer = 'Bearer {token}'.format(token=self._credentials.access_token)
        return {'Authorization': bearer}
