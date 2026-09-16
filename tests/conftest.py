import pytest
import uuid
from playwright.sync_api import Browser, BrowserContext, Page
from config.settings import settings
from src.api.auth_client import AuthClient
from src.api.article_client import ArticleClient
from src.api.models.article import SingleArticleResponse


@pytest.fixture(scope="session")
def global_settings():
    """Provides access to application configuration across all tests."""
    return settings


@pytest.fixture(scope="session")
def auth_token() -> str:
    """Session-scoped fixture to obtain a single JWT token for test user."""
    print("DEBUG: Using base_url:", settings.base_url)
    print("DEBUG: Using api_base_url:", settings.api_base_url)
    print("DEBUG: Using user_email:", settings.user_email)
    auth_client = AuthClient()
    return auth_client.login_and_get_token(
        email=settings.user_email,
        password=settings.user_password
    )


@pytest.fixture(scope="function")
def authenticated_context(browser: Browser, auth_token: str) -> BrowserContext:
    """
    Creates a BrowserContext with pre-injected localStorage JWT token.
    Bypasses UI login completely.
    """
    context = browser.new_context(
        base_url=str(settings.base_url),
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    context.set_default_timeout(settings.default_timeout_ms)

    # Inject JWT into localStorage via context initialization script
    # Conduit SPA looks for key 'jwtToken' or 'jwt' in localStorage
    init_script = f"""
        window.localStorage.setItem('jwtToken', '{auth_token}');
        window.localStorage.setItem('user', JSON.stringify({{
            email: '{settings.user_email}',
            token: '{auth_token}'
        }}));
    """
    context.add_init_script(init_script)

    yield context
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(authenticated_context: BrowserContext) -> Page:
    """Provides a fresh isolated page pre-authenticated with user session."""
    page = authenticated_context.new_page()
    yield page
    page.close()

    
@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Configures a custom browser context per test (viewport, timeouts, base_url)."""
    context = browser.new_context(
        base_url=str(settings.base_url),
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    context.set_default_timeout(settings.default_timeout_ms)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Provides a fresh isolated browser page per test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def article_client(auth_token: str) -> ArticleClient:
    """Provides a single ArticleClient instance pre-loaded with the session auth token."""
    return ArticleClient(auth_token=auth_token)    
    
 
@pytest.fixture(scope="function")
def created_article(article_client: ArticleClient):
    """ Hybrid Fixture:
    1. Pre-seeds a unique article via API.
    2. Yields the created article object to the UI test.
    3. Guarantees cleanup (DELETE via API) after the test finishes.
    """
    unique_title = f"Hybrid Article {uuid.uuid4().hex[:8]}"
    description = "Automated test article created via API for UI validation."
    body = "This article was created via API setup and will be cleaned up via API teardown"
    tags = ["hybrid", "pytest"]
    
    # --- SETUP (API) ---
    response = article_client.create_article(
        title=unique_title,
        description=description,
        body=body,
        tags=tags
    )
    
    assert response.status_code in (200,201), f"Fixture setup failed: {response.text}"
    
    # Here this should use the BaseAPIClient ValidateResponse method
    article_data = SingleArticleResponse(**response.json()).article
    
    # --- YIELD TO TEST ---
    yield article_data
    
    # --- TEARDOWN (API) ---
    # Runs regardless of wether the test passed, failed, or threw an exception
    delete_res = article_client.delete_article(article_data.slug)
    assert delete_res.status_code in (200,201,204), f"Fixture teardown failed: {delete_res.text}"
