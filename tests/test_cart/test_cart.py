from enum import nonmember
from itertools import product

import allure
import pytest

from playwright.sync_api import expect, Page

from components.navbar import NavBarComponent
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage

@pytest.mark.cart
class TestCart:
    """Test for Cart UI."""

    def test_empty_cart(
            self,
            navbar: NavBarComponent,
            catalog_page: CatalogPage,
            cart_page: CartPage) -> None:
        """Verify that cart empty shows correctly."""

        catalog_page.navigate()

        navbar.navbar_links("cart").click()
        expect(cart_page.page).to_have_url("/cart")
        expect(cart_page.start_shopping_btn).to_be_visible()


    def test_add_product_to_cart(self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that click in 'add to cart' button, the product appears in cart page."""

        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first

        #extract product_id and click in 'add-to-cart'
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()
        catalog_page.add_to_card_btn(product_id).click()

        #navigate to cart
        cart_page.navigate()
        expect(cart_page.page).to_have_url("/cart")

        expect(cart_page.cart_item(product_id)).to_be_visible()


    def test_cart_item_renders_all_product_information(self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that adding a product to the cart correctly renders all
        its properties and interactive controls in cart page."""

        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first

        #extract properties by product_id  and click in 'add-to-cart'
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()
        product_name = catalog_page.product_name(product_id).inner_text()
        product_price = catalog_page.product_price(product_id).inner_text()
        catalog_page.add_to_card_btn(product_id).click()

        #navigate to cart
        cart_page.navigate()

        expect(cart_page.cart_item(product_id)).to_be_visible()
        expect(cart_page.cart_item_image(product_id)).to_be_visible()
        expect(cart_page.cart_item_name(product_id)).to_have_text(product_name)
        expect(cart_page.cart_item_price(product_id)).to_have_text(product_price)

        #Controls
        expect(cart_page.decrease_qty_item_btn(product_id)).to_be_visible()
        expect(cart_page.increase_qty_item_btn(product_id)).to_be_visible()
        expect(cart_page.qty_value_item(product_id)).to_have_text("1")
        expect(cart_page.subtotal_item(product_id)).to_be_visible()
        expect(cart_page.remove_item_btn(product_id)).to_be_visible()

        #Summary
        expect(cart_page.cart_total_amount).to_be_visible()
        expect(cart_page.clear_cart_btn).to_be_visible()
        expect(cart_page.checkout_btn).to_be_visible()



    def test_cart_item_qty_controls_update_totals_correctly(
            self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that incrementing and decrementing product quantity via cart controls
        correctly updates the item count, subtotal, and order total amount."""
        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first

        #extract properties by product_id  and click in 'add-to-cart'
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()
        product_price_raw = catalog_page.product_price(product_id).inner_text()
        product_price = float(product_price_raw.replace("$", "").strip())
        catalog_page.add_to_card_btn(product_id).click()

        #Navigate to cart
        cart_page.navigate()

        expect(cart_page.qty_value_item(product_id)).to_have_text("1")

        #Increment unit of product
        cart_page.increase_qty_item_btn(product_id).click()
        expect(cart_page.qty_value_item(product_id)).to_have_text("2")
        expect(cart_page.subtotal_item(product_id)).to_have_text(f"${(product_price * 2):0.2f}")
        expect(cart_page.cart_total_amount).to_have_text(f"${(product_price * 2):0.2f}")

        #Decrement unit of product
        cart_page.decrease_qty_item_btn(product_id).click()
        expect(cart_page.qty_value_item(product_id)).to_have_text("1")
        expect(cart_page.subtotal_item(product_id)).to_have_text(f"${product_price}")
        expect(cart_page.cart_total_amount).to_have_text(f"${product_price}")



    def test_remove_item_from_cart_updates_list_and_totals(
            self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that clicking the remove button on a cart item,
        deletes it from the order list and correctly updates the cart totals"""
        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first

        #extract properties by product_id  and click in 'add-to-cart'
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()
        product_price_raw = catalog_page.product_price(product_id).inner_text()
        product_price = float(product_price_raw.replace("$", "").strip())
        catalog_page.add_to_card_btn(product_id).click()

        #Navigate to cart
        cart_page.navigate()

        expect(cart_page.cart_total_amount).to_have_text(f"${product_price:0.2f}")

        #Delete item cart
        cart_page.remove_item_btn(product_id).click()
        expect(cart_page.cart_item(product_id)).not_to_be_visible()
        expect(cart_page.cart_empty_container).to_be_visible()



    def test_clear_cart_btn_removes_all_items(
            self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that clicking clear cart button, removes all products
        from the cart and displays the empty car state."""
        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first

        #extract properties by product_id  and click in 'add-to-cart'
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()
        catalog_page.add_to_card_btn(product_id).click()

        #Navigate to cart
        cart_page.navigate()
        expect(cart_page.cart_item(product_id)).to_be_visible()

        #Clear cart
        cart_page.clear_cart_btn.click()
        expect(cart_page.cart_empty_container).to_be_visible()


    def test_proceed_to_checkout_redirects_correctly(
            self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that clicking the proceed to checkout button
        redirects to the checkout page."""
        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first

        #extract properties by product_id  and click in 'add-to-cart'
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()
        catalog_page.add_to_card_btn(product_id).click()

        #Navigate to cart
        cart_page.navigate()
        expect(cart_page.cart_item(product_id)).to_be_visible()

        #Checkout
        cart_page.checkout_btn.click()
        expect(cart_page.page).to_have_url("/checkout")


    def test_removing_one_item_from_multiple_keeps_remaining_and_updates_totals(
            self, catalog_page: CatalogPage, cart_page: CartPage) -> None:
        """Verify that when multiple items are in the cart, removing one item
        deletes only that specific product and correctly updates the order total."""
        catalog_page.navigate()

        #Select first product in catalog
        first_card = catalog_page.all_product_cards.first
        second_card = catalog_page.all_product_cards.nth(1)

        #extract properties by product_id (1) and click in 'add-to-cart'
        att_card_1 = first_card.get_attribute("data-testid")
        product_id_1 = att_card_1.replace("product-card-prod-", "").strip()
        product_price_raw_1 = catalog_page.product_price(product_id_1).inner_text()
        product_price_1 = float(product_price_raw_1.replace("$", "").strip())
        catalog_page.add_to_card_btn(product_id_1).click()

        #extract properties by product_id (2) and click in 'add-to-cart'
        att_card_2 = second_card.get_attribute("data-testid")
        product_id_2 = att_card_2.replace("product-card-prod-", "").strip()
        product_price_raw_2 = catalog_page.product_price(product_id_2).inner_text()
        product_price_2 = float(product_price_raw_2.replace("$", "").strip())
        catalog_page.add_to_card_btn(product_id_2).click()

        #Navigate to cart
        cart_page.navigate()
        expect(cart_page.cart_item(product_id_1)).to_be_visible()
        expect(cart_page.cart_item(product_id_2)).to_be_visible()
        expect(cart_page.cart_total_amount).to_have_text(f"${(product_price_1 + product_price_2):0.2f}")

        #delete product 1
        cart_page.remove_item_btn(product_id_1).click()
        expect(cart_page.cart_item(product_id_1)).not_to_be_visible()
        expect(cart_page.cart_total_amount).to_have_text(f"${product_price_2:0.2f}")