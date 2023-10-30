"""Articles module.

Contain following functionalities:
- CRUD over list with information about articles names and fee.
- Calculation of price of one article item.
"""


from decimal import Decimal
from typing import Optional

from chip_logistics.core.articles.calcs import (
    CalculationsResults,
    calculate_article_price,
    calculate_total_price,
)
from chip_logistics.core.articles.currencies import CurrenciesService
from chip_logistics.core.articles.models import (
    ArticleInfo,
    ArticleItem,
    Currency,
)
from chip_logistics.core.articles.repo import ArticlesRepo


async def get_article(
    repo: ArticlesRepo,
    article_id: str,
) -> Optional[ArticleInfo]:
    """Get article by id.

    Args:
        repo: Articles storage.
        article_id: Article id.

    Returns:
        Article if found.
    """
    return await repo.get_article(article_id)


async def find_articles(
    repo: ArticlesRepo,
    query: Optional[str] = None,
) -> list[ArticleInfo]:
    """Find articles by name.

    Search is case and word position insensitive.

    So, for names ['fOo', 'Bar', 'bar foo'] query
    'foo' would find ['fOo', 'bar foo'].

    Args:
        repo: Articles storage.
        query: Name query. If None, all articles returned.

    Returns:
        List of found articles.
    """
    return await repo.find_articles(query)


async def create_article(
    repo: ArticlesRepo,
    name: str,
    duty_fee_ratio: Decimal,
) -> ArticleInfo:
    """Create new articles.

    Args:
        repo: Articles storage.
        name: Article name.
        duty_fee_ratio: Article duty fee ration.

    Returns:
        Created article.
    """
    article = ArticleInfo(
        id=None,
        name=name,
        duty_fee_ratio=duty_fee_ratio,
    )
    return await repo.put_article(article)


async def delete_article(
    repo: ArticlesRepo,
    article_id: str,
) -> bool:
    """Delete article from repository.

    Args:
        repo: Articles storage.
        article_id: Id of article to delete.

    Returns:
        True if article deleted.
    """
    return await repo.delete_article(article_id)


async def _convert_item_to_usd(
    currencies_service: CurrenciesService,
    article_item: ArticleItem,
) -> Optional[ArticleItem]:
    """Create new item instance with price converted to USD.

    Args:
        currencies_service: Currencies operation provider.
        article_item: Item with price in some currency.

    Returns:
        Article item with unit_price in USD if price
        successfully converted.
    """
    usd_price = await currencies_service.convert_price(
        article_item.unit_price,
        article_item.price_currency,
        Currency.usd,
        use_cached=True,
    )
    if usd_price is None:
        return None

    usd_item = ArticleItem(**article_item.model_dump())
    usd_item.price_currency = Currency.usd
    usd_item.unit_price = usd_price
    return usd_item


async def calculate_articles_price(
    currencies_service: CurrenciesService,
    articles_items: list[ArticleItem],
) -> tuple[CalculationsResults, Decimal]:
    """Calculate prices for all items.

    All prices converted to USD.

    Args:
        currencies_service: Currencies operation provider.
        articles_items: Items for price calculating.

    Returns:
        Items prices and total price.
    """
    usd_articles_items = [
        await _convert_item_to_usd(currencies_service, article_item)
        for article_item in articles_items
    ]
    calculations_results = [
        (
            article_item,
            calculate_article_price(article_item),
        )
        for article_item in usd_articles_items
        if article_item is not None
    ]
    total_price = calculate_total_price(
        calculations_results,
    )
    return calculations_results, total_price
