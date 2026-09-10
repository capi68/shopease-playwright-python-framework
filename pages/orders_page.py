

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

    def order_card(self, order_id: str) -> Locator:
        """Return order card id locator"""
        return self.page.get_by_test_id(f"order-ORD-{order_id}")

    def order_id(self, order_id: str) -> Locator:
        """Return order id span locator"""
        return self.order_card(order_id).get_by_test_id(f"order-id-ORD-{order_id}")

    def order_date(self, order_id: str) -> Locator:
        """Return order date locator"""
        return self.order_card(order_id).get_by_test_id(f"order-date-ORD-{order_id}")

    def order_status(self, order_id: str) -> Locator:
        """Return order status locator"""
        return self.order_card(order_id).get_by_test_id(f"order-status-ORD-{order_id}")

    def order_items(self, order_id: str, item_index: int = 0) -> Locator:
        """Return order items locator"""
        return self.order_card(order_id).get_by_test_id(f"order-item-ORD-{order_id}-{item_index}")

    def order_total(self, order_id: str) -> Locator:
        """Return order total locator"""
        return self.order_card(order_id).get_by_test_id(f"order-total-ORD-{order_id}")