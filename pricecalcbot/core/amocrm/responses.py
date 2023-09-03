"""AmoCRM API responses models."""


from pydantic import BaseModel


class AuthResponse(BaseModel):
    """Response for authorization at /oauth2/access_token."""

    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str
