"""Test articles report module."""

from pathlib import Path

from chip_logistics.core.articles.calcs import (
    calculate_article_price,
    calculate_total_price,
)
from chip_logistics.core.articles.report import create_calculations_report
from tests.articles.conftest import test_articles


async def test_create_calculations_report(
    report_template: bytes,
) -> None:
    """Test calcs report creation.

    Args:
        report_template: Report template.
    """
    calculations_results = [
        (
            article_item,
            calculate_article_price(article_item),
        )
        for article_item, _ in test_articles
    ]
    total_price = calculate_total_price(
        calculations_results,
    )
    report, name = create_calculations_report(
        calculations_results,
        total_price,
        'Alex',
        report_template,
    )
    assert Path(name).write_bytes(report)
