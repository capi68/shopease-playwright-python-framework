

from pages.base_page import BasePage
from playwright.sync_api import Locator

class CatalogPage(BasePage):
    """Page Object for ShopEase catalog page."""

    @property
    def url(self) -> str:
        """Return the catalog page URL."""
        return "/catalog"

    @property
    def results_count(self) -> Locator:
        """Return results count locator."""
        return self.page.get_by_test_id("results-count")

    @property
    def product_grid(self) -> Locator:
        """Return products grid locator."""
        return self.page.get_by_test_id("product-grid")


    #-----------------------------
    #Cards
    #-----------------------------


    @property
    def all_product_cards(self) -> Locator:
        """Return locator for all product cards."""
        return self.page.locator("[data-testid^='product-card-prod-']")

    def card_product(self, product_id: int) -> Locator:
        """Return specific product card locator by product_id"""
        return self.page.get_by_test_id(f"product-card-prod-{product_id}")

    @property
    def product_price(self) -> Locator:
        """Return product price locator in the grid."""
        return self.page.locator('[data-testid^="product-price-prod-"]')

    @property
    def product_rating(self) -> Locator:
        """Return product rating locator in the grid."""
        return self.page.locator('[data-testid^="product-rating-prod-"]')

    @property
    def product_name(self) -> Locator:
        """Return product name locator in the grid."""
        return self.page.locator('[data-testid^="product-name-prod-"]')

    def wishlist_btn(self, product_id: int) -> Locator:
        """Return the add to wishlist button for specific product by product_id."""
        return self.page.get_by_test_id(f"wishlist-btn-prod-{product_id}")

    def add_to_card_btn(self, product_id: int) -> Locator:
        """Return add to cart button for specific product by product_id."""
        return self.page.get_by_test_id(f"add-to-cart-prod-{product_id}")

    @property
    def empty_catalog(self) -> Locator:
        """Return empty catalog locator."""
        return self.page.get_by_test_id("empty-catalog")

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








