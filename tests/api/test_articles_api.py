import pytest
import uuid
from src.api.article_client import ArticleClient
from src.api.models.article import MultipleArticlesResponse, SingleArticleResponse


@pytest.mark.api
def test_get_global_articles_contract(article_client: ArticleClient):
    """Verifies that GET /articles returns HTTP 200 and matches expected schema contract."""
    response = article_client.get_articles(limit=5)

    assert response.status_code == 200
    
    parsed_data = MultipleArticlesResponse(**response.json())
    assert isinstance(parsed_data.articles, list)
    assert len(parsed_data.articles) <= 5


@pytest.mark.api
def test_create_and_delete_article(article_client: ArticleClient):
    """Verifies creating an article via API, validating contract, and cleaning up."""
    unique_title = f"Test Article {uuid.uuid4().hex[:8]}"
    description = "Automated test article description"
    body = "This is the body content created during automated API testing."
    tags = ["automation", "pytest"]

    # 1. Create Article (Client is authenticated by default)
    create_res = article_client.create_article(
        title=unique_title, 
        description=description, 
        body=body, 
        tags=tags
    )
    assert create_res.status_code in (200, 201)

    created_article = SingleArticleResponse(**create_res.json()).article
    assert created_article.title == unique_title
    assert created_article.description == description
    slug = created_article.slug

    # 2. Cleanup: Delete Article
    delete_res = article_client.delete_article(slug)
    assert delete_res.status_code in (200, 204)


@pytest.mark.api
def test_create_article_unauthorized_fails(article_client: ArticleClient):
    """Verifies that creating an article without an Auth header returns 401 Unauthorized."""
    # Explicitly clear token to simulate unauthenticated state on the same client
    article_client.clear_token()

    response = article_client.create_article(
        title="Unauthorized Article",
        description="Should fail",
        body="No token provided"
    )
    assert response.status_code == 401