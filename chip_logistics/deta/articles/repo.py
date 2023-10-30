"""ArticlesRepository based on Deta Base."""


from secrets import choice
from string import ascii_letters, digits
from typing import Optional

from deta import Deta

from chip_logistics.core.articles.models import ArticleInfo
from chip_logistics.core.articles.repo import ArticlesRepository
from chip_logistics.deta.models import model_dump


class DetaArticlesRepository(ArticlesRepository):
    """ArticlesRepository based on Deta Base.

    Articles are stored in the `articles` base.
    """

    def __init__(self, deta: Deta) -> None:
        """Init repository.

        Args:
            deta: Deta API.
        """
        super().__init__()
        self._base = deta.AsyncBase('articles')

    async def put_article(self, article: ArticleInfo) -> ArticleInfo:
        """Add article to base.

        If article with same id exists, it will bew updated.

        If article id is None, it will be auto-generated.

        Args:
            article: Article data.

        Returns:
            Created or updated article.
        """
        if article.id is None:
            article = ArticleInfo(**article.model_dump())
            article.id = self._generate_id()

        article_data = await self._base.put(
            data=model_dump(article),
            key=article.id,
        )
        return ArticleInfo(**article_data)

    async def get_articles(self) -> list[ArticleInfo]:
        """Get list of all articles in base.

        Returns:
            Articles info.
        """
        articles_result = await self._base.fetch()
        return [
            ArticleInfo(**article_data)
            for article_data in articles_result.items
        ]

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
        articles = await self.get_articles()
        if query is None:
            return articles

        return [
            article for article in articles
            if query.lower() in article.name.lower()
        ]

    async def get_article(self, article_id: str) -> Optional[ArticleInfo]:
        """Get article from base by id.

        Args:
            article_id: Article identifier.

        Returns:
            Found article or None.
        """
        article_data = await self._base.get(article_id)
        if article_data is None:
            return article_data

        return ArticleInfo(**article_data)

    async def delete_article(self, article_id: str) -> bool:
        """Delete article from base.

        Args:
            article_id: Id of article to delete.

        Returns:
            True if article deleted.
        """
        article = await self.get_article(article_id)
        await self._base.delete(article_id)
        return article is not None

    async def close(self) -> None:
        """Close base and clean resources."""
        await self._base.close()

    def _generate_id(self) -> str:
        """Generate random article id.

        Returns:
            Random 12-chars string.
        """
        length = 12
        alphabet = ascii_letters + digits
        return ''.join(choice(alphabet) for _ in range(length))
