import pytest
from playwright.sync_api import Page
from config.settings import settings


@pytest.mark.ui
def test_conduit_homepage_loads(page: Page):
    """Sanity check to confirm Playwright and Pytest environment setup."""
    page.goto(str(settings.base_url))
    assert page.title() != ""