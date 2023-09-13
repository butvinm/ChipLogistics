"""Articles management callbacks."""

from aiogram.filters.callback_data import CallbackData


class OpenArticlesMenuCallback(CallbackData, prefix='articles/open'):
    """Open articles management menu."""


class OpenArticlesListCallback(CallbackData, prefix='articles/list/open'):
    """Open articles list."""


class CreateArticleCallback(CallbackData, prefix='articles/create'):
    """Start creating of the new article."""


class ConfirmArticleCreateCallback(
    CallbackData,
    prefix='articles/create/confirm',
):
    """Confirm article creation."""


class OpenArticleCallback(
    CallbackData,
    prefix='articles/list/article',
):
    """Open article menu."""

    article_id: str


class DeleteArticleCallback(
    CallbackData,
    prefix='articles/list/article/delete',
):
    """Delete article."""

    article_id: str
