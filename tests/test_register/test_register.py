"""Tests for Register UI functionality."""

import uuid
import allure
import pytest
from playwright.sync_api import Page, expect

from pages.register_page import RegisterPage


@allure.epic("EPIC-01: Authentication")
@allure.feature("Register Module")
@pytest.mark.register
class TestRegister:
    """Test suite for Register UI functionality."""

    @pytest.mark.smoke
    @allure.story("User Registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify that a new user can register successfully")
    def test_register_user(self, register_page: RegisterPage, page: Page) -> None:
        """Verify that a new user can register successfully."""
        with allure.step("Generate dynamic credentials for new user"):
            uid = uuid.uuid4().hex[:8]
            user_name = f"user {uid}"
            user_email = f"user_{uid}@shopease.io"
            user_password = "Password123!"

        with allure.step("Navigate to register page and submit account form"):
            register_page.navigate()
            register_page.register_account(
                name=user_name,
                email=user_email,
                password=user_password,
                confirm_password=user_password,
            )

        with allure.step("Verify successful user creation and redirection to catalog"):
            expect(page).to_have_url("/catalog")

    @pytest.mark.regression
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify error alert when name field is empty")
    def test_register_with_empty_name_field(self, register_page: RegisterPage) -> None:
        """Empty name field should return name error alert and not create account."""
        uid = uuid.uuid4().hex[:8]
        user_name = ""
        user_email = f"user_{uid}@shopease.io"
        user_password = "Password123!"

        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password,
        )

        expect(register_page.name_alert).to_be_visible()

    @pytest.mark.regression
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify error alert when email field is empty")
    def test_register_with_empty_email_field(self, register_page: RegisterPage) -> None:
        """Empty email field should return email error alert and not create account."""
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = ""
        user_password = "Password123!"

        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password,
        )

        expect(register_page.email_alert).to_be_visible()

    @pytest.mark.regression
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify error alert when password field is empty")
    def test_register_with_empty_password_field(self, register_page: RegisterPage) -> None:
        """Empty password field should return password alert and not create account."""
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = f"user{uid}@shopease.io"
        user_password = ""

        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password,
        )

        expect(register_page.password_alert).to_be_visible()

    @pytest.mark.regression
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify error alert when confirm password field is empty")
    def test_register_with_empty_confirm_password_field(
            self, register_page: RegisterPage
    ) -> None:
        """Empty confirm password field should return confirm password alert and not create account."""
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = f"user{uid}@shopease.io"
        user_password = "Password123!"

        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password="",
        )

        expect(register_page.confirm_alert).to_be_visible()

    @pytest.mark.regression
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify validation alerts when submitting form with all fields empty")
    def test_register_with_all_empty_fields(self, register_page: RegisterPage) -> None:
        """All empty required fields should return name/email/password alerts and not create account."""
        register_page.navigate()
        register_page.register_account(
            name="",
            email="",
            password="",
            confirm_password="",
        )

        expect(register_page.name_alert).to_be_visible()
        expect(register_page.email_alert).to_be_visible()
        expect(register_page.password_alert).to_be_visible()

    @pytest.mark.regression
    @allure.story("Navigation Links")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Verify 'Sign in' link redirects to login page")
    def test_sign_in_link(self, register_page: RegisterPage, page: Page) -> None:
        """The 'Sign in' link must redirect to login page."""
        register_page.navigate()
        register_page.sign_in_link.click()

        expect(page).to_have_url("/login")

