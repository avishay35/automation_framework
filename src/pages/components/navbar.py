from playwright.sync_api import Page, Locator


class NavbarComponent:
    """Reusable Navigation Bar component present across Conduit SPA pages."""

    def __init__(self, page: Page) -> None:
        self.page = page
        
        # Locators using accessible user-facing attributes
        self.brand_link: Locator = page.get_by_role("link", name="conduit", exact=True)
        self.home_link: Locator = page.get_by_role("link", name="Home")
        self.sign_in_link: Locator = page.get_by_role("link", name="Sign in")
        self.sign_up_link: Locator = page.get_by_role("link", name="Sign up")
        self.new_article_link: Locator = page.get_by_role("link", name="New Article")
        self.settings_link: Locator = page.get_by_role("link", name="Settings")

    def click_sign_in(self) -> None:
        self.sign_in_link.click()

    def click_sign_up(self) -> None:
        self.sign_up_link.click()

    def click_new_article(self) -> None:
        self.new_article_link.click()

    def get_user_profile_link(self, username: str) -> Locator:
        return self.page.get_by_role("link", name=username)