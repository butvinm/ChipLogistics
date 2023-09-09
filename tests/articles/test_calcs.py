"""Tests fro article price calculations."""


from decimal import Decimal

import pytest

from pricecalcbot.core.articles.calcs import calculate_article_price
from pricecalcbot.models.articles import ArticleItem

test_data = [
    (
        ArticleItem(
            count=1755,
            unit_weight=Decimal('0.07'),
            unit_price=Decimal('11.12'),
            duty_fee_ratio=Decimal('1.09'),
        ),
        Decimal('34484.6376'),
    ),
    (
        ArticleItem(
            count=10,
            unit_weight=Decimal('2.1'),
            unit_price=Decimal('125.874'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('2505.05892'),
    ),
    (
        ArticleItem(
            count=132,
            unit_weight=Decimal('0.23'),
            unit_price=Decimal('13.75'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('3635.046'),
    ),
    (
        ArticleItem(
            count=1500,
            unit_weight=Decimal('0.00048'),
            unit_price=Decimal('0.45'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('1016.046'),
    ),
    (
        ArticleItem(
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('50'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('364531.896'),
    ),
    (
        ArticleItem(
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('0.5'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('3676.896'),
    ),
    (
        ArticleItem(
            count=5000,
            unit_weight=Decimal('0.001'),
            unit_price=Decimal('3.75'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('27496.98'),
    ),
    (
        ArticleItem(
            count=5000,
            unit_weight=Decimal('0.002'),
            unit_price=Decimal('7.85'),
            duty_fee_ratio=Decimal('1'),
        ),
        Decimal('57545.46'),
    ),
]


@pytest.mark.parametrize(
    'article,expected_price',
    test_data,
)
def test_article_price_calculation(
    article: ArticleItem,
    expected_price: Decimal,
) -> None:
    """Test calculate_article_price function.

    Args:
        article: The article for which to calculate the price.
        expected_price: Expected function result.
    """
    result = calculate_article_price(article)
    assert result == expected_price
