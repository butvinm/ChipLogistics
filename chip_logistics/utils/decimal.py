"""Utilities for decimal numbers."""


from decimal import Decimal


def parse_decimal(text: str) -> Decimal:
    """Parse decimal from string.

    Normalize string before parsing and allow comma as well as dot.

    Args:
        text: String to parse.

    Returns:
        Parsed decimal with default context.

    Raises:
        DecimalException: if text is not valid decimal.  # noqa: DAR402
    """
    text = text.replace(' ', '')
    text = text.replace(',', '.')
    return Decimal(text)
