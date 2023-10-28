"""Tests for articles service."""


from decimal import Decimal
from random import choices
from string import ascii_letters, digits
from typing import AsyncGenerator, Optional

import pytest
from chip_logistics.core.articles.currencies import CurrenciesService

from chip_logistics.core.articles.repo import ArticlesRepository
from chip_logistics.core.articles.service import ArticlesService
from chip_logistics.core.articles.models import ArticleInfo, ArticleItem
from tests.articles.conftest import test_articles


class ArticlesRepositoryStub(ArticlesRepository):
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
async def repo() -> AsyncGenerator[ArticlesRepository, None]:
    """Get article repo stub instance.

    Repository is prefilled with test_articles.

    Yields:
        Articles repository stub.
    """
    async with ArticlesRepositoryStub() as repo:
        for article, _ in test_articles:
            await repo.put_article(
                ArticleInfo(id=None, **article.model_dump()),
            )
        yield repo


@pytest.fixture
async def currencies_service(
    fixer_api_key: str,
) -> AsyncGenerator[CurrenciesService, None]:
    """Get currencies service instance.

    Args:
        fixer_api_key: Fixer API key.

    Yields:
        Currencies service.
    """
    async with CurrenciesService(fixer_api_key) as service:
        yield service


@pytest.fixture
async def service(
    repo: ArticlesRepository,
    currencies_service: CurrenciesService,
) -> ArticlesService:
    """Get articles service instance.

    Args:
        repo: Articles repository.
        currencies_service: Currencies service.

    Returns:
        Articles service.
    """
    return ArticlesService(repo, currencies_service)


TEST_NAME = 'Test Article'
TEST_FEE = Decimal('1.5')


async def test_create_article(service: ArticlesService) -> None:
    """
    Test the create_article method of ArticlesService.

    This test checks if the create_article method correctly creates
    a new article and returns it with the expected attributes.

    Args:
        service: ArticlesService instance with a mock repository.
    """
    article = await service.create_article(TEST_NAME, TEST_FEE)
    assert article.name == TEST_NAME
    assert article.duty_fee_ratio == TEST_FEE


async def test_find_articles(service: ArticlesService) -> None:
    """
    Test the find_articles method of ArticlesService.

    This test checks if the find_articles method
    correctly filters articles based on a query.

    Args:
        service: ArticlesService instance with a mock repository.
    """
    articles = await service.find_articles('Article')
    assert len(articles) == len(test_articles)

    articles = await service.find_articles('8')
    assert len(articles) == 1


async def test_delete_article(
    service: ArticlesService,
    repo: ArticlesRepository,
) -> None:
    """
    Test the delete_article method of ArticlesService.

    This test checks if the delete_article method
    correctly deletes an article and returns True.

    Args:
        service: ArticlesService instance with a mock repository.
        repo: Mock repository instance.
    """
    article = (await repo.get_articles())[0]
    assert article.id is not None

    deleted = await service.delete_article(article.id)
    assert deleted is True
    assert await repo.get_article(article.id) is None


@pytest.mark.parametrize(
    'article,expected_price',
    test_articles,
)
async def test_calculate_article_item_price(
    article: ArticleItem,
    expected_price: Decimal,
    service: ArticlesService,
) -> None:
    """
    Test the calculate_article_item_price method of ArticlesService.

    This test checks if the calculate_article_item_price method
    correctly calculates the price of an article item.

    Args:
        article: The article for which to calculate the price.
        expected_price: Expected function result.
        service: ArticlesService instance with a mock repository.
    """
    assert service.calculate_article_item_price(article) == expected_price
