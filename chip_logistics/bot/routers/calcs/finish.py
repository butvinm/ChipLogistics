"""Finish router."""


from typing import Any, Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.calcs import FinishCalcsCallback
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.finish import send_calcs_report
from chip_logistics.core.amocrm.api import attach_file_to_contact, upload_file
from chip_logistics.core.amocrm.client import AmoCRMClient
from chip_logistics.core.articles.articles import calculate_articles_price
from chip_logistics.core.articles.currencies import CurrenciesService
from chip_logistics.core.articles.models import ArticleItem
from chip_logistics.core.articles.repo import ReportTemplateRepo
from chip_logistics.core.articles.report import create_calculations_report

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
    currencies_service: CurrenciesService,
    report_template_repo: ReportTemplateRepo,
) -> HandlerResult:
    """Send contact select menu.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.
        amocrm_client: AmoCRM client data to access API.
        currencies_service: Currencies operations provider.
        report_template_repo: Report templates storage.

    Returns:
        Ok - report file successfully created.
        Err - file upload fails.
    """
    context = await state.get_data()
    report = await get_report(
        currencies_service,
        report_template_repo,
        context.get('items', []),
        context.get('customer_name', ''),
    )
    if report is None:
        return Err(message='Report building failed')

    report_data, report_name = report
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
    currencies_service: CurrenciesService,
    report_template_repo: ReportTemplateRepo,
    articles_data: list[dict[str, Any]],
    customer_name: str,
) -> Optional[tuple[bytes, str]]:
    """Calculate price and form report.

    Args:
        currencies_service: Currencies operations provider.
        report_template_repo: Report templates storage.
        articles_data: Entered articles data from FSM context.
        customer_name: Entered customer_name from FSM context.

    Returns:
        Calculations report.
    """
    articles_items = [
        ArticleItem(**item_data)
        for item_data in articles_data
    ]
    calculations_results, total_price = await calculate_articles_price(
        currencies_service,
        articles_items,
    )
    report_template = await report_template_repo.get_template()
    if report_template is None:
        return None

    return create_calculations_report(
        calculations_results,
        total_price,
        customer_name,
        report_template,
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
