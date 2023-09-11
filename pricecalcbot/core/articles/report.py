"""CSV report generation."""


import csv
from datetime import datetime
from decimal import Decimal
from io import StringIO

from pricecalcbot.models.articles import ArticleItem


def generate_report_name() -> str:
    """Generate report file name from current datetime.

    Returns:
        Report file name with .csv extension.
    """
    return 'Расчет-{date}.csv'.format(
        date=datetime.now().strftime('%H:%M-%m.%d.%Y'),
    )


def create_calculations_report(
    calculations_results: list[tuple[ArticleItem, Decimal]],
    total_price: Decimal,
) -> tuple[bytes, str]:
    """Generate CSV report for calculations.

    Args:
        calculations_results: List with item sand their costs.
        total_price: Total items price.

    Returns:
        File data and name.
    """
    file_buffer = StringIO()
    writer = csv.writer(file_buffer)

    writer.writerow([
        'Наименование',
        'Цена',
    ])
    for article_item, price in calculations_results:
        writer.writerow([
            article_item.name,
            price,
        ])

    writer.writerow([
        'Общая стоимость',
        total_price,
    ])
    return file_buffer.getvalue().encode('utf-8'), generate_report_name()
