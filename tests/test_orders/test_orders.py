"""Tests for Orders UI functionality."""

import allure
import pytest
from playwright.sync_api import expect

from components.footer import FooterComponent
from components.navbar import NavBarComponent
from pages.orders_page import OrdersPage


@allure.epic("EPIC-05: Orders History")
@allure.feature("Orders Module")
@pytest.mark.orders
class TestOrders:
    """Test suite for Orders UI functionality."""

    @pytest.mark.smoke
    @allure.story("Empty Orders State")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify empty orders page displays empty state and redirects to catalog")
    def test_empty_orders_page_displays_empty_state_and_redirects_to_catalog(
            self, orders_page: OrdersPage, navbar: NavBarComponent, footer: FooterComponent
    ) -> None:
        """Verify correct display of orders page without any order and start shopping button navigation."""
        with allure.step("Navigate to Orders page"):
            orders_page.navigate()

        with allure.step("Verify empty state container and navigation components are visible"):
            expect(orders_page.orders_empty).to_be_visible()
            expect(orders_page.start_shopping_btn).to_be_visible()
            expect(navbar.nav_bar).to_be_visible()
            expect(footer.footer).to_be_visible()

        with allure.step("Click 'Start Shopping' button and verify redirection to catalog"):
            orders_page.start_shopping_btn.click()
            expect(orders_page.page).to_have_url("/catalog")