import pytest
from playwright.sync_api import Page
from src.pages.home_page import HomePage
from src.pages.article_page import ArticlePage
from src.api.models.article import ArticleModel
from playwright.sync_api import expect

@pytest.mark.e2e
def test_view_api_created_article_in_ui(
    authenticated_page: Page,
    created_article: ArticleModel
):
    """
    Hybrid E2E Test:
    - Setup: Article created via API fixture (0.2s).
    - Execution: Navigate directly to article URL via UI.
    - Verification: Assert article title and content render correctly in the DOM.
    - Teardown: Article deleted via API fixture automatically.
    """
    home_page = HomePage(authenticated_page)
    article_page = ArticlePage(authenticated_page)
    
    # 1. Direct UI navigation using slug from API response
    home_page.navigate_to(f"/article/{created_article.slug}")
    
    # 2. UI Verification
    expect(article_page.title_heading).to_be_visible()
    assert article_page.title_heading.inner_text() == created_article.title
    assert article_page.body_text.inner_text() == created_article.body