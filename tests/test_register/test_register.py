"""Tests from  Register UI."""
from urllib import response

import allure
import pytest
import uuid
from playwright.sync_api import expect, Page
from pages.register_page import RegisterPage
from config.settings import Settings

class TestRegister:
    """Tests Register UI."""


    @pytest.mark.smoke
    def test_register_user(self, register_page: RegisterPage, page: Page):
        """Verify that a new user can register successfully."""
        #Data new user
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = f"user_{uid}@shopease.io"
        user_password = "Password123!"

        #Navigate to register
        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )

        expect(page).to_have_url("/catalog")


    @pytest.mark.regression
    def test_register_with_empty_name_field(self,register_page: RegisterPage):
        """Empty name field should return name error alert and not create account."""
        #Data new user
        uid = uuid.uuid4().hex[:8]
        user_name = ""
        user_email = f"user_{uid}@shopease.io"
        user_password = "Password123!"

        #Navigate to register
        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )

        expect(register_page.name_alert).to_be_visible()


    @pytest.mark.regression
    def test_register_with_empty_email_field(self,register_page: RegisterPage):
        """Empty email field should return email error alert and not create account."""
        #Data new user
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = ""
        user_password = "Password123!"

        #Navigate to register
        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )

        expect(register_page.email_alert).to_be_visible()


    @pytest.mark.regression
    def test_register_with_empty_password_field(self, register_page: RegisterPage):
        """Empty password field should return password alert and not create account."""
        #Data new user
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = f"user{uid}@shopease.io"
        user_password = ""

        #Navigate to register
        register_page.navigate()
        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )

        expect(register_page.password_alert).to_be_visible()


    @pytest.mark.regression
    def test_register_with_empty_confirm_password_field(self, register_page: RegisterPage):
        """Empty confirm password field should return confirm password alert and not create account."""
        #Data new user
        uid = uuid.uuid4().hex[:8]
        user_name = f"user {uid}"
        user_email = f"user{uid}@shopease.io"
        user_password = "Password123!"

        #Navigate to register
        register_page.navigate()

        register_page.register_account(
            name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=""
        )

        expect(register_page.confirm_alert).to_be_visible()


    @pytest.mark.regression
    def test_register_with_all_empty_fields(self, register_page: RegisterPage):
        """All empty required fields should return name alert/email alert/password alert
        and not create account."""

        #Navigate to register
        register_page.navigate()

        register_page.register_account(
            name="",
            email="",
            password="",
            confirm_password=""
        )

        expect(register_page.name_alert).to_be_visible()
        expect(register_page.email_alert).to_be_visible()
        expect(register_page.password_alert).to_be_visible()


    @pytest.mark.register
    @pytest.mark.regression
    def test_sign_in_link(self, register_page: RegisterPage, page: Page):
        """ The 'Sign in' link must be redirected to login page."""
        #Navigate to register
        register_page.navigate()

        register_page.sign_in_link.click()

        expect(page).to_have_url("/login")


