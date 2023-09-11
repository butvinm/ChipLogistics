"""Contact select views."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from pricecalcbot.bot.callbacks.calcs import (
    FinishCalcsCallback,
    SearchContactCallback,
    SelectContactCallback,
)
from pricecalcbot.bot.texts.calcs import (
    ASK_SEARCH_QUERY,
    CONTACT_SEARCH_MENU,
    CONTACT_SELECTED,
    CONTINUE_SEARCH_CONTACT_BTN,
    FINISH_BTN,
    SEARCH_CONTACT_BTN,
    SEARCH_RESULT,
    SKIP_CONTACT_BTN,
)
from pricecalcbot.models.amocrm import Contact

select_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=SEARCH_CONTACT_BTN,
                callback_data=SearchContactCallback().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=SKIP_CONTACT_BTN,
                callback_data=FinishCalcsCallback().pack(),
            ),
        ],
    ],
)


async def send_contact_select_menu(
    message: Message,
) -> None:
    """Send select menu with search button.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=CONTACT_SEARCH_MENU,
        reply_markup=select_menu_kb,
    )


async def send_search_query_request(
    message: Message,
) -> None:
    """Send select menu with search button.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(text=ASK_SEARCH_QUERY)


def build_search_result_kb(contacts: list[Contact]) -> InlineKeyboardMarkup:
    """Build kb with contacts selecting buttons and skip/retry buttons.

    Args:
        contacts: Found contacts.

    Returns:
        Keyboard with search results.
    """
    builder = InlineKeyboardBuilder()

    rows_sizes: list[int] = []
    for contact in contacts:
        rows_sizes.append(1)
        builder.button(
            text=contact.name,
            callback_data=SelectContactCallback(
                contact_id=contact.id,
            ).pack(),
        )

    rows_sizes.append(2)
    builder.button(
        text=CONTINUE_SEARCH_CONTACT_BTN,
        callback_data=SearchContactCallback().pack(),
    )
    builder.button(
        text=SKIP_CONTACT_BTN,
        callback_data=FinishCalcsCallback().pack(),
    )

    builder.adjust(*rows_sizes)
    return builder.as_markup()


async def send_search_result(
    message: Message,
    contacts: list[Contact],
) -> None:
    """Send search result with contacts list.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        contacts: Found contacts.
    """
    await message.answer(
        text=SEARCH_RESULT,
        reply_markup=build_search_result_kb(contacts),
    )


contact_selected_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=FINISH_BTN,
                callback_data=FinishCalcsCallback().pack(),
            ),
        ],
    ],
)


async def send_contact_selected(
    message: Message,
) -> None:
    """Send selecting confirmation and button to finish calculations.

    Args:
        message: Message. Can be used to answer, modify or get user info.
    """
    await message.answer(
        text=CONTACT_SELECTED,
        reply_markup=contact_selected_kb,
    )
