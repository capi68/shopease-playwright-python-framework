"""Tests for Checkout UI functionality and Order placement flow."""

import allure
import pytest
from playwright.sync_api import expect

from components.footer import FooterComponent
from components.navbar import NavBarComponent
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.orders_page import OrdersPage


@allure.epic("EPIC-04: Checkout Module")
@allure.feature("Checkout & Order Placement")
@pytest.mark.checkout
class TestCheckout:
    """Test suite for Checkout UI wizard steps and final order creation."""

    @pytest.mark.regression
    @allure.story("Shipping Step")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify initial display of checkout page and shipping form fields")
    def test_checkout_page_correctly_display(
            self,
            checkout_page: CheckoutPage,
            catalog_page: CatalogPage,
            cart_page: CartPage,
            navbar: NavBarComponent,
            footer: FooterComponent,
            first_product_id: str,
    ) -> None:
        """Verify that checkout page displays correctly."""
        catalog_page.add_to_card_btn(first_product_id).click()

        # Navigate to cart and proceed to checkout
        cart_page.navigate()
        cart_page.checkout_btn.click()

        expect(cart_page.page).to_have_url("/checkout")
        expect(checkout_page.shipping_step).to_have_attribute("class", "step active")
        expect(checkout_page.shipping_name).to_be_visible()
        expect(checkout_page.shipping_address).to_be_visible()
        expect(checkout_page.shipping_city).to_be_visible()
        expect(checkout_page.shipping_zip).to_be_visible()
        expect(checkout_page.shipping_country).to_be_visible()
        expect(checkout_page.shipping_phone).to_be_visible()
        expect(checkout_page.continue_to_payment_btn).to_be_visible()
        expect(navbar.nav_bar).to_be_visible()
        expect(footer.footer).to_be_visible()

    @pytest.mark.regression
    @allure.story("Shipping Step")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify validation error messages appear for empty required shipping fields")
    def test_shipping_form_shows_errors_on_empty_submit(
            self, order_ready_to_checkout: CheckoutPage
    ) -> None:
        """Verify validation error messages appear for all required fields when submitting empty shipping form."""
        order_ready_to_checkout.continue_to_payment_btn.click()

        required_fields = ["name", "address", "city", "zip", "phone"]

        for field in required_fields:
            expect(order_ready_to_checkout.field_error_message(field)).to_be_visible()

    @pytest.mark.regression
    @allure.story("Shipping Step")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify filling required shipping fields advances user to payment step")
    def test_fill_shipping_required_fields_and_continue_to_payment(
            self, order_ready_to_checkout: CheckoutPage
    ) -> None:
        """Verify that correctly filling shipping fields proceeds to payment."""
        order_ready_to_checkout.shipping_name.fill("Peter Parker")
        order_ready_to_checkout.shipping_address.fill("#20 Ingram Street")
        order_ready_to_checkout.shipping_city.fill("Queens")
        order_ready_to_checkout.shipping_zip.fill("11101")
        order_ready_to_checkout.shipping_country.select_option("US")
        order_ready_to_checkout.shipping_phone.fill("+19876543210")
        order_ready_to_checkout.continue_to_payment_btn.click()

        expect(order_ready_to_checkout.payment_form).to_be_visible()

    @pytest.mark.regression
    @allure.story("Payment Step")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify correct display of payment form fields and step indicator")
    def test_payment_form_correctly_display(
            self, shipping_to_payment_order: CheckoutPage
    ) -> None:
        """Verify the correct display of payment form."""
        expect(shipping_to_payment_order.shipping_step).to_have_attribute("class", "step active")
        expect(shipping_to_payment_order.payment_step).to_have_attribute("class", "step active")
        expect(shipping_to_payment_order.name_on_card).to_be_visible()
        expect(shipping_to_payment_order.number_card).to_be_visible()
        expect(shipping_to_payment_order.card_expiry).to_be_visible()
        expect(shipping_to_payment_order.card_cvv).to_be_visible()
        expect(shipping_to_payment_order.back_btn).to_be_visible()
        expect(shipping_to_payment_order.review_order_btn).to_be_visible()

    @pytest.mark.regression
    @allure.story("Payment Step")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify validation error messages appear for empty required payment fields")
    def test_payment_form_shows_errors_on_empty_submit(
            self, shipping_to_payment_order: CheckoutPage
    ) -> None:
        """Verify validation error messages appear for all required fields when submitting empty payment form."""
        shipping_to_payment_order.review_order_btn.click()

        required_fields = ["name", "number", "expiry", "cvv"]

        for field in required_fields:
            expect(shipping_to_payment_order.error_card_alerts(field)).to_be_visible()

    @pytest.mark.regression
    @allure.story("Payment Step")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify filling required payment fields advances user to review section")
    def test_fill_payment_required_fields_and_continue_to_review(
            self, shipping_to_payment_order: CheckoutPage
    ) -> None:
        """Verify that correctly filling payment fields proceeds to review."""
        shipping_to_payment_order.name_on_card.fill("Peter Parker")
        shipping_to_payment_order.number_card.fill("4009 1753 3280 6176")
        shipping_to_payment_order.card_expiry.fill("02/29")
        shipping_to_payment_order.card_cvv.fill("123")
        shipping_to_payment_order.review_order_btn.click()

        expect(shipping_to_payment_order.review_section).to_be_visible()

    @pytest.mark.regression
    @allure.story("Review Step")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify order review section displays accurate item, price, and shipping details")
    def test_review_section_display_correctly(
            self, payment_to_review_order: CheckoutPage
    ) -> None:
        """Verify the correct display of review section."""
        product_id = payment_to_review_order.product_id
        shipping_info = payment_to_review_order.shipping_data
        product_price = payment_to_review_order.product_price

        # Verify product by product_id
        expect(payment_to_review_order.review_item(product_id)).to_be_visible()
        expect(payment_to_review_order.review_item(product_id)).to_contain_text(product_price)

        # Verify shipping_info
        shipping_container = payment_to_review_order.review_shipping
        expect(shipping_container).to_contain_text(shipping_info["name"])
        expect(shipping_container).to_contain_text(shipping_info["address"])
        expect(shipping_container).to_contain_text(shipping_info["city"])
        expect(shipping_container).to_contain_text(shipping_info["zip"])
        expect(shipping_container).to_contain_text(shipping_info["country"])

        # Verify total
        expect(payment_to_review_order.review_total).to_contain_text(product_price)

    @pytest.mark.smoke
    @allure.story("Order Completion")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify placing an order completes transaction and creates valid order in history")
    def test_place_order_creates_order_successfully(
            self, review_to_orders_page: OrdersPage
    ) -> None:
        """Verify that placing an order redirects to OrdersPage and displays valid order details."""
        orders = review_to_orders_page
        product_price = review_to_orders_page.product_price

        with allure.step("Verify redirection to Orders page and container visibility"):
            expect(orders.order_list).to_be_visible()
            expect(orders.latest_order_card).to_be_visible()

        with allure.step("Verify order details (ID, Date, Status, Total amount)"):
            expect(orders.latest_order_id).to_be_visible()
            expect(orders.latest_order_date).to_be_visible()
            expect(orders.latest_order_status).to_be_visible()
            expect(orders.latest_order_item()).to_be_visible()
            expect(orders.latest_order_total).to_contain_text(product_price)