"""
Root conftest.py --Shared fixtures for the ShopEase test framework.

This file provides:
- Browser configuration (viewport, base_url)
- Authentication fixtures (logged-in pages for each role)
- Page object fixtures (raeady-to-use page objects)
"""

import sys
from pathlib import Path

from pages.catalog_page import CatalogPage

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

@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    """Provide a ready-to-use CatalogePage instance."""
    return CatalogPage(page)


#--------------------------
#Authentication Fixtures
#--------------------------

@pytest.fixture(params=["customer", "vip"])
def authenticated_page(request: pytest.FixtureRequest, page: Page, login_page: LoginPage, settings: Settings) -> Page:
    """Provide a page authenticated for both customer and vip user."""
    role = request.param
    credentials = getattr(settings, role)

    login_page.navigate()
    login_page.login(
        credentials.email,
        credentials.password
    )
    page.wait_for_url("/catalog")
    return page

@pytest.fixture
def wishlist_page(authenticated_page):
    from pages.wishlist_page import WishlistPage
    return WishlistPage(authenticated_page)

@pytest.fixture
def cart_page(authenticated_page):
    from pages.cart_page import CartPage
    return CartPage(authenticated_page)

@pytest.fixture
def navbar(authenticated_page):
    from components.navbar import NavBarComponent
    return NavBarComponent(authenticated_page, authenticated_page.get_by_test_id("navbar"))

@pytest.fixture
def footer(authenticated_page):
    from components.footer import FooterComponent
    return FooterComponent(authenticated_page, authenticated_page.get_by_test_id("store-footer"))

@pytest.fixture
def first_product_id(catalog_page: CatalogPage) -> str:
    """Navigate to catalog, pick the first product card and return its extracted ID."""
    catalog_page.navigate()
    first_card = catalog_page.all_product_cards.first
    att_card = first_card.get_attribute("data-testid")
    return att_card.replace("product-card-prod-", "").strip()