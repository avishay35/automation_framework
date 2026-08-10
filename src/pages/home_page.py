from playwright.sync_api import Page, Locator, expect
from src.pages.base_page import BasePage
from src.pages.components.navbar import NavbarComponent


class HomePage(BasePage):
    """Page object for Conduit Home Page / Feed (/)." """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navbar = NavbarComponent(page)

        # Locators
        self.banner_title: Locator = page.get_by_role("heading", name="conduit")
        self.global_feed_tab: Locator = page.get_by_role("button", name="Global Feed")
        self.your_feed_tab: Locator = page.get_by_role("button", name="Your Feed")
        self.article_preview: Locator = page.locator(".article-preview")
        self.popular_tags: Locator = page.locator(".sidebar .tag-list a")

    def load(self) -> "HomePage":
        """Navigates to home page."""
        self.navigate_to("/")
        return self

    def select_global_feed(self) -> "HomePage":
        """Switches tab to Global Feed."""
        self.global_feed_tab.click()
        return self

    def get_article_titles(self) -> list[str]:
        """Fetches all visible article titles on current feed."""
        expect(self.article_preview.first).to_be_visible()
        headings = self.page.locator(".article-preview h1")
        return headings.all_text_contents()