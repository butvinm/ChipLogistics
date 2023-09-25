"""Calculation models."""


from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Currency(str, Enum):  # noqa: WPS600
    """Supported items prices currencies."""

    usd = 'USD'

    cyn = 'CNY'


class ArticleInfo(BaseModel):
    """Article information."""

    # Article identifier
    id: Optional[str]

    # Name
    name: str

    # Duty fee ratio for price
    duty_fee_ratio: Decimal = Field(default=1, ge=1)


class ArticleItem(BaseModel):
    """Data of one article item for price calculation."""

    # Name
    name: str

    # Count of article items
    count: int = Field(ge=0)

    # Weight per unit in kg
    unit_weight: Decimal = Field(ge=0)

    # Price per unit in rubles
    unit_price: Decimal = Field(ge=0)

    # Currency of price
    price_currency: Currency

    # Duty fee ratio for price
    duty_fee_ratio: Decimal = Field(default=Decimal(1), ge=1)
