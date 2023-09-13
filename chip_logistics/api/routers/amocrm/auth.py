"""Webhook for AMoCRM "Integration" authorization.

See "Redirect URL" at https://www.amocrm.ru/developers/content/oauth/step-by-step  # noqa: E501
"""


from typing import Annotated

from fastapi import APIRouter, Depends

from chip_logistics.api.routers.deps import get_amocrm_service
from chip_logistics.core.amocrm.service import AmoCRMService

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
async def authorize(
    auth_code: str,
    service: Annotated[AmoCRMService, Depends(get_amocrm_service)],
) -> None:
    """Authorize application with provided auth code.

    Args:
        auth_code: AmoCRM "Integration" auth code.
        service: AmoCRM service.
    """
    await service.authorize(auth_code)


@router.patch('/')
async def refresh_token(
    service: Annotated[AmoCRMService, Depends(get_amocrm_service)],
) -> None:
    """Refresh authorization token.

    Args:
        service: AmoCRM service.
    """
    await service.refresh_access_token()
