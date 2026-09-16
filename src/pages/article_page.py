from playwright.sync_api import Page, Locator
from src.pages.base_page import BasePage
#from src.pages.components.navbar import NavbarComponent
from playwright.sync_api import expect


class ArticlePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators defined directly on the page component
        self.title_heading: Locator = page.get_by_role("heading", level=1)
        self.body_text: Locator = page.locator("p")
        self.publish_button: Locator = page.get_by_role("button", name="Publish Article")
        self.body_input: Locator = page.get_by_placeholder("Write your article")

    def publish_article(self, body: str):
        self.body_input.fill(body)
        self.publish_button.click()