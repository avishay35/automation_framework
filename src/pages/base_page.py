from playwright.sync_api import Page, Response, expect
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class providing shared functionality across all Page Objects."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, path: str = "/") -> Response | None:
        """Navigates to a relative path off the base_url configured in context."""
        logger.info(f"Navigating to path: '{path}'")
        return self.page.goto(path)

    def get_current_url(self) -> str:
        """Returns the current browser URL."""
        return self.page.url

    def wait_for_url_contains(self, url_substring: str, timeout_ms: int = 5000) -> None:
        """Waits until current URL contains a specific substring."""
        self.page.wait_for_url(f"**/*{url_substring}*", timeout=timeout_ms)

    def assert_toast_message(self, expected_message: str) -> None:
        """Asserts error or notification toast presence (common in modern SPAs)."""
        toast = self.page.get_by_text(expected_message)
        expect(toast).to_be_visible()