"""
Base page object for the Shop Ease test framework.

All page objects inherit from this class. It provides shared
navigation, wait helpers, and screenshot utilities.
"""
from typing import Optional
from playwright.sync_api import Page, Locator, Response, expect

class BasePage:
    """Base page object providing shared functionality for all pages."""

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def url(self) -> str:
        """Override in subclasses to define the page URL path."""
        raise NotImplementedError("Subclasses must define 'url' property")

    def navigate(self) -> Optional[Response]:
        """Navigate to this page's URL and wait for DOM content to load."""
        response = self.page.goto(self.url)
        self.wait_for_page_load()
        return response

    def navigate_to(self, path: str) -> Optional[Response]:
        """Navigate to an explicit relative path or absolute URL."""
        return self.page.goto(path)

    def wait_for_page_load(self) -> None:
        """Wait for the page to reach domcontentloaded state."""
        self.page.wait_for_load_state("domcontentloaded")

    def get_element(self, selector: str) -> Locator:
        """Return a playwright locator from css selector or xPath."""
        return self.page.locator(selector)

    def wait_for_url_contains(self, partial_url: str, timeout: float = 5000) -> None:
        """Wait for the current URL to contain a specific substring."""
        expect(self.page).to_have_url(f".*{partial_url}.*", timeout=timeout)

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url

    def get_page_title(self) -> str:
        """Return actual page Title."""
        return self.page.title()

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")