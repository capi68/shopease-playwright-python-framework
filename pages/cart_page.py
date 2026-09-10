

from pages.base_page import BasePage
from playwright.sync_api import Locator

class CartPage(BasePage):
    """Page Object for ShopEase cart page."""

    @property
    def url(self) -> str:
        """Return the cart page URL."""
        return "/cart"

    #-----------------
    #Cart Page
    #-----------------

    @property
    def cart_page_contain(self) -> Locator:
        """Return cart page contain locator."""
        return self.page.get_by_test_id("cart-page")


    @property
    def start_shopping_btn(self) -> Locator:
        """Return start shopping button locator."""
        return  self.page.get_by_test_id("continue-shopping")

    @property
    def cart_empty_container(self) -> Locator:
        """Return cart empty container locator."""
        return self.page.get_by_test_id("cart-empty")

    #----------------------
    #items contain
    #----------------------

    @property
    def items_container(self) -> Locator:
        """Return items container locator."""
        return self.page.get_by_test_id("cart-items")

    def cart_item(self, item_id: str) -> Locator:
        """Return cart item locator by item_id"""
        return self.page.get_by_test_id(f"cart-item-prod-{item_id}")

    def cart_item_image(self, item_id: str) -> Locator:
        """Return item image of specific item locator."""
        return self.cart_item(item_id).locator(".cart-item-image")

    def cart_item_name(self, item_id: str) -> Locator:
        """Return item name of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"cart-item-name-prod-{item_id}")

    def cart_item_price(self, item_id: str) -> Locator:
        """Return item price of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"cart-item-price-prod-{item_id}")

    def decrease_qty_item_btn(self, item_id: str) -> Locator:
        """Return decrease quantity button  of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"qty-dec-prod-{item_id}")

    def qty_value_item(self, item_id: str) -> Locator:
        """Return quantity value  of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"qty-val-prod-{item_id}")

    def increase_qty_item_btn(self, item_id: str) -> Locator:
        """Return increase quantity button  of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"qty-inc-prod-{item_id}")

    def subtotal_item(self, item_id: str) -> Locator:
        """Return subtotal of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"cart-item-subtotal-prod-{item_id}")

    def remove_item_btn(self, item_id: str) -> Locator:
        """Return remove item button  of specific item locator."""
        return self.cart_item(item_id).get_by_test_id(f"cart-remove-prod-{item_id}")

    #-------------------
    #cart summary
    #-------------------

    @property
    def cart_summary(self) -> Locator:
        """Return cart_summary locator."""
        return self.page.get_by_test_id("cart-summary")

    @property
    def cart_total_amount(self) -> Locator:
        """Return cart total amount locator."""
        return self.page.get_by_test_id("cart-total-amount")

    @property
    def clear_cart_btn(self) -> Locator:
        """Return clear cart button locator."""
        return self.page.get_by_test_id("clear-cart")

    @property
    def checkout_btn(self) -> Locator:
        """Return checkout button locator."""
        return self.page.get_by_test_id("checkout-button")






