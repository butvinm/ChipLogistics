"""Articles service.

Contains logic for managing articles list, calculate articles items price.
"""


from decimal import Decimal

from pricecalcbot.core.articles import calcs
from pricecalcbot.core.articles.repo import ArticlesRepository
from pricecalcbot.models.articles import ArticleInfo, ArticleItem


class ArticlesService(object):
    """Articles service.

    Provide following functionalities:
    - CRUD over list with information about articles names and fee.
    - Calculation of price of one article item.
    """

    def __init__(self, repo: ArticlesRepository) -> None:
        """Initialize service.

        Args:
            repo: Articles repository.
        """
        self._repo = repo

    async def find_articles(self, query: str) -> list[ArticleInfo]:
        """Find articles by name.

        Search is case and word position insensitive.

        So, for names ['fOo', 'Bar', 'bar foo'] query
        'foo' would find ['fOo', 'bar foo'].

        Args:
            query: Name query.

        Returns:
            List of found articles.
        """
        articles = await self._repo.get_articles()
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
