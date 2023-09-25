"""Shared fixtures and test data."""


# List of articles and them costs
from decimal import Decimal
from os import environ

import pytest

from chip_logistics.models.articles import ArticleItem, Currency

test_articles = (
    (
        ArticleItem(
            name='Article 1',
            count=1755,
            unit_weight=Decimal('0.07'),
            unit_price=Decimal('11.12'),
            duty_fee_ratio=Decimal('1.09'),
            price_currency=Currency.usd,
        ),
        Decimal('34484.6376'),
    ),
    (
        ArticleItem(
            name='Article 2',
            count=10,
            unit_weight=Decimal('2.1'),
            unit_price=Decimal('125.874'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('2505.05892'),
    ),
    (
        ArticleItem(
            name='Article 3',
            count=132,
            unit_weight=Decimal('0.23'),
            unit_price=Decimal('13.75'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('3635.046'),
    ),
    (
        ArticleItem(
            name='Article 4',
            count=1500,
            unit_weight=Decimal('0.00048'),
            unit_price=Decimal('0.45'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('1016.046'),
    ),
    (
        ArticleItem(
            name='Article 5',
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('50'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('364531.896'),
    ),
    (
        ArticleItem(
            name='Article 6',
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('0.5'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('3676.896'),
    ),
    (
        ArticleItem(
            name='Article 7',
            count=5000,
            unit_weight=Decimal('0.001'),
            unit_price=Decimal('3.75'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('27496.98'),
    ),
    (
        ArticleItem(
            name='Article 8',
            count=5000,
            unit_weight=Decimal('0.002'),
            unit_price=Decimal('7.85'),
            duty_fee_ratio=Decimal('1'),
            price_currency=Currency.usd,
        ),
        Decimal('57545.46'),
    ),
)


@pytest.fixture(scope='package')
def fixer_api_key() -> str:
    """Get Fixer API key from environment.

    Returns:
        Fixer API key.
    """
    return environ['FIXER_API_KEY']
