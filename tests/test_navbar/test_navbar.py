from csv import excel

import allure
import pytest

from playwright.sync_api import expect, Page
from components.navbar import NavBarComponent
from pages.catalog_page import CatalogPage


class TestNavbar:
    """Tests for NavBar UI."""


    def test_navbar_display(self, navbar: NavBarComponent) -> None:
        """Verify the correctly display of navbar."""

        links = ["catalog","wishlist","orders","cart","profile","logout"]

        expect(navbar.navbar_brand).to_be_visible()
        expect(navbar.search_input).to_be_visible()
        expect(navbar.search_btn).to_be_visible()
        expect(navbar.navbar_brand).to_be_visible()
        for link in links:
            expect(navbar.navbar_links(link)).to_be_visible()


    @pytest.mark.parametrize("link", ["catalog","wishlist","orders","cart","profile"])
    def test_redirect_link(self, navbar: NavBarComponent, link) -> None:
        """Verify that all navbar links redirect for specific page."""


        navbar.navbar_links(link).click()

        expect(navbar.page).to_have_url(f"/{link}")


    def test_logout_link(self, navbar: NavBarComponent) -> None:
        """Verify that logout link redirect to login page."""

        navbar.navbar_links("logout").click()

        expect(navbar.page).to_have_url("/catalog")


    def test_search_product(self, navbar: NavBarComponent, catalog_page: CatalogPage) -> None:
        """Verify the correct function of navbar search, should filter products by query."""

        search_query = "organic"
        navbar.search_product(search_query)

        expect(catalog_page.page).to_have_url(f"/catalog?search={search_query}")

        product_names = catalog_page.product_name.all_text_contents()
        print(product_names)

        assert len(product_names) > 0, f"No products found for query: '{search_query}'"

        for name in product_names:
            assert search_query.lower() in name.lower(), (
                f"Product '{name}', does nor contain search term '{search_query}'"
            )


    @pytest.mark.navbar
    @pytest.mark.xfail(
        reason="TRELLO-BUG: Clearing search input dos not reset catalog grid filter",
        strict=True
    )
    def test_clearing_search_input_restore_full_catalog(self, navbar: NavBarComponent, catalog_page: CatalogPage) -> None:
        """Verify that clearing search input resets catalog and display all products."""

        #Initial cards count
        initial_cards_count = int(catalog_page.results_count.inner_text().replace(" products", "").strip())

        #Initial search to apply filter.
        navbar.search_product("organic")
        expect(catalog_page.page).to_have_url(f"/catalog?search=organic")

        #Clear search input
        navbar.search_input.clear()
        navbar.search_btn.click()

        second_cards_count = int(catalog_page.results_count.inner_text().replace(" products", "").strip())

        assert initial_cards_count == second_cards_count




