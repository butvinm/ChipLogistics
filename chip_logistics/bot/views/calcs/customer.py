"""Customer info dialog view."""


from aiogram.types import Message

from chip_logistics.bot.texts.calcs import ASK_CUSTOMER_NAME


async def send_customer_name_request(
    message: Message,
) -> None:
    """Ask for customer name.

    Args:
        message: Message answer to.
    """
    await message.answer(
        text=ASK_CUSTOMER_NAME,
    )
