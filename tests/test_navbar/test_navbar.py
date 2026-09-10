

import allure
import pytest

from playwright.sync_api import expect, Page
from components.navbar import NavBarComponent
from pages.catalog_page import CatalogPage
from pages.wishlist_page import WishlistPage


@pytest.mark.navbar
class TestNavbar:
    """Tests for NavBar UI."""

    def test_navbar_display(self, navbar: NavBarComponent) -> None:
        """Verify the correctly display of navbar."""

        links = ["catalog","wishlist","orders","cart","profile","logout"]

        expect(navbar.navbar_brand).to_be_visible()
        expect(navbar.search_input).to_be_visible()
        expect(navbar.search_btn).to_be_visible()
        for link in links:
            expect(navbar.navbar_links(link)).to_be_visible()


    @pytest.mark.parametrize("link", ["catalog","wishlist","orders","cart","profile"])
    def test_redirect_link(self, navbar: NavBarComponent, link) -> None:
        """Verify that all navbar links redirect for specific page."""


        navbar.navbar_links(link).click()

        expect(navbar.page).to_have_url(f"/{link}")


    def test_logout_link(self, navbar: NavBarComponent) -> None:
        """Verify that logout link redirect to catalog page."""

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


    def test_add_product_to_wishlist(self, navbar: NavBarComponent, catalog_page: CatalogPage, wishlist_page: WishlistPage) -> None:
        """Verify that click in add to wishlist button, the product appears in wishlist page."""

        catalog_page.navigate()
        #select first card in catalog
        first_card = catalog_page.all_product_cards.first

        #extract product_id
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()

        #add to wishlist
        catalog_page.wishlist_btn(product_id).click()

        #navigate to wishlist page
        navbar.navbar_links("wishlist").click()
        expect(wishlist_page.page).to_have_url("/wishlist")

        #Verify
        expect(wishlist_page.wl_item_card(product_id)).to_be_visible()


    def test_cart_badge_function(self, navbar: NavBarComponent, catalog_page: CatalogPage) -> None:
        """Verify that cart badge function correctly."""

        catalog_page.navigate()
        expect(navbar.cart_badge).not_to_be_visible()
        #select first card in catalog
        first_card = catalog_page.all_product_cards.first

        #xtract product_id
        att_card = first_card.get_attribute("data-testid")
        product_id = att_card.replace("product-card-prod-", "").strip()

        #add to cart
        catalog_page.add_to_card_btn(product_id).click()

        expect(navbar.cart_badge).to_be_visible()
        expect(navbar.cart_badge).to_have_text("1")









