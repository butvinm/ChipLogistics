"""Shared fixtures and test data."""


# List of articles and them costs
from decimal import Decimal
from pathlib import Path
from random import randint

import pytest

from chip_logistics.core.articles.models import ArticleItem, Currency

ARTICLE_NAME_PREFIX = 'Article'

DEFAULT_DUTY_FEE_RATIO = Decimal('1')

REPORT_TEMPLATE_FILE = Path('tests/articles/report_template.docx')


@pytest.fixture
def report_template() -> bytes:
    """Get test report template file.

    Returns:
        Template content.
    """
    return REPORT_TEMPLATE_FILE.read_bytes()


def gen_article_name() -> str:
    """Generate random article name.

    Returns:
        ARTICLE_NAME_PREFIX-{int}
    """
    return '{prefix}-{number}'.format(
        prefix=ARTICLE_NAME_PREFIX,
        number=randint(0, 1024),  # noqa: S311
    )


test_articles = (
    (
        ArticleItem(
            name=gen_article_name(),
            count=1755,
            unit_weight=Decimal('0.07'),
            unit_price=Decimal('11.12'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('30901.0'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=10,
            unit_weight=Decimal('2.1'),
            unit_price=Decimal('125.874'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('2303.5'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=132,
            unit_weight=Decimal('0.23'),
            unit_price=Decimal('13.75'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('3300.2'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=1500,
            unit_weight=Decimal('0.00048'),
            unit_price=Decimal('0.45'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('1016.0'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('50'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('364531.9'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=5000,
            unit_weight=Decimal('0.0002'),
            unit_price=Decimal('0.5'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('3676.9'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=5000,
            unit_weight=Decimal('0.001'),
            unit_price=Decimal('3.75'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('27497.0'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=5000,
            unit_weight=Decimal('0.002'),
            unit_price=Decimal('7.85'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('57449.5'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=1000,
            unit_weight=Decimal('0.001'),
            unit_price=Decimal('10.83'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('15822.0'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=5000,
            unit_weight=Decimal('0.0123'),
            unit_price=Decimal('1'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('8553.3'),
    ),
    (
        ArticleItem(
            name=gen_article_name(),
            count=1360,
            unit_weight=Decimal('0.039'),
            unit_price=Decimal('0.9'),
            duty_fee_ratio=DEFAULT_DUTY_FEE_RATIO,
            price_currency=Currency.usd,
        ),
        Decimal('2884.9'),
    ),
)
