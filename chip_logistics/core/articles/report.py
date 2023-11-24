"""CSV report generation.

Report is builded from template that is DOCX file with SINGLE table.
That table would be replaced with corresponding data.
"""


from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Any, Union

from docxtpl import DocxTemplate
from pydantic import BaseModel

from chip_logistics.core.articles.models import ArticleItem


def generate_report_name() -> str:
    """Generate report file name from current datetime.

    Returns:
        Report file name with .docx extension.
    """
    return 'Расчет-{date}.docx'.format(
        date=datetime.now().strftime('%H:%M-%m.%d.%Y'),
    )


def get_formatted_number(number: Union[float, Decimal]) -> str:
    """Return float number string representation.

    Number is formatted with one digit after point.

    Args:
        number: Number to format.

    Returns:
        Formatted string.
    """
    return '{0:.1f}'.format(number)


class TableData(BaseModel):
    """Table data representation."""

    cells: list[list[Any]]
    cols: int
    rows: int


def build_table_data(
    calculations_results: list[tuple[ArticleItem, Decimal]],
    total_price: Decimal,
    customer_name: str,
) -> TableData:
    """Create report table content.

    Args:
        calculations_results: List with item sand their costs.
        total_price: Total items price.
        customer_name: Customer name.

    Returns:
        Table data.
    """
    cells: list[list[Any]] = []
    # header
    header = [
        'Клиент',
        'Наименование',
        'Количество',
        'Общий вес',
        'Цена (В долларах)',
    ]
    cells.append(header)

    # articles data
    for article_item, price in calculations_results:
        cells.append([
            customer_name,
            article_item.name,
            str(article_item.count),
            str(article_item.unit_weight * article_item.count),
            get_formatted_number(price),
        ])

    # footer
    cells.append([])
    cells.append([
        'Общая стоимость (В долларах)',
        get_formatted_number(total_price),
    ])
    return TableData(cells=cells, cols=len(header), rows=len(cells))


def create_calculations_report(
    calculations_results: list[tuple[ArticleItem, Decimal]],
    total_price: Decimal,
    customer_name: str,
    template: bytes,
) -> tuple[bytes, str]:
    """Generate Excel calculations report.

    Available template params:
        headers: Table headers labels.
        articles: List with calculated articles info as list of fields.
        total: Total price.

    See DocxTpl documentation for templates syntaxes reference:
    https://github.com/elapouya/python-docx-template

    Args:
        calculations_results: List with item sand their costs.
        total_price: Total items price.
        customer_name: Customer name.
        template: Docx template.

    Returns:
        File data and name.
    """
    doc = DocxTemplate(BytesIO(template))
    context = {
        'headers': [
            'Клиент',
            'Наименование',
            'Количество',
            'Общий вес',
            'Цена (В долларах)',
        ],
        'articles': [
            [
                customer_name,
                article_item.name,
                str(article_item.count),
                str(article_item.unit_weight * article_item.count),
                get_formatted_number(price),
            ]
            for article_item, price in calculations_results
        ],
        'total': total_price,
    }
    doc.render(context)

    doc_buffer = BytesIO()
    doc.save(doc_buffer)
    return doc_buffer.getvalue(), generate_report_name()
