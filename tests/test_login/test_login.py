"""Tests for Login UI."""

import allure
import pytest
from playwright.sync_api import Page, expect

from config.settings import Settings
from pages.login_page import LoginPage


@allure.epic("EPIC-01: Authentication")
@allure.feature("Login Module")
@pytest.mark.login
class TestLogin:
    """Test suite for Login UI functionality."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("role", ["customer", "vip"])
    @allure.story("Valid Credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify {role} user can log in successfully with valid credentials")
    def test_valid_login(
            self, login_page: LoginPage, page: Page, settings: Settings, role: str
    ) -> None:
        """Verify that a customer/vip can log in and reach the catalog page."""
        with allure.step("Navigate to login page"):
            login_page.navigate()

        with allure.step(f"Submit login form with valid {role} credentials"):
            credentials = getattr(settings, role)
            login_page.login(credentials.email, credentials.password)

        with allure.step("Verify redirection to catalog page"):
            expect(page).to_have_url("/catalog")

    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify 'Sign In' button is disabled when password field is empty for {role}")
    def test_log_in_empty_password(
            self, login_page: LoginPage, settings: Settings, role: str
    ) -> None:
        """With the password field empty, the 'Sign In' button must remain disabled."""
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.email_input.fill(credentials.email)
        login_page.password_input.fill("")

        expect(login_page.login_submit_btn).to_be_disabled()

    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify 'Sign In' button is disabled when email field is empty for {role}")
    def test_log_in_empty_email(
            self, login_page: LoginPage, settings: Settings, role: str
    ) -> None:
        """With the email field empty, the 'Sign In' button must remain disabled."""
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.email_input.fill("")
        login_page.password_input.fill(credentials.password)

        expect(login_page.login_submit_btn).to_be_disabled()

    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    @allure.story("Invalid Credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify error alert when logging in with invalid password for {role}")
    def test_invalid_password(
            self, login_page: LoginPage, settings: Settings, role: str
    ) -> None:
        """With invalid password should return error message and not sign in."""
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.login(credentials.email, "wrongpass")

        expect(login_page.error_alert).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.parametrize("role", ["customer", "vip"])
    @allure.story("Invalid Credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify error alert when logging in with unregistered email for {role}")
    def test_invalid_email(
            self, login_page: LoginPage, settings: Settings, role: str
    ) -> None:
        """With invalid email should return error message and not sign in."""
        login_page.navigate()

        credentials = getattr(settings, role)
        login_page.login("customer999@shopease.io", credentials.password)

        expect(login_page.error_alert).to_be_visible()

    @pytest.mark.regression
    @allure.story("Navigation Links")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Verify registration link redirects to /register")
    def test_register_link(self, login_page: LoginPage, page: Page) -> None:
        """Verify that the register link works correctly."""
        login_page.navigate()
        login_page.register_link.click()

        expect(page).to_have_url("/register")
