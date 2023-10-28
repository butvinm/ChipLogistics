"""AmoCRM API.

Encapsulate AmoCRM API calls.
"""


from http import HTTPStatus
from typing import Optional, Union

from chip_logistics.core.amocrm.client import AmoCRMClient, get_auth_headers
from chip_logistics.core.amocrm.models import Contact
from chip_logistics.core.amocrm.responses import (
    AuthResponse,
    ContactsResponse,
    FileSessionResponse,
    FileUploadResponse,
    PartUploadResponse,
)


async def authorize(client: AmoCRMClient, auth_code: str) -> None:
    """Authorize service in AmoCRM.

    See https://www.amocrm.ru/developers/content/oauth/step-by-step

    Args:
        client: Client data for API access.
        auth_code: Authorization code.
    """
    async with client.api_session.post(
        '/oauth2/access_token',
        json={
            'grant_type': 'authorization_code',
            'client_id': client.credentials.client_id,
            'client_secret': client.credentials.client_secret,
            'code': auth_code,
            'redirect_uri': client.credentials.redirect_uri,
        },
    ) as response:
        response.raise_for_status()
        response_data = AuthResponse.from_json(await response.json())
        client.credentials.access_token = response_data.access_token
        client.credentials.refresh_token = response_data.refresh_token
        await client.repo.save_credentials(client.credentials)


async def refresh_access_token(client: AmoCRMClient) -> None:
    """Update access token.

    See https://www.amocrm.ru/developers/content/oauth/step-by-step#Получение-нового-access-token-по-его-истечении for details. # noqa: E501

    Args:
        client: Client data for API access.
    """
    async with client.api_session.post(
        '/oauth2/access_token',
        json={
            'grant_type': 'refresh_token',
            'client_id': client.credentials.client_id,
            'client_secret': client.credentials.client_secret,
            'refresh_token': client.credentials.refresh_token,
            'redirect_uri': client.credentials.redirect_uri,
        },
    ) as response:
        response.raise_for_status()
        response_data = AuthResponse.from_json(await response.json())
        client.credentials.access_token = response_data.access_token
        client.credentials.refresh_token = response_data.refresh_token
        await client.repo.save_credentials(client.credentials)


async def find_contacts(
    client: AmoCRMClient,
    query: str = '',
) -> list[Contact]:
    """Find contacts by fields data.

    Args:
        client: Client data for API access.
        query: Value to search in fields.

    Returns:
        List of found contacts.
    """
    async with client.api_session.get(
        '/api/v4/contacts',
        params={'query': query},
        headers=get_auth_headers(client),
    ) as response:
        response.raise_for_status()
        if response.status == HTTPStatus.OK:
            response_data = ContactsResponse.from_json(
                json=await response.json(),
            )
        else:
            response_data = ContactsResponse(page=0, contacts=[])

        return response_data.contacts


async def attach_file_to_contact(
    client: AmoCRMClient,
    contact_id: int,
    file_uuid: str,
) -> None:
    """Attach file to contact.

    Args:
        client: Client data for API access.
        contact_id: Contact identifier.
        file_uuid: File identifier.
    """
    async with client.api_session.put(
        '/api/v4/contacts/{contact_id}/files'.format(
            contact_id=contact_id,
        ),
        json=[{'file_uuid': file_uuid}],
        headers=get_auth_headers(client),
    ) as response:
        response.raise_for_status()


async def _open_file_upload_session(
    client: AmoCRMClient,
    file_name: str,
    file_size: int,
    file_uuid: Optional[str] = None,
    content_type: Optional[str] = None,
) -> FileSessionResponse:
    """Open file upload session.

    See https://www.amocrm.ru/developers/content/files/files-api#Создание-сессии-загрузки-файла for reference. # noqa: E501

    Args:
        client: Client data for API access.
        file_name: File name
        file_size: File size
        file_uuid: File identifier. \
            Corresponding file will be updated, if specified.
        content_type: MIME-type of file.

    Returns:
        File upload session data.
    """
    async with client.drive_session.post(
        '/v1.0/sessions',
        json={
            'file_name': file_name,
            'file_size': file_size,
            'file_uuid': file_uuid,
            'content_type': content_type,
        },
        headers=get_auth_headers(client),
    ) as response:
        response.raise_for_status()
        return FileSessionResponse.from_json(await response.json())


async def _upload_file_part(
    client: AmoCRMClient,
    upload_url: str,
    part_data: bytes,
) -> Union[PartUploadResponse, FileUploadResponse]:
    """Upload file part in terms of current file uploading session.

    Args:
        client: Client data for API access.
        upload_url: Upload URl provided by API when last part was uploaded.
        part_data: File part data.

    Returns:
        FileUploadResponse if whole file was uploaded,
        otherwise PartUploadResponse.
    """
    upload_url = upload_url.replace(client.credentials.drive_url, '')
    async with client.drive_session.post(
        upload_url,
        data=part_data,
        headers=get_auth_headers(client),
    ) as response:
        response.raise_for_status()
        if response.status == HTTPStatus.ACCEPTED:
            return PartUploadResponse.from_json(await response.json())

        return FileUploadResponse.from_json(await response.json())


async def upload_file(
    client: AmoCRMClient,
    file_name: str,
    file_data: bytes,
    file_uuid: Optional[str] = None,
    content_type: Optional[str] = None,
) -> str:
    """Upload file to account drive.

    Args:
        client: Client data for API access.
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
    session_data = await _open_file_upload_session(
        client=client,
        file_name=file_name,
        file_size=len(file_data),
        file_uuid=file_uuid,
        content_type=content_type,
    )
    upload_url = session_data.upload_url
    while file_data:
        part_data = file_data[:session_data.max_part_size]
        file_data = file_data[session_data.max_part_size:]
        upload_data = await _upload_file_part(
            client=client,
            upload_url=upload_url,
            part_data=part_data,
        )
        if isinstance(upload_data, PartUploadResponse):
            upload_url = upload_data.next_url
        else:
            return upload_data.uuid

    raise RuntimeError('File uploading failed')
