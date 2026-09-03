"""Tests from  Register UI."""

import allure
import pytest
import uuid
from playwright.sync_api import expect, Page
from pages.register_page import RegisterPage
from config.settings import Settings

class TestRegister:
    """Tests Register UI."""

    @pytest.mark.register
    @pytest.mark.smoke
    def test_register_user(self, register_page: RegisterPage, page: Page, settings: Settings):
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