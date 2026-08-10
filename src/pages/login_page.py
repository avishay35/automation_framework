from playwright.sync_api import Page, Locator, expect
from src.pages.base_page import BasePage
from src.pages.components.navbar import NavbarComponent


class LoginPage(BasePage):
    """Page object for Conduit Sign In page (/login)."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navbar = NavbarComponent(page)

        # Modern User-Facing Locators
        self.heading: Locator = page.get_by_role("heading", name="Sign in")
        self.email_input: Locator = page.get_by_placeholder("Email")
        self.password_input: Locator = page.get_by_placeholder("Password")
        self.submit_button: Locator = page.get_by_role("button", name="Sign in")
        self.error_messages: Locator = page.locator(".error-messages li")

    def load(self) -> "LoginPage":
        """Navigates to the login page."""
        self.navigate_to("/login")
        expect(self.heading).to_be_visible()
        return self

    def login(self, email: str, password: str) -> None:
        """Fills and submits credentials."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def get_error_messages(self) -> list[str]:
        """Returns error messages displayed on invalid login attempts."""
        self.error_messages.first.wait_for(state="visible")
        return self.error_messages.all_text_contents()