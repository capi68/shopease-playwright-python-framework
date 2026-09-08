

from components.base_component import BaseComponent
from playwright.sync_api import Locator

class NavBarComponent(BaseComponent):
    """Component Object for ShopEase navbar."""

    @property
    def nav_bar(self) -> Locator:
        """Return NavBar locator."""
        return self.root

    @property
    def navbar_brand(self) -> Locator:
        """Return navbar brand locator."""
        return self.root.get_by_test_id("nav-brand")

    @property
    def search_input(self) -> Locator:
        """Return search input locator."""
        return self.root.get_by_test_id("search-input")

    @property
    def search_btn(self) -> Locator:
        """Return search button locator."""
        return self.root.get_by_test_id("search-submit")


    def navbar_links(self, link: str) -> Locator:
        """Return a navbar link locator for specific link."""
        return self.root.get_by_test_id(f"nav-{link.lower()}")


    def search_product(self, query: str) -> None:
        """Fill search input and click submit button."""
        self.search_input.fill(query)
        self.search_btn.click()
