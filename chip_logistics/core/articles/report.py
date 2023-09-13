"""CSV report generation."""


from datetime import datetime
from decimal import Decimal
from io import BytesIO

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font

from chip_logistics.models.articles import ArticleItem


def generate_report_name() -> str:
    """Generate report file name from current datetime.

    Returns:
        Report file name with .xlsx extension.
    """
    return 'Расчет-{date}.xlsx'.format(
        date=datetime.now().strftime('%H:%M-%m.%d.%Y'),
    )


def add_header(sheet: Worksheet, columns_names: list[str]) -> None:
    """Add header with bold columns names to sheet.

    Args:
        sheet: Target worksheet.
        columns_names: Names of columns in header.
    """
    header_font = Font(bold=True)
    for column, column_name in enumerate(columns_names):
        cell = sheet.cell(1, column + 1, value=column_name)
        cell.font = header_font


def create_calculations_report(
    calculations_results: list[tuple[ArticleItem, Decimal]],
    total_price: Decimal,
) -> tuple[bytes, str]:
    """Generate Excel calculations report.

    Args:
        calculations_results: List with item sand their costs.
        total_price: Total items price.

    Returns:
        File data and name.
    """
    workbook = Workbook()
    sheet = workbook.active

    add_header(sheet, ['Наименование', 'Цена'])

    for article_item, price in calculations_results:
        sheet.append([
            article_item.name,
            price,
        ])

    sheet.append([])
    sheet.append(['Общая стоимость', total_price])

    file_buffer = BytesIO()
    workbook.save(file_buffer)
    return file_buffer.getvalue(), generate_report_name()
