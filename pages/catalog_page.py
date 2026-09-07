

from pages.base_page import BasePage
from playwright.sync_api import Locator

class CatalogPage(BasePage):
    """Page Object for ShopEase catalog page."""

    @property
    def url(self) -> str:
        """Return the catalog page URL."""
        return "/catalog"


    #-----------------------------
    #Catalog Page
    #-----------------------------

    @property
    def results_count(self) -> Locator:
        """Return results count locator."""
        return self.page.get_by_test_id("results-count")

    @property
    def product_grid(self) -> Locator:
        """Return products grid locator."""
        return self.page.get_by_test_id("product-grid")

    def card_product(self, product_id: int) -> Locator:
        """Return product card locator by product_id"""
        return self.page.get_by_test_id(f"product-card-prod-{product_id}")

    #-----------------------------
    #Filters section
    #-----------------------------

    @property
    def catalog_filter(self) -> Locator:
        """Return catalog filter locator."""
        return self.page.get_by_test_id("catalog-filters")


    def filter_category(self, category: str) -> Locator:
        """Return category filter locator by category."""
        return self.page.get_by_test_id(f"filter-category-{category.lower()}")

    @property
    def filter_price_min(self) -> Locator:
        """Return filter min price locator."""
        return self.page.get_by_test_id("filter-price-min")

    @property
    def filter_price_max(self) -> Locator:
        """Return filter max price locator."""
        return self.page.get_by_test_id("filter-price-max")

    @property
    def filter_sort(self) -> Locator:
        """Return sort filter locator."""
        return self.page.get_by_test_id("filter-sort")


    def apply_price_range(self, min_price: str, max_price: str) -> None:
        """Set price range filters."""
        self.filter_price_min.fill(min_price)
        self.filter_price_max.fill(max_price)








