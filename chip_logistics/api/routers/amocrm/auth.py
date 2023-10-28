"""Webhook for AMoCRM "Integration" authorization.

See "Redirect URL" at https://www.amocrm.ru/developers/content/oauth/step-by-step  # noqa: E501
"""


from typing import Annotated

from fastapi import APIRouter, Depends

from chip_logistics.api.routers.deps import get_amocrm_client
from chip_logistics.core.amocrm.api import authorize, refresh_access_token
from chip_logistics.core.amocrm.client import AmoCRMClient

router = APIRouter(prefix='/auth')


@router.get('/')
async def handle_authorization(
    code: str,
    referer: str,
    state: str,
    from_widget: str = '',
    platform: int = 0,
) -> None:
    """Handle auth response from AmoCRM.

    Auth response is send on user login via login-link
    and periodically by AmoCRM to check availability.

    Currently it's just stub, because we don't provide
    login for users and work with one account.

    Args:
        code: Authorization code.
        referer: User account address.
        state: Signature for request verification or identification.
        from_widget: Specified, if request send by AmoCRM, not user.
        platform: AmoCRM platform identifier: \
            0 - if not specified, \
            1 - from Russian amocrm.ru account, \
            2 - from global amocrm.com/kommo.com account.
    """


@router.post('/')
async def authorize_client(
    auth_code: str,
    client: Annotated[AmoCRMClient, Depends(get_amocrm_client)],
) -> None:
    """Authorize AmoCRM client with provided auth code.

    Args:
        auth_code: AmoCRM "Integration" auth code.
        client: AmoCRM client.
    """
    await authorize(client, auth_code)


@router.patch('/')
async def refresh_auth_token(
    client: Annotated[AmoCRMClient, Depends(get_amocrm_client)],
) -> None:
    """Refresh authorization token.

    Args:
        client: AmoCRM client.
    """
    await refresh_access_token(client)
