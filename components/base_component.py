"""
Base component for reusable UI patterns.

All components receive a root_locator that scopes their selectors.
This prevents accidentally interacting with elements outside the component.
"""

from playwright.sync_api import Locator, Page

class BaseComponent:
    """Base class for reusable UI components."""

    def __init__(self, page: Page, root_locator: Locator):
        """
        Args:
            page: The Playwright page instance
            root_locator: The root element that contains this component
        """

        self.page = page
        self.root = root_locator

    def is_visible(self) -> bool:
        """Check if the component root is visible."""
        return self.root.is_visible()

