"""Tests for Navbar UI component and navigation."""

import allure
import pytest
from playwright.sync_api import Page, expect

from components.navbar import NavBarComponent
from pages.catalog_page import CatalogPage


@allure.epic("EPIC-02: Catalog & Navigation")
@allure.feature("Navbar Module")
@pytest.mark.navbar
class TestNavbar:
    """Test suite for Navbar component links, search, and badges."""

    @pytest.mark.regression
    @allure.story("Navbar Elements Visibility")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify navbar brand, search bar, and navigation links are properly displayed")
    def test_navbar_display(self, navbar: NavBarComponent) -> None:
        """Verify the correct display of navbar elements."""
        links = ["catalog", "wishlist", "orders", "cart", "profile", "logout"]

        expect(navbar.navbar_brand).to_be_visible()
        expect(navbar.search_input).to_be_visible()
        expect(navbar.search_btn).to_be_visible()
        for link in links:
            expect(navbar.navbar_links(link)).to_be_visible()

    @pytest.mark.regression
    @pytest.mark.parametrize("link", ["catalog", "wishlist", "orders", "cart", "profile"])
    @allure.story("Navigation Links")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify navbar link '{link}' redirects to correct route '/{link}'")
    def test_redirect_link(self, navbar: NavBarComponent, link: str) -> None:
        """Verify that all navbar links redirect to specific page."""
        navbar.navbar_links(link).click()
        expect(navbar.page).to_have_url(f"/{link}")

    @pytest.mark.regression
    @allure.story("Navigation Links")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify logout link redirects to catalog page")
    def test_logout_link(self, navbar: NavBarComponent) -> None:
        """Verify that logout link redirects to catalog page."""
        navbar.navbar_links("logout").click()
        expect(navbar.page).to_have_url("/catalog")

    @pytest.mark.regression
    @allure.story("Product Search")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify search bar filters products in catalog by query term")
    def test_search_product(
            self, navbar: NavBarComponent, catalog_page: CatalogPage
    ) -> None:
        """Verify the correct function of navbar search, should filter products by query."""
        search_query = "organic"
        navbar.search_product(search_query)

        expect(catalog_page.page).to_have_url(f"/catalog?search={search_query}")

        product_names = catalog_page.all_product_name.all_text_contents()

        assert len(product_names) > 0, f"No products found for query: '{search_query}'"

        for name in product_names:
            assert search_query.lower() in name.lower(), (
                f"Product '{name}' does not contain search term '{search_query}'"
            )

    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="TRELLO-BUG: Clearing search input does not reset catalog grid filter",
        strict=True,
    )
    @allure.story("Product Search")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify clearing search input restores full catalog product grid")
    def test_clearing_search_input_restore_full_catalog(
            self, navbar: NavBarComponent, catalog_page: CatalogPage
    ) -> None:
        """Verify that clearing search input resets catalog and displays all products."""
        # Initial cards count
        initial_cards_count = int(
            catalog_page.results_count.inner_text().replace(" products", "").strip()
        )

        # Initial search to apply filter
        navbar.search_product("organic")
        expect(catalog_page.page).to_have_url("/catalog?search=organic")

        # Clear search input
        navbar.search_input.clear()
        navbar.search_btn.click()

        second_cards_count = int(
            catalog_page.results_count.inner_text().replace(" products", "").strip()
        )

        assert initial_cards_count == second_cards_count

    @pytest.mark.regression
    @allure.story("Cart Badge")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify cart badge updates count when adding a product from catalog")
    def test_cart_badge_function(
            self, navbar: NavBarComponent, catalog_page: CatalogPage
    ) -> None:
        """Verify that cart badge functions correctly."""
        catalog_page.navigate()
        expect(navbar.cart_badge).not_to_be_visible()

        # Select first card in catalog
        first_card = catalog_page.all_product_cards.first

        # Extract product_id
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()

        # Add to cart
        catalog_page.add_to_card_btn(product_id).click()

        expect(navbar.cart_badge).to_be_visible()
        expect(navbar.cart_badge).to_have_text("1")



