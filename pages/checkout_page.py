

from pages.base_page import BasePage
from playwright.sync_api import Locator

class CheckoutPage(BasePage):
    """Page Object for ShopEase order page."""

    @property
    def url(self) -> str:
        """Return the checkout url page"""
        return "/checkout"
    
    @property
    def checkout_steps(self) -> Locator:
        """Return checkout steps container locator"""
        return self.page.get_by_test_id("checkout-steps")

    @property
    def shipping_step(self) -> Locator:
        """Return shipping step locator."""
        return self.page.get_by_test_id("step-1")

    @property
    def payment_step(self) -> Locator:
        """Return payment step locator."""
        return self.page.get_by_test_id("step-2")

    @property
    def review_step(self) -> Locator:
        """Return review step locator."""
        return self.page.get_by_test_id("step-3")

    #-------------
    #shipping
    #-------------

    @property
    def shipping_form(self) -> Locator:
        """Return shipping form locator."""
        return self.page.get_by_test_id("shipping-form")

    @property
    def shipping_name(self) -> Locator:
        """Return shipping name locator."""
        return self.page.get_by_test_id("shipping-name")

    @property
    def shipping_address(self) -> Locator:
        """Return shipping address locator."""
        return self.page.get_by_test_id("shipping-address")

    @property
    def shipping_city(self) -> Locator:
        """Return shipping citty locator."""
        return self.page.get_by_test_id("shipping-city")

    @property
    def shipping_zip(self) -> Locator:
        """Return shipping zip locator."""
        return self.page.get_by_test_id("shipping-zip")

    @property
    def shipping_country(self) -> Locator:
        """Return shipping country locator."""
        return self.page.get_by_test_id("shipping-country")

    @property
    def shipping_phone(self) -> Locator:
        """Return shipping phone locator."""
        return self.page.get_by_test_id("shipping-phone")

    @property
    def continue_to_payment_btn(self) -> Locator:
        """Return continue to payment button locator."""
        return self.page.get_by_test_id("shipping-next")


    def field_error_message(self, field: str) -> Locator:
        """Return error message by specified field locator."""
        return self.page.get_by_test_id(f"error-ship-{field.lower()}")

    #-----------
    #Payment
    #-----------

    @property
    def payment_form(self) -> Locator:
        """Return payment form locator."""
        return self.page.get_by_test_id("payment-form")

    @property
    def name_on_card(self) -> Locator:
        """Return name on card field locator."""
        return self.page.get_by_test_id("payment-name")

    @property
    def number_card(self) -> Locator:
        """Return number card field locator."""
        return self.page.get_by_test_id("payment-card")

    @property
    def card_expiry(self) -> Locator:
        """Return card expiry field locator."""
        return self.page.get_by_test_id("payment-expiry")

    @property
    def card_cvv(self) -> Locator:
        """Return card cvv field locator."""
        return self.page.get_by_test_id("payment-cvv")

    @property
    def back_btn(self) -> Locator:
        """Return back button locator."""
        return self.page.get_by_test_id("payment-back")

    @property
    def review_order_btn(self) -> Locator:
        """Return review order button locator."""
        return self.page.get_by_test_id("payment-next")

    def error_card_alerts(self, field: str) -> Locator:
        """Return error card fields locators."""
        return self.page.get_by_test_id(f"error-card-{field}")

    #-------------
    #review
    #-------------
    
    @property
    def review_section(self) -> Locator:
        """Return review section locator."""
        return self.page.get_by_test_id("review-section")
    

    def review_item(self, product_id: str) -> Locator:
        """Return review item locator."""
        return self.page.get_by_test_id(f"review-item-prod-{product_id}")

    @property
    def review_shipping(self) -> Locator:
        """Return review ship info locator."""
        return self.page.get_by_test_id("review-shipping")

    @property
    def review_total(self) -> Locator:
        """Return review total amount locator."""
        return self.page.get_by_test_id("review-total")

    @property
    def review_back_btn(self) -> Locator:
        """Return back button locator."""
        return self.page.get_by_test_id("review-back")

    @property
    def place_order_btn(self) -> Locator:
        """Return place order button locator."""
        return self.page.get_by_test_id("place-order")

