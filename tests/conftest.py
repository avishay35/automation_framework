import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from config.settings import settings


@pytest.fixture(scope="session")
def global_settings():
    """Provides access to application configuration across all tests."""
    return settings


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