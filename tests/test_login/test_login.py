"""Tests from Login UI."""

import allure
import pytest
from playwright.sync_api import expect, Page
from pages.login_page import LoginPage
from config.settings import Settings, Credentials

@pytest.mark.login
class TestLogin:
    """Tet Login UI."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("role", ["customer", "vip"])
    def test_valid_login(self, login_page: LoginPage, page: Page, settings: Settings, role: str) -> None:
        """Verify that a customer/vip can log in and reach the catalog page."""
        #Navigate to /login
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.login(
            credentials.email,
            credentials.password
        )

        expect(page).to_have_url("/catalog")


    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    def test_log_in_empty_password(self, login_page: LoginPage, settings: Settings, role: str) -> None:
        """With the password field empty, the 'Sign In' button must remain disabled."""
        #Navigate to /login
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.email_input.fill(credentials.email)
        login_page.password_input.fill("")

        expect(login_page.login_submit_btn).to_be_disabled()



    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    def test_log_in_empty_email(self, login_page: LoginPage, settings: Settings, role: str) -> None:
        """With the email field empty, the 'Sign In' button must remain disabled."""
        #Navigate to /login
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.email_input.fill("")
        login_page.password_input.fill(credentials.password)

        expect(login_page.login_submit_btn).to_be_disabled()


    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    def test_invalid_password(self, login_page: LoginPage, settings: Settings, role: str) -> None:
        """With invalid password should return error message and not sign in."""
        #Navigate to /login
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.login(
            credentials.email,
            "wrongpass"
        )
        expect(login_page.error_alert).to_be_visible()


    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    def test_invalid_email(self, login_page: LoginPage, settings: Settings, role: str) -> None:
        """With invalid email should return error message and not sign in."""
        #Navigate to /login
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.login(
            "customer999@shopease.io",
            credentials.password
        )

        expect(login_page.error_alert).to_be_visible()


    @pytest.mark.regression
    def test_register_link(self, login_page: LoginPage, page: Page) -> None:
        """Verify that the register link works correctly."""
        #Navigate to /login
        login_page.navigate()

        login_page.register_link.click()

        expect(page).to_have_url("/register")
