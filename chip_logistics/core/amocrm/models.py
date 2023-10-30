"""AmoCRM models."""


from typing import Optional

from pydantic import BaseModel


class Credentials(BaseModel):
    """Integration credentials model."""

    api_url: str
    drive_url: str
    client_id: str
    client_secret: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    redirect_uri: str


class Contact(BaseModel):
    """AmoCRM contact model.

    See https://www.amocrm.ru/developers/content/crm_platform/contacts-api
    """

    id: int
    name: str
