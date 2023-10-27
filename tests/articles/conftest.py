"""Shared fixtures and test data."""


# List of articles and them costs
from decimal import Decimal
from os import environ

import pytest

from chip_logistics.models.articles import ArticleItem, Currency

test_articles = (
    (
        ArticleItem(
            name="Микро",
            count=1755,
            unit_weight=Decimal('0.07'),
            unit_price=Decimal('11.12'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('30901.0'),
    ),
    (
        ArticleItem(
            name="Микро2",
            count=10,
            unit_weight=Decimal('2.1'),
            unit_price=Decimal('125.874'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('2303.5'),
    ),
    (
        ArticleItem(
            name="Микро3",
            count=132,
            unit_weight=Decimal('0.23'),
            unit_price=Decimal('13.75'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('3300.2'),
    ),
    (
        ArticleItem(
            name="Микро4",
            count=1500,
            unit_weight=Decimal('0.00048'),
            unit_price=Decimal('0.45'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('1016.0'),
    ),
    (
        ArticleItem(
            name="Микро5",
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('50'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('364531.9'),
    ),
    (
        ArticleItem(
            name="Микро6",
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('0.5'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('3676.9'),
    ),
    (
        ArticleItem(
            name="Микро7",
            count=5000,
            unit_weight=Decimal('0.001'),
            unit_price=Decimal('3.75'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('27497.0'),
    ),
    (
        ArticleItem(
            name="Микро8",
            count=5000,
            unit_weight=Decimal('0.002'),
            unit_price=Decimal('7.85'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('57449.5'),
    ),
    (
        ArticleItem(
            name="Микро9",
            count=1000,
            unit_weight=Decimal('0.001'),
            unit_price=Decimal('10.83'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('15822.0'),
    ),
    (
        ArticleItem(
            name="Микро10",
            count=5000,
            unit_weight=Decimal('0.0123'),
            unit_price=Decimal('1'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('8553.3'),
    ),
    (
        ArticleItem(
            name="Микрор11",
            count=1360,
            unit_weight=Decimal('0.039'),
            unit_price=Decimal('0.9'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('2884.9'),
    ),
)


@pytest.fixture(scope='package')
def fixer_api_key() -> str:
    """Get Fixer API key from environment.

    Returns:
        Fixer API key.
    """
    return environ['FIXER_API_KEY']
