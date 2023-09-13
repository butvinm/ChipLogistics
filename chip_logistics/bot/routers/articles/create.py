"""Article creation router."""


from decimal import Decimal, DecimalException

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from chip_logistics.bot.callbacks.articles import (
    ConfirmArticleCreateCallback,
    CreateArticleCallback,
)
from chip_logistics.bot.filters.extract_message import ExtractMessage
from chip_logistics.bot.filters.text_message import TextMessage
from chip_logistics.bot.handler_result import Err, HandlerResult, Ok
from chip_logistics.bot.states.articles import CreateArticleState
from chip_logistics.bot.views.articles.create import (
    send_bad_duty_fee_ratio,
    send_confirmation_request,
    send_created_article,
    send_duty_fee_ratio_request,
    send_name_request,
)
from chip_logistics.core.articles.service import ArticlesService
from chip_logistics.models.articles import ArticleInfo
from chip_logistics.utils.decimal import parse_decimal

router = Router(name='articles/create')


@router.callback_query(
    CreateArticleCallback.filter(),
    ExtractMessage,
)
async def start_article_creation(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
) -> HandlerResult:
    """Start article creation and ask for article name.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_name_request(message)
    await state.clear()
    await state.set_state(CreateArticleState.wait_name)
    return Ok()


@router.message(CreateArticleState.wait_name, TextMessage)
async def handle_name(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Handle article name and ask for duty fee ratio.

    Args:
        message: Message where query from.
        text: Input name.
        state: Current FSM state.

    Returns:
        Always success.
    """
    await send_duty_fee_ratio_request(message)
    await state.update_data(name=text)
    await state.set_state(CreateArticleState.wait_duty_fee_ratio)
    return Ok(extra={'name': text})


@router.message(
    CreateArticleState.wait_duty_fee_ratio,
    TextMessage,
)
async def handle_duty_fee_ratio(
    message: Message,
    text: str,
    state: FSMContext,
) -> HandlerResult:
    """Handle duty fee ratio and ask for creating confirmation.

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
    await state.set_state(CreateArticleState.wait_confirmation)

    context = await state.get_data()
    article = ArticleInfo(id=None, **context)
    await send_confirmation_request(message, article)
    return Ok(extra={'article': article})


@router.callback_query(
    ConfirmArticleCreateCallback.filter(),
    ExtractMessage,
)
async def create_article(
    callback_query: CallbackQuery,
    message: Message,
    state: FSMContext,
    articles_service: ArticlesService,
) -> HandlerResult:
    """Create new article.

    Args:
        callback_query: Open menu query.
        message: Message where query from.
        state: Current FSM state.
        articles_service: Articles service.

    Returns:
        Ok - article created successfully.
        Err - Bad context.
    """
    context = await state.get_data()
    article = ArticleInfo(id=None, **context)
    article = await articles_service.create_article(
        article.name,
        article.duty_fee_ratio,
    )
    await send_created_article(message, article)
    await state.clear()
    return Ok(extra={'article': article})
