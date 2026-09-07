

import allure
import pytest
from playwright.sync_api import expect, Page


from pages.catalog_page import CatalogPage

class TestCatalog:
    """Tests Catalog UI."""

    @pytest.mark.catalog
    @pytest.mark.usefixtures("authenticated_page")
    def test_catalog_page(self,catalog_page: CatalogPage, nav_bar, footer) -> None:
        """Verify that authenticated users (customer/vip) can see catalog page correctly."""

        filter_categories = ["all", "electronics", "clothing", "home", "sports", "books"]

        expect(catalog_page.results_count).to_be_visible()
        expect(catalog_page.product_grid).to_be_visible()
        for category in filter_categories:
            expect(catalog_page.filter_category(category)).to_be_visible()
        expect(catalog_page.filter_price_min).to_be_visible()
        expect(catalog_page.filter_price_max).to_be_visible()
        expect(catalog_page.filter_sort).to_be_visible()
        expect(nav_bar.nav_bar).to_be_visible()
        expect(footer.footer).to_be_visible()

