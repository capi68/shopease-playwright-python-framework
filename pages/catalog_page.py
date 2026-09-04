

from pages.base_page import BasePage
from playwright.sync_api import Locator

class CatalogPage(BasePage):
    """Page Object for ShopEase catalog page."""

    @property
    def url(self) -> str:
        """Return the catalog page URL."""
        return "/catalog"

    #-----------------------------
    #NavBar
    #-----------------------------

    @property
    def nav_bar(self) -> Locator:
        """Return NavBar locator."""
        return self.page.get_by_test_id("navbar")

    @property
    def navbar_brand(self) -> Locator:
        """Return navbar brand locator."""
        return self.page.get_by_test_id("nav-brand")

    @property
    def search_input(self) -> Locator:
        """Return search input locator."""
        return self.page.get_by_test_id("search-input")

    @property
    def search_btn(self) -> Locator:
        """Return search button locator."""
        return self.page.get_by_test_id("search-submit")

    @property
    def catalog_link(self) -> Locator:
        """Return catalog link locator."""
        return self.page.get_by_test_id("nav-catalog")

    @property
    def cart_link(self) -> Locator:
        """Return cart link locator."""
        return self.page.get_by_test_id("nav-cart")

    @property
    def sign_in_link(self) -> Locator:
        """Return 'sign in' link locator."""
        return self.page.get_by_test_id("nav-login")


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


    #-----------------------------
    #Foot
    #-----------------------------

    @property
    def footer(self) -> Locator:
        """Return footer locator."""
        return self.page.get_by_test_id("store-footer")


    def footer_link(self, link_name: str) -> Locator:
        """Return contact us link locator."""
        return self.page.get_by_test_id(f"footer-{link_name.lower()}")

    @property
    def copyright(self) -> Locator:
        """Return copyright locator."""
        return self.page.get_by_test_id("footer-copyright")

    #-----------------------------
    #Methods
    #-----------------------------

    def search_product(self, query: str) -> None:
        """Fill search input and click submit button."""
        self.search_input.fill(query)
        self.search_btn.click()

    def apply_price_range(self, min_price: str, max_price: str) -> None:
        """Set price range filters."""
        self.filter_price_min.fill(min_price)
        self.filter_price_max.fill(max_price)








