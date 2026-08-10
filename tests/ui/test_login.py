import pytest
from playwright.sync_api import Page, expect
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage
from config.settings import settings


@pytest.mark.ui
def test_login_page_elements_visible(page: Page):
    """Verifies that key elements on the login page load correctly."""
    login_page = LoginPage(page).load()
    
    expect(login_page.email_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.submit_button).to_be_enabled()


@pytest.mark.ui
def test_invalid_login_shows_error(page: Page):
    """Verifies error message handling on invalid credentials."""
    login_page = LoginPage(page).load()
    login_page.login("invalid_user@example.com", "WrongPassword123")
    
    errors = login_page.get_error_messages()
    assert len(errors) > 0
    assert any("email or password" in err.lower() for err in errors)


@pytest.mark.ui
def test_navigate_from_home_to_login(page: Page):
    """Verifies navigation from Home page navbar to Login page."""
    home_page = HomePage(page).load()
    home_page.navbar.click_sign_in()
    
    login_page = LoginPage(page)
    expect(login_page.heading).to_be_visible()