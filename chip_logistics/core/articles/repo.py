"""Articles repository."""


from typing import Optional, Protocol, runtime_checkable

from chip_logistics.core.articles.models import ArticleInfo
from chip_logistics.utils.closing import AClosing


@runtime_checkable
class ArticlesRepo(AClosing, Protocol):
    """Interface of articles repository.

    Articles repository provide CRUD over articles info in database.
    """

    async def put_article(self, article: ArticleInfo) -> ArticleInfo:
        """Add article to repository.

        If article with same id exists, it will bew updated.

        If article id is None, it will be auto-generated.

        Args:
            article: Article data.

        Returns:
            Created or updated article.
        """

    async def get_articles(self) -> list[ArticleInfo]:
        """Get list of all articles in repository.

        Returns:
            Articles info.
        """

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

    async def get_article(self, article_id: str) -> Optional[ArticleInfo]:
        """Get article from repository by id.

        Args:
            article_id: Article identifier.

        Returns:
            Found article or None.
        """

    async def delete_article(self, article_id: str) -> bool:
        """Delete article from repository.

        Args:
            article_id: Id of article to delete.

        Returns:
            True if article deleted.
        """
