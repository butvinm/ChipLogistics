"""Articles service.

Contains logic for managing articles list, calculate articles items price.
"""


from decimal import Decimal
from typing import Optional

from chip_logistics.core.articles import calcs, report
from chip_logistics.core.articles.currencies import CurrenciesService
from chip_logistics.core.articles.models import (
    ArticleInfo,
    ArticleItem,
    Currency,
)
from chip_logistics.core.articles.repo import ArticlesRepository


class ArticlesService(object):
    """Articles service.

    Provide following functionalities:
    - CRUD over list with information about articles names and fee.
    - Calculation of price of one article item.
    """

    def __init__(
        self,
        repo: ArticlesRepository,
        currencies_service: CurrenciesService,
    ) -> None:
        """Initialize service.

        Args:
            repo: Articles repository.
            currencies_service: Utilized for items price converting.
        """
        self._repo = repo
        self._currencies_service = currencies_service

    async def get_article(self, article_id: str) -> Optional[ArticleInfo]:
        """Get article by id.

        Args:
            article_id: Article id.

        Returns:
            Article if found.
        """
        return await self._repo.get_article(article_id)

    async def find_articles(
        self,
        query: Optional[str] = None,
    ) -> list[ArticleInfo]:
        """Find articles by name.

        Search is case and word position insensitive.

        So, for names ['fOo', 'Bar', 'bar foo'] query
        'foo' would find ['fOo', 'bar foo'].

        Args:
            query: Name query. If None, all articles returned.

        Returns:
            List of found articles.
        """
        articles = await self._repo.get_articles()
        if query is None:
            return articles

        return [
            article for article in articles
            if query.lower() in article.name.lower()
        ]

    async def create_article(
        self,
        name: str,
        duty_fee_ratio: Decimal,
    ) -> ArticleInfo:
        """Create new articles.

        Args:
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
        return await self._repo.put_article(article)

    async def delete_article(
        self,
        article_id: str,
    ) -> bool:
        """Delete article from repository.

        Args:
            article_id: Id of article to delete.

        Returns:
            True if article deleted.
        """
        return await self._repo.delete_article(article_id)

    def calculate_article_item_price(
        self,
        article_item: ArticleItem,
    ) -> Decimal:
        """Calculate price of article item.

        Args:
            article_item: Item data.

        Returns:
            Calculated price.
        """
        return calcs.calculate_article_price(article_item)

    async def calculate_articles_price(
        self,
        articles_items: list[ArticleItem],
    ) -> tuple[calcs.CalculationsResults, Decimal]:
        """Calculate prices for all items.

        All prices converted to USD.

        Args:
            articles_items: Items for price calculating.

        Returns:
            Items prices and total price.
        """
        usd_articles_items = [
            await self._convert_item_to_usd(article_item)
            for article_item in articles_items
        ]
        calculations_results = [
            (
                article_item,
                self.calculate_article_item_price(article_item),
            )
            for article_item in usd_articles_items
            if article_item is not None
        ]
        total_price = calcs.calculate_total_price(
            calculations_results,
        )
        return calculations_results, total_price

    def create_calculations_report(
        self,
        calculations_results: calcs.CalculationsResults,
        total_price: Decimal,
        customer_name: str,
    ) -> tuple[bytes, str]:
        """Generate CSV report for calculations.

        Args:
            calculations_results: List with item sand their costs.
            total_price: Total items price.
            customer_name: Customer name.

        Returns:
            File data and name.
        """
        return report.create_calculations_report(
            calculations_results,
            total_price,
            customer_name,
        )

    async def _convert_item_to_usd(
        self,
        article_item: ArticleItem,
    ) -> Optional[ArticleItem]:
        """Create new item instance with price converted to USD.

        Args:
            article_item: Item with price in some currency.

        Returns:
            Article item with unit_price in USD if price
            successfully converted.
        """
        usd_price = await self._currencies_service.convert_price(
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
