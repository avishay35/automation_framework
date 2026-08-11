import pytest
from playwright.sync_api import Page, expect
from src.pages.settings_page import SettingsPage
from src.pages.home_page import HomePage


@pytest.mark.ui
def test_authenticated_user_accesses_settings(authenticated_page: Page):
    """Verifies that an authenticated user can access /settings without going through UI login."""
    settings_page = SettingsPage(authenticated_page).load()
    
    expect(settings_page.heading).to_be_visible()
    expect(settings_page.logout_button).to_be_visible()


@pytest.mark.ui
def test_authenticated_user_sees_user_feed(authenticated_page: Page):
    """Verifies that 'Your Feed' tab is available for authenticated user on Home page."""
    home_page = HomePage(authenticated_page).load()
    
    expect(home_page.your_feed_tab).to_be_visible()


@pytest.mark.ui
def test_logout_clears_session(authenticated_page: Page):
    """Verifies logging out redirects home and removes authenticated elements."""
    settings_page = SettingsPage(authenticated_page).load()
    settings_page.logout()

    home_page = HomePage(authenticated_page)
    expect(home_page.navbar.sign_in_link).to_be_visible()