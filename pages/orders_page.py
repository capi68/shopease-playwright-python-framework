

from pages.base_page import BasePage
from playwright.sync_api import Locator

class OrdersPage(BasePage):
    """Page Object from ShopEase orders page."""
    
    @property
    def url(self) -> str:
        """Return the orders url page"""
        return "/orders"

    @property
    def orders_empty(self) -> Locator:
        """Return orders empty container locator."""
        return self.page.get_by_test_id("orders-empty")

    @property
    def start_shopping_btn(self) -> Locator:
        """Return start shopping button locator."""
        return self.page.get_by_test_id("shop-now")

    #--------------
    #history
    #--------------

    @property
    def order_list(self) -> Locator:
        """Return order list locator."""
        return self.page.get_by_test_id("orders-list")

    @property
    def latest_order_card(self) -> Locator:
        """Return order card id locator"""
        return self.page.locator("[data-testid^='order-ORD-']").first

    @property
    def latest_order_id(self) -> Locator:
        """Return order id span locator"""
        return self.latest_order_card.locator("[data-testid^='order-id-ORD-']")

    @property
    def latest_order_date(self) -> Locator:
        """Return order date locator"""
        return self.latest_order_card.locator("[data-testid^='order-date-ORD-']")

    @property
    def latest_order_status(self) -> Locator:
        """Return order status locator"""
        return self.latest_order_card.locator("[data-testid^='order-status-ORD-']")

    def latest_order_item(self, item_index: int = 0) -> Locator:
        """Return specific item locator of the latest order by index."""
        return self.latest_order_card.locator(f"[data-testid^='order-item-ORD-'][data-testid$='-{item_index}']")

    @property
    def latest_order_total(self) -> Locator:
        """Return order total locator"""
        return self.latest_order_card.locator("[data-testid^='order-total-ORD-']")