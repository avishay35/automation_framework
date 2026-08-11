import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from config.settings import settings
from src.api.auth_client import AuthClient


@pytest.fixture(scope="session")
def global_settings():
    """Provides access to application configuration across all tests."""
    return settings


@pytest.fixture(scope="session")
def auth_token() -> str:
    """Session-scoped fixture to obtain a single JWT token for test user."""
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