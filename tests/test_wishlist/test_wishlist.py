"""Tests for Wishlist UI functionality and item management."""

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.wishlist_page import WishlistPage


@allure.epic("EPIC-02: Catalog & Search")
@allure.feature("Wishlist Module")
@pytest.mark.wishlist
class TestWishlist:
    """Test suite for Wishlist UI functionality and transfer to cart."""

    @pytest.mark.smoke
    @allure.story("Wishlist Management")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify adding a product to wishlist updates toggle button state and renders item")
    def test_add_product_to_wishlist_update_button_state_and_renders_item_in_wishlist_page(
            self,
            catalog_page: CatalogPage,
            wishlist_page: WishlistPage,
            first_product_id: str,
    ) -> None:
        """Verify that clicking wishlist button updates aria-label and renders product in wishlist page."""
        with allure.step("Verify initial wishlist button state and toggle action"):
            expect(catalog_page.wishlist_btn(first_product_id)).to_have_attribute(
                "aria-label", "Add to wishlist"
            )
            catalog_page.wishlist_btn(first_product_id).click()
            expect(catalog_page.wishlist_btn(first_product_id)).to_have_attribute(
                "aria-label", "Remove from wishlist"
            )

        with allure.step("Navigate to Wishlist page and verify item presence"):
            wishlist_page.navigate()
            expect(wishlist_page.wl_item_card(first_product_id)).to_be_visible()

    @pytest.mark.regression
    @allure.story("Wishlist Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify wishlist item renders correct product name and price matching catalog data")
    def test_add_product_to_wishlist_renders_item_in_wishlist_page(
            self,
            catalog_page: CatalogPage,
            wishlist_page: WishlistPage,
            first_product_id: str,
    ) -> None:
        """Verify that clicking wishlist button correctly renders the product in the wishlist page."""
        catalog_page.wishlist_btn(first_product_id).click()
        catalog_product_name = catalog_page.product_name(first_product_id).inner_text()
        catalog_product_price = catalog_page.product_price(first_product_id).inner_text()

        wishlist_page.navigate()

        expect(wishlist_page.wl_item_card(first_product_id)).to_be_visible()
        expect(wishlist_page.wl_item_name(first_product_id)).to_have_text(catalog_product_name)
        expect(wishlist_page.wl_item_price(first_product_id)).to_have_text(catalog_product_price)

    @pytest.mark.regression
    @allure.story("Wishlist Transfer")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify moving item from wishlist transfers product directly to cart page")
    def test_move_product_to_cart_from_wl_transfer_item_correctly(
            self,
            catalog_page: CatalogPage,
            wishlist_page: WishlistPage,
            cart_page: CartPage,
            first_product_id: str,
    ) -> None:
        """Verify that clicking move to cart button in wishlist page successfully transfers item to cart."""
        catalog_page.wishlist_btn(first_product_id).click()
        catalog_product_name = catalog_page.product_name(first_product_id).inner_text()
        catalog_product_price = catalog_page.product_price(first_product_id).inner_text()

        wishlist_page.navigate()

        # Move item to cart
        wishlist_page.move_to_cart_btn(first_product_id).click()
        expect(wishlist_page.wl_item_card(first_product_id)).not_to_be_visible()

        # Navigate to cart page
        cart_page.navigate()
        expect(cart_page.cart_item(first_product_id)).to_be_visible()
        expect(cart_page.cart_item_name(first_product_id)).to_have_text(catalog_product_name)
        expect(cart_page.cart_item_price(first_product_id)).to_have_text(catalog_product_price)

    @pytest.mark.regression
    @allure.story("Wishlist Removal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify removing item directly from wishlist page updates grid and displays empty state")
    def test_remove_product_from_wl_page_updates_list_and_shows_empty_state(
            self,
            catalog_page: CatalogPage,
            wishlist_page: WishlistPage,
            first_product_id: str,
    ) -> None:
        """Verify that removing an item from wishlist page deletes card and triggers empty container."""
        catalog_page.wishlist_btn(first_product_id).click()

        wishlist_page.navigate()

        wishlist_page.remove_item_btn(first_product_id).click()
        expect(wishlist_page.wl_item_card(first_product_id)).not_to_be_visible()
        expect(wishlist_page.empty_grid).to_be_visible()

    @pytest.mark.regression
    @allure.story("Empty Wishlist State")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Verify 'Browse products' button in empty wishlist redirects to catalog page")
    def test_browse_button_redirect_to_catalog_page(
            self, wishlist_page: WishlistPage
    ) -> None:
        """Verify that clicking the 'browse products' button redirects to catalog page."""
        wishlist_page.navigate()

        wishlist_page.browse_products_btn.click()
        expect(wishlist_page.page).to_have_url("/catalog")