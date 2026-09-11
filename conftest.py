"""
Root conftest.py --Shared fixtures for the ShopEase test framework.

This file provides:
- Browser configuration (viewport, base_url)
- Authentication fixtures (logged-in pages for each role)
- Page object fixtures (raeady-to-use page objects)
"""

import sys
from pathlib import Path

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.orders_page import OrdersPage

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
def checkout_page(authenticated_page):
    from pages.checkout_page import CheckoutPage
    return CheckoutPage(authenticated_page)

@pytest.fixture
def orders_page(authenticated_page):
    from pages.orders_page import OrdersPage
    return OrdersPage(authenticated_page)

@pytest.fixture
def profile_page(authenticated_page):
    from pages.profile_page import ProfilePage
    return ProfilePage(authenticated_page)

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

@pytest.fixture
def order_ready_to_checkout(
        first_product_id: str,
        catalog_page: CatalogPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage) -> CheckoutPage:
    """Create a valid order, ready to check out proceed."""

    catalog_page.add_to_card_btn(first_product_id).click()
    cart_page.navigate()

    product_price = cart_page.cart_item_price(first_product_id).inner_text()
    product_name = cart_page.cart_item_name(first_product_id).inner_text()

    #save instances
    checkout_page.product_id = first_product_id
    checkout_page.product_price = product_price
    checkout_page.product_name = product_name

    cart_page.checkout_btn.click()
    return checkout_page

@pytest.fixture
def shipping_to_payment_order(order_ready_to_checkout: CheckoutPage) -> CheckoutPage:
    """Create a shipping information ready to payment."""
    page = order_ready_to_checkout

    page.shipping_data = {
        "name": "Peter Parker",
        "address": "#20 Ingram Street",
        "city": "Queens",
        "zip": "11101",
        "country": "US",
        "phone": "+19876543210"
    }

    order_ready_to_checkout.shipping_name.fill(page.shipping_data["name"])
    order_ready_to_checkout.shipping_address.fill(page.shipping_data["address"])
    order_ready_to_checkout.shipping_city.fill(page.shipping_data["city"])
    order_ready_to_checkout.shipping_zip.fill(page.shipping_data["zip"])
    order_ready_to_checkout.shipping_country.select_option(page.shipping_data["country"])
    order_ready_to_checkout.shipping_phone.fill(page.shipping_data["phone"])
    order_ready_to_checkout.continue_to_payment_btn.click()

    return order_ready_to_checkout

@pytest.fixture
def payment_to_review_order(shipping_to_payment_order: CheckoutPage) -> CheckoutPage:
    """Create a payment information ready to review."""
    shipping_to_payment_order.name_on_card.fill("Peter Parker")
    shipping_to_payment_order.number_card.fill("4009 1753 3280 6176")
    shipping_to_payment_order.card_expiry.fill("02/29")
    shipping_to_payment_order.card_cvv.fill("123")
    shipping_to_payment_order.review_order_btn.click()

    return shipping_to_payment_order

@pytest.fixture
def review_to_orders_page(
        payment_to_review_order: CheckoutPage,orders_page: OrdersPage) -> OrdersPage:
    """Complete order in review step and redirect to OrdersPage with shared order context."""
    page = payment_to_review_order

    # transfer context for OrdersPage
    orders_page.product_id = page.product_id
    orders_page.product_price = page.product_price
    orders_page.product_name = page.product_name
    orders_page.shipping_data = page.shipping_data

    page.place_order_btn.click()

    return orders_page

