"""AmoCRM API responses models."""


from typing import Any

from pydantic import BaseModel, ValidationError

from pricecalcbot.models.amocrm import Customer


class AuthResponse(BaseModel):
    """Response for authorization at /oauth2/access_token."""

    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'AuthResponse':
        """Build reponse object from json data.

        Auth response has simple structure, so just pass all fields.
        See https://www.amocrm.ru/developers/content/oauth/step-by-step#Запросы-к-API-с-передачей-access-token for response format referene. # noqa: E501

        Args:
            json: Response json data.

        Returns:
            Auth response model.
        """
        return AuthResponse(**json)


class CustomersResponse(BaseModel):
    """Response with customers list."""

    page: int
    customers: list[Customer]

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> 'CustomersResponse':
        """Build response object from json data.

        See https://www.amocrm.ru/developers/content/crm_platform/customers-api#customers-list for response format reference. # noqa: E501

        Args:
            json: Response json data.

        Returns:
            Customers response model.

        Raises:
            ValidationError: If json data invalid.
        """
        page = json.get('_page')
        if not page:
            raise ValidationError('Page field missed.')

        customers = json.get('_embedded', {}).get('customers')
        if not customers:
            raise ValidationError('Custoemrs field missed.')

        return CustomersResponse(page=page, customers=customers)
