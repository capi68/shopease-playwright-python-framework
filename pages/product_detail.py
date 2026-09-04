

from pages.base_page import BasePage
from playwright.sync_api import Locator

class ProductDetailPage(BasePage):
    """Page Object for ShopEase product detail page."""

    @property
    def url(self) -> str:
        """Return base URL path for product detail."""
        return "/product"

    def navigate_to_product(self, product_id: int | str) -> None:
        """Navigate directly to a specific product detail page."""
        self.page.goto(f"{self.url}/prod-{product_id}")

    #---------------------------
    #breadcrumb
    #---------------------------

    def breadcrumb_link(self, text: str) -> Locator:
        """Return a breadcrumb link locator by its visible text (e.g. 'Catalog', 'electronics')."""
        return self.page.get_by_test_id("breadcrumb").get_by_role("link", name=text, exact=False)

    #---------------------------
    #product detail
    #---------------------------

    @property
    def detail_image(self) -> Locator:
        """Return Image detail locator."""
        return self.page.get_by_test_id("detail-image")

    @property
    def detail_name(self) -> Locator:
        """Return Name detail locator."""
        return self.page.get_by_test_id("detail-name")

    @property
    def detail_rating(self) -> Locator:
        """Return rating detail locator."""
        return self.page.get_by_test_id("detail-rating")

    @property
    def detail_price(self) -> Locator:
        """Return price detail locator."""
        return self.page.get_by_test_id("detail-price")

    @property
    def detail_stock(self) -> Locator:
        """Return stock detail locator."""
        return self.page.get_by_test_id("detail-stock")

    @property
    def quantity_control(self) -> Locator:
        """Return quantity control locator."""
        return self.page.get_by_test_id("quantity-control")

    @property
    def qty_decrease_btn(self) -> Locator:
        """Return quantity decrease button locator."""
        return self.page.get_by_test_id("qty-decrease")

    @property
    def qty_increase_btn(self) -> Locator:
        """Return quantity increase button locator."""
        return self.page.get_by_test_id("qty-increase")

    @property
    def qty_input(self) -> Locator:
        """Return quantity input locator."""
        return self.page.get_by_test_id("qty-input")

    @property
    def detail_add_to_cart_btn(self) -> Locator:
        """Return detail add to cart button locator."""
        return self.page.get_by_test_id("detail-add-to-cart")


    @property
    def description_btn(self) -> Locator:
        """Return tab description button locator."""
        return self.page.get_by_test_id("tab-description")

    @property
    def specs_btn(self) -> Locator:
        """Return tab specifications button locator."""
        return self.page.get_by_test_id("tab-specs")

    @property
    def panel_description(self) -> Locator:
        """Return panel description locator."""
        return self.page.get_by_test_id("panel-description")

    @property
    def panel_specs(self) -> Locator:
        """Return panel specifications locator."""
        return self.page.get_by_test_id("panel-specs")

    #-------------------------
    #Methods
    #-------------------------

    def set_quantity(self, qty: int) -> None:
        """Fill quantity input directly."""
        self.qty_input.fill(str(qty))

    def add_to_cart(self) -> None:
        """Click the add to cart button."""
        self.detail_add_to_cart_btn.click()
