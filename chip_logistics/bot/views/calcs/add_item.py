"""Item data views."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from chip_logistics.bot.callbacks.calcs import ItemPriceCurrencyCallback
from chip_logistics.bot.texts.calcs import (
    ASK_ITEM_COUNT,
    ASK_ITEM_NAME,
    ASK_ITEM_PRICE_CURRENCY,
    ASK_ITEM_UNIT_PRICE,
    ASK_ITEM_UNIT_WEIGHT,
    BAD_ITEM_COUNT,
    BAD_ITEM_UNIT_PRICE,
    BAD_ITEM_UNIT_WEIGHT,
)
from chip_logistics.core.articles.models import Currency


async def send_item_name_request(
    message: Message,
) -> None:
    """Ask article item name.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_ITEM_NAME)


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


currencies_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=currency,
                callback_data=ItemPriceCurrencyCallback(
                    currency=currency,
                ).pack(),
            ),
        ]
        for currency in Currency
    ],
)


async def send_item_price_currency_request(
    message: Message,
) -> None:
    """Ask article item price currency.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=ASK_ITEM_PRICE_CURRENCY,
        reply_markup=currencies_kb,
    )


async def send_item_unit_price_request(
    message: Message,
    currency: Currency,
) -> None:
    """Ask article item unit price.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        currency: Currency to show in the message.
    """
    await message.answer(text=ASK_ITEM_UNIT_PRICE.format(currency=currency))


async def send_bad_item_unit_price(
    message: Message,
) -> None:
    """Warn about incorrect price format.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=BAD_ITEM_UNIT_PRICE)
