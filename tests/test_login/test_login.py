"""Tests from Login UI."""

import allure
import pytest
from playwright.sync_api import expect, Page
from pages.login_page import LoginPage
from config.settings import Settings


class TestLogin:
    """Tets Login UI."""

    @pytest.mark.login
    @pytest.mark.smoke
    @pytest.mark.parametrize("role", ["customer", "vip"])
    def test_valid_login(self, login_page: LoginPage, page: Page, settings: Settings, role):
        """Verify that a customer/vip can log in and reach the catalog page."""
        #Navigate to /login
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.login(
            credentials.email,
            credentials.password
        )

        expect(page).to_have_url("/catalog")