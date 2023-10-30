"""Tests for articles module."""


from decimal import Decimal
from random import choices
from string import ascii_letters, digits
from typing import AsyncGenerator, Optional

import pytest

from chip_logistics.core.articles.articles import (
    create_article,
    delete_article,
    find_articles,
)
from chip_logistics.core.articles.models import ArticleInfo
from chip_logistics.core.articles.repo import ArticlesRepo
from tests.articles.conftest import (
    ARTICLE_NAME_PREFIX,
    gen_article_name,
    test_articles,
)


class ArticlesRepoStub(ArticlesRepo):
    """Stub of articles repository.

    Articles stored in the dictionary.
    """

    def __init__(self) -> None:
        """Initialize repository with empty articles dict."""
        super().__init__()
        self._articles: dict[str, ArticleInfo] = {}

    async def put_article(self, article: ArticleInfo) -> ArticleInfo:
        """Put article to the dict.

        Args:
            article: Article data.

        Returns:
            Created or updated article.
        """
        if article.id is None:
            article.id = self._gen_article_id()

        self._articles[article.id] = article
        return article

    async def delete_article(self, article_id: str) -> bool:
        """Delete article from dict.

        Args:
            article_id: Id of article to delete.

        Returns:
            True if article deleted.
        """
        if article_id in self._articles:
            self._articles.pop(article_id)
            return True

        return False

    async def get_article(self, article_id: str) -> Optional[ArticleInfo]:
        """Ger article from dict.

        Args:
            article_id: Article identifier.

        Returns:
            Found article or None.
        """
        return self._articles.get(article_id)

    async def get_articles(self) -> list[ArticleInfo]:
        """Get all articles from dict.

        Returns:
            Articles info.
        """
        return list(self._articles.values())

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

    async def close(self) -> None:
        """Close repository and clean resources."""
        self._articles = {}

    def _gen_article_id(self) -> str:
        """Generate random article id.

        Returns:
            12-chars random string.
        """
        size = 12
        return ''.join(choices(ascii_letters + digits, k=size))  # noqa: S311


@pytest.fixture
async def repo() -> AsyncGenerator[ArticlesRepo, None]:
    """Get article repo stub instance.

    Repository is prefilled with test_articles.

    Yields:
        Articles repository stub.
    """
    async with ArticlesRepoStub() as repo:
        for article, _ in test_articles:
            await repo.put_article(
                ArticleInfo(id=None, **article.model_dump()),
            )
        yield repo


TEST_NAME = gen_article_name()
TEST_FEE = Decimal('1.5')


async def test_create_article(repo: ArticlesRepo) -> None:
    """
    Test the create_article method of ArticlesService.

    This test checks if the create_article method correctly creates
    a new article and returns it with the expected attributes.

    Args:
        repo: Mocked articles storage.
    """
    article = await create_article(repo, TEST_NAME, TEST_FEE)
    assert article.name == TEST_NAME
    assert article.duty_fee_ratio == TEST_FEE


async def test_find_articles(repo: ArticlesRepo) -> None:
    """
    Test the find_articles method of ArticlesService.

    This test checks if the find_articles method
    correctly filters articles based on a query.

    Args:
        repo: Mocked articles storage.
    """
    articles = await find_articles(repo, ARTICLE_NAME_PREFIX)
    assert len(articles) == len(test_articles)

    articles = await find_articles(repo, test_articles[0][0].name)
    assert len(articles) == 1

    articles = await find_articles(repo, 'ENDOFUNCTOR!!!')
    assert len(articles) == 0


async def test_delete_article(repo: ArticlesRepo) -> None:
    """
    Test the delete_article method of ArticlesService.

    This test checks if the delete_article method
    correctly deletes an article and returns True.

    Args:
        repo: Mocked articles storage.
    """
    article = (await repo.get_articles())[0]
    assert article.id is not None

    deleted = await delete_article(repo, article.id)
    assert deleted is True
    assert await repo.get_article(article.id) is None
