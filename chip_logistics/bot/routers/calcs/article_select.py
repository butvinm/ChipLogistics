"""Article select routes."""


from decimal import Decimal, DecimalException

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.calcs import (
    AddItemCallback,
    ManualArticleCallback,
    SelectArticleCallback,
)
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.calcs import CalculationsState
from chip_logistics.bot.views.calcs.article_select import (
    send_article_request,
    send_bad_duty_fee_ratio,
    send_duty_fee_ratio_request,
    send_name_request,
)
from chip_logistics.bot.views.calcs.item_data import send_item_count_request
from chip_logistics.core.articles.service import ArticlesService
from chip_logistics.models.articles import ArticleInfo
from chip_logistics.utils.decimal import parse_decimal

router = Router(name='calcs/article')


@router.callback_query(
    AddItemCallback.filter(),
    ExtractMessage,
)
async def open_article_select(
    callback_query: CallbackQuery,
    message: Message,
    articles_service: ArticlesService,
    state: FSMContext,
) -> HandlerResult:
    """Ask for article selection or manual input.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        articles_service: Articles service.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await state.set_state(CalculationsState.wait_article)
    articles = await articles_service.find_articles()
    await send_article_request(message, articles)
    return Ok()


@router.callback_query(
    SelectArticleCallback.filter(),
    CalculationsState.wait_article,
    ExtractMessage,
)
async def handle_article(
    callback_query: CallbackQuery,
    message: Message,
    callback_data: SelectArticleCallback,
    articles_service: ArticlesService,
    state: FSMContext,
) -> HandlerResult:
    """Save selected article data to state.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        callback_data: Callback data with article id.
        articles_service: Articles service.
        state: Current FSM state.

    Returns:
        Ok - article data successfully taken.
        Err - article not found.
    """
    article = await articles_service.get_article(callback_data.article_id)
    if article is None:
        return Err(
            message='Article {article_id} not found'.format(
                article_id=callback_data.article_id,
            ),
        )

    await state.update_data(
        name=article.name,
        duty_fee_ratio=str(article.duty_fee_ratio),
    )
    await state.set_state(CalculationsState.wait_item_count)
    await send_item_count_request(message)
    return Ok(extra={
        'name': article.name,
        'duty_fee_ratio': article.duty_fee_ratio,
    })


@router.callback_query(
    ManualArticleCallback.filter(),
    CalculationsState.wait_article,
    ExtractMessage,
)
async def start_manual_article_input(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Request for article name input.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await state.set_state(CalculationsState.wait_article_name)
    await send_name_request(message)
    return Ok()


@router.message(
    CalculationsState.wait_article_name,
    TextMessage,
)
async def handle_name(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Save name to state and ask duty fee ratio.

    Args:
        message: Message where query from.
        text: Input name.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await state.update_data(name=text)
    await state.set_state(CalculationsState.wait_article_duty_fee_ratio)
    await send_duty_fee_ratio_request(message)
    return Ok(extra={'name': text})


@router.message(
    CalculationsState.wait_article_duty_fee_ratio,
    TextMessage,
)
async def handle_duty_fee_ratio(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Handle duty fee ratio and ask for item count.

    Args:
        message: Message where query from.
        text: Input duty fee ratio.
        state: Current FSM state.

    Returns:
        Ok - duty fee ratio successfully handled.
        Err - incorrect duty fee ratio format.
    """
    try:
        duty_fee_ratio = parse_decimal(text) / Decimal(100) + 1
    except DecimalException as convert_error:
        await send_bad_duty_fee_ratio(message)
        return Err(
            error=str(convert_error),
            message='Incorrect duty fee ratio format.',
        )

    await state.update_data(duty_fee_ratio=str(duty_fee_ratio))
    await state.set_state(CalculationsState.wait_item_count)

    context = await state.get_data()
    article = ArticleInfo(id=None, **context)
    await send_item_count_request(message)
    return Ok(extra={
        'name': article.name,
        'duty_fee_ratio': article.duty_fee_ratio,
    })
