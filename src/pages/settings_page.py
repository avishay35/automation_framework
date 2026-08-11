from playwright.sync_api import Page, Locator, expect
from src.pages.base_page import BasePage
from src.pages.components.navbar import NavbarComponent


class SettingsPage(BasePage):
    """Page Object for Conduit Settings Page (/settings)."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navbar = NavbarComponent(page)

        # Locators
        self.heading: Locator = page.get_by_role("heading", name="Your Settings")
        self.username_input: Locator = page.get_by_placeholder("Your Name")
        self.bio_input: Locator = page.get_by_placeholder("Short bio about you")
        self.email_input: Locator = page.get_by_placeholder("Email")
        self.logout_button: Locator = page.get_by_role("button", name="Or click here to logout")

    def load(self) -> "SettingsPage":
        """Navigates to /settings."""
        self.navigate_to("/settings")
        expect(self.heading).to_be_visible()
        return self

    def logout(self) -> None:
        """Clicks the logout button."""
        self.logout_button.click()