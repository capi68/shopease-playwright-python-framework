
import allure
import pytest

from playwright.sync_api import expect

from conftest import first_product_id, cart_page, catalog_page
from pages.cart_page import CartPage
from pages.wishlist_page import WishlistPage
from pages.catalog_page import CatalogPage

@pytest.mark.wishlist
class TestWishlist:
    """Tests for Wishlist UI."""


    def test_add_product_to_wishlist_update_button_state_and_renders_item_in_wishlist_page(
            self,
            catalog_page: CatalogPage,
            wishlist_page: WishlistPage,
            first_product_id: str) -> None:
        """Verify that clicking wishlist button updates its aria-label to active state
        and correctly renders the product in the wishlist page."""

        #add to wishlist and aria-label updates
        expect(catalog_page.wishlist_btn(first_product_id)).to_have_attribute("aria-label","Add to wishlist")
        catalog_page.wishlist_btn(first_product_id).click()
        expect(catalog_page.wishlist_btn(first_product_id)).to_have_attribute("aria-label", "Remove from wishlist")

        #navigate to wishlist page
        wishlist_page.navigate()

        #Verify that product is in wishlist page
        expect(wishlist_page.wl_item_card(first_product_id)).to_be_visible()


    def test_add_product_to_wishlist_renders_item_in_wishlist_page(
            self,catalog_page: CatalogPage,wishlist_page: WishlistPage, first_product_id: str) -> None:
        """Verify that clicking wishlist button correctly renders the product in the wishlist page."""

        #add first product to wishlist and extract other properties
        catalog_page.wishlist_btn(first_product_id).click()
        catalog_product_name = catalog_page.product_name(first_product_id).inner_text()
        catalog_product_price = catalog_page.product_price(first_product_id).inner_text()

        #navigate to wishlist page
        wishlist_page.navigate()

        expect(wishlist_page.wl_item_card(first_product_id)).to_be_visible()
        expect(wishlist_page.wl_item_name(first_product_id)).to_have_text(catalog_product_name)
        expect(wishlist_page.wl_item_price(first_product_id)).to_have_text(catalog_product_price)


    def test_move_product_to_cart_from_wl_transfer_item_correctly(
            self,catalog_page: CatalogPage, wishlist_page: WishlistPage, cart_page: CartPage, first_product_id: str) -> None:
        """Verify that clicking the move to cart button inside the wishlist page successfully
        adds the product to the cart page"""

        #add first product to wishlist and extract other properties
        catalog_page.wishlist_btn(first_product_id).click()
        catalog_product_name = catalog_page.product_name(first_product_id).inner_text()
        catalog_product_price = catalog_page.product_price(first_product_id).inner_text()

        #navigate to wishlist page
        wishlist_page.navigate()

        #Move item to cart
        wishlist_page.move_to_cart_btn(first_product_id).click()
        expect(wishlist_page.wl_item_card(first_product_id)).not_to_be_visible()

        #Navigate to cart page
        cart_page.navigate()
        expect(cart_page.cart_item(first_product_id)).to_be_visible()
        expect(cart_page.cart_item_name(first_product_id)).to_have_text(catalog_product_name)
        expect(cart_page.cart_item_price(first_product_id)).to_have_text(catalog_product_price)


    def test_remove_product_from_wl_page_updates_list_and_shows_empty_state(
            self, catalog_page: CatalogPage, wishlist_page: WishlistPage, first_product_id: str) -> None:
        """Verify that removing an item directly from the wishlist page
        deletes the product card and triggers the empty wishlist container."""

        #add first product to wishlist and extract other properties
        catalog_page.wishlist_btn(first_product_id).click()

        #navigate to wishlist page
        wishlist_page.navigate()

        #Remove item from wishlist
        wishlist_page.remove_item_btn(first_product_id).click()
        expect(wishlist_page.wl_item_card(first_product_id)).not_to_be_visible()
        expect(wishlist_page.empty_grid).to_be_visible()


    def test_browse_button_redirect_to_catalog_page(self, wishlist_page: WishlistPage):
        """Verify that clicking the 'browse products' button, redirect to catalog page."""
        #navigate to wishlist page
        wishlist_page.navigate()

        #click browse products button
        wishlist_page.browse_products_btn.click()
        expect(wishlist_page.page).to_have_url("/catalog")