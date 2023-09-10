"""Calculation models."""


from decimal import Decimal

from pydantic import BaseModel, Field


class ArticleItem(BaseModel):
    """Data of one article item for price calculation."""

    # Name
    name: str

    # Count of article items
    count: int = Field(gt=0)

    # Weight per unit in kg
    unit_weight: Decimal = Field(gt=0)

    # Price per unit in rubles
    unit_price: Decimal = Field(gt=0)

    # Duty fee ratio for price
    duty_fee_ratio: Decimal = Field(ge=1)
