"""Tests fro article price calculations."""


from decimal import Decimal

import pytest

from chip_logistics.core.articles.calcs import calculate_article_price
from chip_logistics.models.articles import ArticleItem
from tests.articles.conftest import test_articles


@pytest.mark.parametrize(
    'article,expected_price',
    test_articles,
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
    assert calculate_article_price(article) == expected_price
