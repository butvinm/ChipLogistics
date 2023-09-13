"""Item data views."""

from aiogram.types import Message

from chip_logistics.bot.texts.calcs import (
    ASK_ITEM_COUNT,
    ASK_ITEM_UNIT_PRICE,
    ASK_ITEM_UNIT_WEIGHT,
    BAD_ITEM_COUNT,
    BAD_ITEM_UNIT_PRICE,
    BAD_ITEM_UNIT_WEIGHT,
)


async def send_item_count_request(
    message: Message,
) -> None:
    """Ask article item count.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_ITEM_COUNT)


async def send_bad_item_count(
    message: Message,
) -> None:
    """Warn about incorrect count format.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=BAD_ITEM_COUNT)


async def send_item_unit_weight_request(
    message: Message,
) -> None:
    """Ask article item unit weight.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_ITEM_UNIT_WEIGHT)


async def send_bad_item_unit_weight(
    message: Message,
) -> None:
    """Warn about incorrect weight format.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=BAD_ITEM_UNIT_WEIGHT)


async def send_item_unit_price_request(
    message: Message,
) -> None:
    """Ask article item unit price.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_ITEM_UNIT_PRICE)


async def send_bad_item_unit_price(
    message: Message,
) -> None:
    """Warn about incorrect price format.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=BAD_ITEM_UNIT_PRICE)
