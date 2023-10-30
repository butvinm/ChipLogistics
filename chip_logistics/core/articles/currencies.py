"""Currencies converting module."""


from decimal import Decimal
from typing import Any, Optional

from aiohttp import ClientResponse, ClientResponseError, ClientSession

from chip_logistics.core.articles.models import Currency
from chip_logistics.utils.closing import AClosing


class CurrenciesService(AClosing):
    """Currencies service.

    Provide functionality for access currencies info and convert prices.

    Utilize Fixer API via API Layer.
    See for reference https://apilayer.com/marketplace/fixer-api.

    Can reuse cached exchange rates for fast converting.
    """

    def __init__(self, fixer_api_key: str) -> None:
        """Initialize service.

        Open session with api server and create dictionary for cached rates.

        Args:
            fixer_api_key (str): FixerAPI key.
        """
        self._session = ClientSession(
            base_url='https://api.apilayer.com',
            headers={'apikey': fixer_api_key},
        )
        self.last_rates: dict[tuple[Currency, Currency], Decimal] = {}

    async def aclose(self) -> None:
        """Close session."""
        await self._session.close()

    async def get_exchange_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        use_cached: bool,
    ) -> Optional[Decimal]:
        """Get exchange rate for specified currencies.

        Also updates cached rate value for that currencies pair.

        Args:
            from_currency: Base currency.
            to_currency: Target currency.
            use_cached: Try to get rate from cache instead of API call.

        Returns:
            Converted price and used rate.
        """
        if from_currency == to_currency:
            return Decimal(1)

        async with self._session.get(
            '/fixer/latest',
            params={
                'base': from_currency.value,
                'symbols': to_currency.value,
            },
        ) as response:
            response_data = await response.json()
            self._raise_for_status(response, response_data)

            rate = response_data.get('rates', {}).get(to_currency.value)
            if rate is None:
                return None

            self._update_cached_rate(from_currency, to_currency, rate)
            return Decimal(rate)

    async def convert_price(
        self,
        price: Decimal,
        from_currency: Currency,
        to_currency: Currency,
        use_cached: bool = True,
    ) -> Optional[Decimal]:
        """Convert price with exchange rate.

        Args:
            price: Price in base currency.
            from_currency: Base currency.
            to_currency: Target currency.
            use_cached: Try to get rate from cache instead of API call.

        Returns:
            Price in target currency. None if cannot get rate.
        """
        rate = await self.get_exchange_rate(
            from_currency,
            to_currency,
            use_cached,
        )
        if rate is None:
            return None

        return price * rate

    def _update_cached_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        rate: Decimal,
    ) -> None:
        """Update rate value in cache for specified currencies pair.

        Args:
            from_currency: Base currency.
            to_currency: Target currency.
            rate: Exchange rate to save.
        """
        self.last_rates[(from_currency, to_currency)] = rate

    def _raise_for_status(
        self,
        response: ClientResponse,
        response_data: dict[str, Any],
    ) -> None:
        """Raise exception if response `success` field is not True.

        It is necessary due to Fixer API error handling.

        Args:
            response: Response object.
            response_data: Response data.

        Raises:
            ClientResponseError: If response `success` field is not True.
        """
        if response_data.get('success') is not True:
            raise ClientResponseError(
                request_info=response.request_info,
                history=response.history,
                status=response_data.get('error', {}).get('code'),
                message=response_data.get('error', {}).get('type'),
                headers=response.headers,
            )
