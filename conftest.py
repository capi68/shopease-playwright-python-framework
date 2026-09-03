"""
Root conftest.py --Shared fixtures for the ShopEase test framework.

This file provides:
- Browser configuration (viewport, base_url)
- Authentication fixtures (logged-in pages for each role)
- Page object fixtures (raeady-to-use page objects)
"""

import sys
from pathlib import Path

# Ensures that the project recognizes the root folders in the PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from playwright.sync_api import Page
from config.settings import Settings
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

#----------------
#Configuration
#----------------

@pytest.fixture(scope="session")
def settings() -> Settings:
    """Provide settings singleton to all tests."""
    return Settings()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings):
    """Configure browser context from settings."""
    return {
        **browser_context_args,
        "base_url": settings.base_url,
        "viewport": {
            "width": settings.viewport.width,
            "height": settings.viewport.height
        }
    }

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provide a ready-to-use LoginPage instance."""
    return LoginPage(page)

@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    """Provide a ready-to-use RegisterPage instance."""
    return RegisterPage(page)


#--------------------------
#Authentication Fixtures
#--------------------------

@pytest.fixture
def customer_page(page: Page, login_page: LoginPage, settings: Settings) -> Page:
    """Provide a page authenticated as a customer user."""
    login_page.navigate()
    login_page.login(
        settings.customer.email,
        settings.customer.password
    )
    page.wait_for_url("/catalog")
    return page