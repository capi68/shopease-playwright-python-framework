

import allure
import pytest

from playwright.sync_api import expect
from components.footer import FooterComponent
from components.navbar import NavBarComponent
from pages.orders_page import OrdersPage

class TestOrders:
    """Tests for Orders UI."""

    @pytest.mark.orders
    def test_empty_orders_page_displays_empty_state_and_redirects_to_catalog(
            self, orders_page: OrdersPage, navbar: NavBarComponent, footer: FooterComponent):
        """Verify correct display of orders page without any order,
        and start shopping button works correctly."""
        orders_page.navigate()

        expect(orders_page.orders_empty).to_be_visible()
        expect(orders_page.start_shopping_btn).to_be_visible()
        expect(navbar.nav_bar).to_be_visible()
        expect(footer.footer).to_be_visible()

        #Clicking start shopping button
        orders_page.start_shopping_btn.click()
        expect(orders_page.page).to_have_url("/catalog")
