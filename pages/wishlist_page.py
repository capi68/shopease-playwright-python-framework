

from pages.base_page import BasePage
from playwright.sync_api import Locator

class WishlistPage(BasePage):
    """Page Object for ShpEase wishlist page."""

    @property
    def url(self) -> str:
        """Return the wishlist page URL."""
        return "/wishlist"

    @property
    def wishlist_container(self) -> Locator:
        """Return the wishlist container locator"""
        return self.page.get_by_test_id("wishlist-page")
    
    @property
    def wishlist_grid(self) -> Locator:
        """Return the wishlist grid locator."""
        return self.page.get_by_test_id("wishlist-grid")

    def wl_item_card(self, item_id: str) -> Locator:
        """Return the wishlist item card by item_id locator."""
        return self.page.get_by_test_id(f"wishlist-item-prod-{item_id}")

    def wl_item_image(self, item_id: str) -> Locator:
        """Return wishlist item image of a specific item_id locator."""
        return self.wl_item_card(item_id).locator(".wishlist-image")

    def wl_item_name(self, item_id: str) -> Locator:
        """Return wishlist item name of a specific item_id locator."""
        return self.wl_item_card(item_id).get_by_test_id(f"wishlist-name-prod-{item_id}")

    def wl_item_price(self, item_id: str) -> Locator:
        """Return wishlist item price of a specific item_id locator."""
        return self.wl_item_card(item_id).get_by_test_id(f"wishlist-price-prod-{item_id}")

    def move_to_cart_btn(self, item_id: str) -> Locator:
        """Return move to cart item button locator."""
        return self.wl_item_card(item_id).get_by_test_id(f"wishlist-to-cart-prod-{item_id}")

    def remove_item_btn(self, item_id: str) -> Locator:
        """Return remove item button locator."""
        return self.wl_item_card(item_id).get_by_test_id(f"wishlist-remove-prod-{item_id}")

    @property
    def empty_grid(self) -> Locator:
        """Return empty wishlist locator."""
        return self.page.get_by_test_id("wishlist-empty")

    @property
    def browse_products_btn(self) -> Locator:
        """Return browse products button locator."""
        return self.page.get_by_test_id("browse-products")




    