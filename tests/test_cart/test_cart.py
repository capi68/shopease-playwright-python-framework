"""Tests for Cart UI functionality and item management."""

import allure
import pytest
from playwright.sync_api import expect

from components.navbar import NavBarComponent
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage


@allure.epic("EPIC-03: Cart Management")
@allure.feature("Cart Module")
@pytest.mark.cart
class TestCart:
    """Test suite for Cart UI functionality, quantity controls, and totals."""

    @pytest.mark.regression
    @allure.story("Empty Cart State")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify empty cart page displays empty state container and start shopping button")
    def test_empty_cart(
            self, navbar: NavBarComponent, catalog_page: CatalogPage, cart_page: CartPage
    ) -> None:
        """Verify that empty cart shows correctly."""
        catalog_page.navigate()

        navbar.navbar_links("cart").click()
        expect(cart_page.page).to_have_url("/cart")
        expect(cart_page.start_shopping_btn).to_be_visible()

    @pytest.mark.smoke
    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify adding a product from catalog reflects item in cart page")
    def test_add_product_to_cart(
            self, catalog_page: CatalogPage, cart_page: CartPage
    ) -> None:
        """Verify that clicking 'add to cart' button displays product in cart page."""
        with allure.step("Navigate to catalog and select first product"):
            catalog_page.navigate()
            first_card = catalog_page.all_product_cards.first
            att_card = first_card.get_attribute("data-testid")
            product_id = att_card.replace("product-card-prod-", "").strip()

        with allure.step("Click 'Add to Cart' button"):
            catalog_page.add_to_card_btn(product_id).click()

        with allure.step("Navigate to cart and verify item is displayed"):
            cart_page.navigate()
            expect(cart_page.page).to_have_url("/cart")
            expect(cart_page.cart_item(product_id)).to_be_visible()

    @pytest.mark.regression
    @allure.story("Cart Item Details")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify cart item renders correct properties, image, and interactive controls")
    def test_cart_item_renders_all_product_information(
            self, catalog_page: CatalogPage, cart_page: CartPage, first_product_id: str
    ) -> None:
        """Verify that adding a product to the cart correctly renders all its properties and interactive controls."""
        # Extract properties by product_id and click 'add-to-cart'
        product_name = catalog_page.product_name(first_product_id).inner_text()
        product_price = catalog_page.product_price(first_product_id).inner_text()
        catalog_page.add_to_card_btn(first_product_id).click()

        # Navigate to cart
        cart_page.navigate()

        expect(cart_page.cart_item(first_product_id)).to_be_visible()
        expect(cart_page.cart_item_image(first_product_id)).to_be_visible()
        expect(cart_page.cart_item_name(first_product_id)).to_have_text(product_name)
        expect(cart_page.cart_item_price(first_product_id)).to_have_text(product_price)

        # Controls
        expect(cart_page.decrease_qty_item_btn(first_product_id)).to_be_visible()
        expect(cart_page.increase_qty_item_btn(first_product_id)).to_be_visible()
        expect(cart_page.qty_value_item(first_product_id)).to_have_text("1")
        expect(cart_page.subtotal_item(first_product_id)).to_be_visible()
        expect(cart_page.remove_item_btn(first_product_id)).to_be_visible()

        # Summary
        expect(cart_page.cart_total_amount).to_be_visible()
        expect(cart_page.clear_cart_btn).to_be_visible()
        expect(cart_page.checkout_btn).to_be_visible()

    @pytest.mark.regression
    @allure.story("Cart Quantity & Calculations")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify quantity controls update item subtotal and total cart amount correctly")
    def test_cart_item_qty_controls_update_totals_correctly(
            self, catalog_page: CatalogPage, cart_page: CartPage, first_product_id: str
    ) -> None:
        """Verify that incrementing and decrementing product quantity updates item count, subtotal, and total amount."""
        product_price_raw = catalog_page.product_price(first_product_id).inner_text()
        product_price = float(product_price_raw.replace("$", "").strip())
        catalog_page.add_to_card_btn(first_product_id).click()

        cart_page.navigate()
        expect(cart_page.qty_value_item(first_product_id)).to_have_text("1")

        # Increment unit of product
        cart_page.increase_qty_item_btn(first_product_id).click()
        expect(cart_page.qty_value_item(first_product_id)).to_have_text("2")
        expect(cart_page.subtotal_item(first_product_id)).to_have_text(f"${(product_price * 2):0.2f}")
        expect(cart_page.cart_total_amount).to_have_text(f"${(product_price * 2):0.2f}")

        # Decrement unit of product
        cart_page.decrease_qty_item_btn(first_product_id).click()
        expect(cart_page.qty_value_item(first_product_id)).to_have_text("1")
        expect(cart_page.subtotal_item(first_product_id)).to_have_text(f"${product_price:.2f}")
        expect(cart_page.cart_total_amount).to_have_text(f"${product_price:.2f}")

    @pytest.mark.regression
    @allure.story("Item Removal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify removing single item deletes row and displays empty cart state")
    def test_remove_item_from_cart_updates_list_and_totals(
            self, catalog_page: CatalogPage, cart_page: CartPage, first_product_id: str
    ) -> None:
        """Verify that clicking remove button on a cart item deletes it and updates cart totals."""
        product_price_raw = catalog_page.product_price(first_product_id).inner_text()
        product_price = float(product_price_raw.replace("$", "").strip())
        catalog_page.add_to_card_btn(first_product_id).click()

        cart_page.navigate()
        expect(cart_page.cart_total_amount).to_have_text(f"${product_price:0.2f}")

        # Delete item cart
        cart_page.remove_item_btn(first_product_id).click()
        expect(cart_page.cart_item(first_product_id)).not_to_be_visible()
        expect(cart_page.cart_empty_container).to_be_visible()

    @pytest.mark.regression
    @allure.story("Item Removal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify 'Clear Cart' button removes all items and resets state")
    def test_clear_cart_btn_removes_all_items(
            self, catalog_page: CatalogPage, cart_page: CartPage, first_product_id: str
    ) -> None:
        """Verify that clicking clear cart button removes all products from cart."""
        catalog_page.add_to_card_btn(first_product_id).click()

        cart_page.navigate()
        expect(cart_page.cart_item(first_product_id)).to_be_visible()

        cart_page.clear_cart_btn.click()
        expect(cart_page.cart_empty_container).to_be_visible()

    @pytest.mark.regression
    @allure.story("Cart Checkout Navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify 'Proceed to Checkout' button redirects to checkout route")
    def test_proceed_to_checkout_redirects_correctly(
            self, catalog_page: CatalogPage, cart_page: CartPage, first_product_id: str
    ) -> None:
        """Verify that clicking proceed to checkout button redirects to checkout page."""
        catalog_page.add_to_card_btn(first_product_id).click()

        cart_page.navigate()
        expect(cart_page.cart_item(first_product_id)).to_be_visible()

        cart_page.checkout_btn.click()
        expect(cart_page.page).to_have_url("/checkout")

    @pytest.mark.regression
    @allure.story("Item Removal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify removing one item from multiple items keeps remaining product and recalculates total")
    def test_removing_one_item_from_multiple_keeps_remaining_and_updates_totals(
            self, catalog_page: CatalogPage, cart_page: CartPage, first_product_id: str
    ) -> None:
        """Verify that removing one item from multiple items deletes only that item and updates total."""
        second_card = catalog_page.all_product_cards.nth(1)

        product_price_raw_1 = catalog_page.product_price(first_product_id).inner_text()
        product_price_1 = float(product_price_raw_1.replace("$", "").strip())
        catalog_page.add_to_card_btn(first_product_id).click()

        att_card_2 = second_card.get_attribute("data-testid")
        product_id_2 = att_card_2.replace("product-card-prod-", "").strip()
        product_price_raw_2 = catalog_page.product_price(product_id_2).inner_text()
        product_price_2 = float(product_price_raw_2.replace("$", "").strip())
        catalog_page.add_to_card_btn(product_id_2).click()

        cart_page.navigate()
        expect(cart_page.cart_item(first_product_id)).to_be_visible()
        expect(cart_page.cart_item(product_id_2)).to_be_visible()
        expect(cart_page.cart_total_amount).to_have_text(f"${(product_price_1 + product_price_2):0.2f}")

        # Delete product 1
        cart_page.remove_item_btn(first_product_id).click()
        expect(cart_page.cart_item(first_product_id)).not_to_be_visible()
        expect(cart_page.cart_total_amount).to_have_text(f"${product_price_2:0.2f}")