"""Finish router."""


from typing import Any

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.calcs import FinishCalcsCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.finish import send_calcs_report
from chip_logistics.core.amocrm.api import attach_file_to_contact, upload_file
from chip_logistics.core.amocrm.client import AmoCRMClient
from chip_logistics.core.articles.models import ArticleItem
from chip_logistics.core.articles.service import ArticlesService

router = Router(name='calcs/finish')


@router.callback_query(
    CalculationsState.wait_contact_select,
    FinishCalcsCallback.filter(),
    ExtractMessage,
)
async def finish_calcs(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
    amocrm_client: AmoCRMClient,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Send contact select menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.
        amocrm_client: AmoCRM client data to access API.
        articles_service: Articles service.

    Returns:
        Ok - report file successfully created.
        Err - file upload fails.
    """
    context = await state.get_data()
    report_data, report_name = await get_report(
        context.get('items', []),
        context.get('customer_name', ''),
        articles_service,
    )

    contact_id = context.get('contact_id')
    if contact_id is not None:
        await upload_report_file_to_amocrm(
            report_data,
            report_name,
            contact_id,
            amocrm_client,
        )

    await send_calcs_report(
        message,
        report_data,
        report_name,
    )
    await state.clear()
    return Ok()


async def get_report(
    articles_data: list[dict[str, Any]],
    customer_name: str,
    articles_service: ArticlesService,
) -> tuple[bytes, str]:
    """Calculate price and form report.

    Args:
        articles_data: Entered articles data from FSM context.
        customer_name: Entered customer_name from FSM context.
        articles_service: Articles service.

    Returns:
        Calculations report.
    """
    articles_items = [
        ArticleItem(**item_data)
        for item_data in articles_data
    ]
    calculations_results, total_price = await articles_service.calculate_articles_price(  # noqa: E501
        articles_items,
    )
    return articles_service.create_calculations_report(
        calculations_results,
        total_price,
        customer_name,
    )


async def upload_report_file_to_amocrm(
    report_data: bytes,
    report_name: str,
    contact_id: int,
    amocrm_client: AmoCRMClient,
) -> None:
    """Upload report to AmoCRM and attach to contact.

    Args:
        report_data: Report file data.
        report_name: Report file name.
        contact_id: Contact identifier.
        amocrm_client: AmoCRM client data to access API.
    """
    report_file_uuid = await upload_file(
        amocrm_client,
        file_name=report_name,
        file_data=report_data,
    )
    await attach_file_to_contact(
        amocrm_client,
        contact_id=contact_id,
        file_uuid=report_file_uuid,
    )
