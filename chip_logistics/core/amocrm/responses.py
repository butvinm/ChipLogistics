"""AmoCRM API responses models."""


from typing import Any

from pydantic import BaseModel, ValidationError

from chip_logistics.core.amocrm.models import Contact


class AuthResponse(BaseModel):
    """Response for authorization at /oauth2/access_token."""

    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'AuthResponse':
        """Build response object from json data.

        Auth response has simple structure, so just pass all fields.
        See https://www.amocrm.ru/developers/content/oauth/step-by-step#Запросы-к-API-с-передачей-access-token for response format referene. # noqa: E501

        Args:
            json: Response json data.

        Returns:
            Auth response model.
        """
        return AuthResponse(**json)


class ContactsResponse(BaseModel):
    """Response with contacts list."""

    page: int
    contacts: list[Contact]

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'ContactsResponse':
        """Build response object from json data.

        See https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-list for response format reference. # noqa: E501

        Args:
            json: Response json data.

        Returns:
            Contacts response model.

        Raises:
            ValidationError: If json data invalid.
        """
        page = json.get('_page')
        if not page:
            raise ValidationError('Page field missed.')

        contacts = json.get('_embedded', {}).get('contacts')
        if not contacts:
            raise ValidationError('Custoemrs field missed.')

        return ContactsResponse(page=page, contacts=contacts)


class FileSessionResponse(BaseModel):
    """Response for new file uploading session."""

    max_file_size: int
    max_part_size: int
    session_id: int
    upload_url: str

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'FileSessionResponse':
        """Build response object from json data.

        See https://www.amocrm.ru/developers/content/files/files-api#Создание-сессии-загрузки-файла for reference. # noqa: E501

        Args:
            json: Response json data

        Returns:
            File session data.
        """
        return FileSessionResponse(**json)


class PartUploadResponse(BaseModel):
    """Response of one file part uploading."""

    next_url: str
    session_id: str

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'PartUploadResponse':
        """Build response object from json data.

        See https://www.amocrm.ru/developers/content/files/files-api#Загрузка-части-файла for reference. # noqa: E501

        Args:
            json: Response json data

        Returns:
            Uploading data.
        """
        return PartUploadResponse(**json)


class FileUploadResponse(BaseModel):
    """Response of last file part uploading."""

    uuid: str
    type: str
    name: str

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'FileUploadResponse':
        """Build response object from json data.

        See https://www.amocrm.ru/developers/content/files/files-api#Загрузка-части-файла for reference. # noqa: E501

        Args:
            json: Response json data

        Returns:
            File info.
        """
        return FileUploadResponse(**json)
