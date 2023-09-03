"""AmoCRM models."""


from typing import Optional

from pydantic import BaseModel


class Credentials(BaseModel):
    """Integration credentials model."""

    client_id: str
    client_secret: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    redirect_uri: str
