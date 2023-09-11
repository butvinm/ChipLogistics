"""Finish calculations views."""

from aiogram.types import BufferedInputFile, Message

from pricecalcbot.bot.texts.calcs import CALCS_RESULT


async def send_calcs_report(
    message: Message,
    report_data: bytes,
    report_name: str,
) -> None:
    """Show finish message with calculations results.

    Args:
        message: Message. Can be used to answer, modify or get user info.
        report_data: Report file data.
        report_name: Report file name.
    """
    await message.answer_document(
        caption=CALCS_RESULT,
        document=BufferedInputFile(report_data, report_name),
    )
