"""Article price calculation."""

import math
from decimal import Decimal

from chip_logistics.core.articles.models import ArticleItem

CalculationsResults = list[tuple[ArticleItem, Decimal]]

# Price of one kg of article weight for air delivery
AIR_DELIVERY_PRICE_PER_KG = 12
CUSTOM_FEE_RATIO = Decimal(215) / Decimal(1000)  # noqa: WPS432
PRICE_MARGIN_RATIO = Decimal(20) / Decimal(100)  # noqa: WPS432
RUSSIAN_DELIVERY_RATIO = (
    (100, Decimal(6)),
    (50, Decimal(5)),
    (25, Decimal(4)),
    (5, Decimal(3)),
)


def calculate_air_delivery_price(total_weight: Decimal) -> Decimal:
    """Calculate the air delivery price.

    Args:
        total_weight: The total weight of the order.

    Returns:
        The air delivery price.
    """
    return Decimal(math.ceil(total_weight)) * AIR_DELIVERY_PRICE_PER_KG


def calculate_price_for_custom(
    total_price: Decimal,
    air_delivery_price: Decimal,
) -> Decimal:
    """Calculate the total price for custom including delivery.

    Args:
        total_price: The total price of the order.
        air_delivery_price: The air delivery price.

    Returns:
        The total price for custom including delivery.
    """
    return total_price + air_delivery_price


def calculate_custom_fee(price_for_custom: Decimal) -> Decimal:
    """Calculate the custom fee.

    Args:
        price_for_custom: The total price for custom including delivery.

    Returns:
        The custom fee.
    """
    return price_for_custom * CUSTOM_FEE_RATIO


def calculate_duty_fee(
    total_price: Decimal,
    duty_fee_ratio: Decimal,
) -> Decimal:
    """Calculate the duty fee.

    Args:
        total_price: The total price of the order.
        duty_fee_ratio: The duty fee ratio.

    Returns:
        The duty fee.
    """
    return total_price * (duty_fee_ratio - 1)


def calculate_russian_delivery_price(
    air_delivery_price: Decimal,
    total_weight: Decimal,
) -> Decimal:
    """Calculate Russian delivery price.

    See RUSSIAN_DELIVERY_RATIO for transformations rules.

    Args:
        air_delivery_price: The air delivery price.
        total_weight: The total weight of the item.

    Returns:
        Russian delivery price.
    """
    for threshold, ratio in RUSSIAN_DELIVERY_RATIO:
        if total_weight > threshold:
            return air_delivery_price / ratio

    return air_delivery_price


def calculate_price_with_fee(
    invoice_and_delivery_for_custom: Decimal,
    russia_delivery_price: Decimal,
    custom_fee: Decimal,
    duty_fee: Decimal,
) -> Decimal:
    """Calculate the final price with all fees.

    Args:
        invoice_and_delivery_for_custom: \
            The total price for custom including delivery.
        russia_delivery_price: The delivery price for Russia.
        custom_fee: The custom fee.
        duty_fee: The duty fee.

    Returns:
        The final price including all fees.
    """
    invoice_and_delivery_with_custom_fee = (
        invoice_and_delivery_for_custom + custom_fee + russia_delivery_price
    )
    return invoice_and_delivery_with_custom_fee + duty_fee


def calculate_article_price(article_item: ArticleItem) -> Decimal:
    """Calculate the total price for an article including all fees.

    Args:
        article_item: The article for which to calculate the price.

    Returns:
        The final price for the article including all fees.
    """
    total_weight = article_item.unit_weight * article_item.count
    total_price = article_item.unit_price * article_item.count
    air_delivery_price = calculate_air_delivery_price(total_weight)

    invoice_and_delivery_for_custom = calculate_price_for_custom(
        total_price,
        air_delivery_price,
    )
    custom_fee = calculate_custom_fee(invoice_and_delivery_for_custom)
    duty_fee = calculate_duty_fee(
        total_price,
        article_item.duty_fee_ratio,
    )
    russia_delivery_price = calculate_russian_delivery_price(
        air_delivery_price,
        total_weight,
    )

    price_with_fee = calculate_price_with_fee(
        invoice_and_delivery_for_custom,
        russia_delivery_price,
        custom_fee,
        duty_fee,
    )
    price_with_margin = price_with_fee * (1 + PRICE_MARGIN_RATIO)
    return round(price_with_margin, 1)


def calculate_total_price(
    calculations_results: list[tuple[ArticleItem, Decimal]],
) -> Decimal:
    """Calculate items prices sum.

    Args:
        calculations_results: List with item sand their costs.

    Returns:
        Total price.
    """
    return sum((price for _, price in calculations_results), Decimal(0))
