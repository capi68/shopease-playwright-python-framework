

import allure
import pytest
from playwright.sync_api import expect, Page

from components.footer import FooterComponent
from components.navbar import NavBarComponent
from pages.catalog_page import CatalogPage


@pytest.mark.catalog
class TestCatalog:
    """Tests Catalog UI."""


    @pytest.mark.usefixtures("authenticated_page")
    def test_catalog_page(self,catalog_page: CatalogPage, navbar: NavBarComponent, footer: FooterComponent) -> None:
        """Verify that authenticated users (customer/vip) can see catalog page correctly."""

        filter_categories = ["all", "electronics", "clothing", "home", "sports", "books"]

        expect(catalog_page.results_count).to_be_visible()
        expect(catalog_page.product_grid).to_be_visible()
        for category in filter_categories:
            expect(catalog_page.filter_category(category)).to_be_visible()
        expect(catalog_page.filter_price_min).to_be_visible()
        expect(catalog_page.filter_price_max).to_be_visible()
        expect(catalog_page.filter_sort).to_be_visible()
        expect(navbar.nav_bar).to_be_visible()
        expect(footer.footer).to_be_visible()


    @pytest.mark.usefixtures("authenticated_page")
    @pytest.mark.parametrize("category", ["electronics", "clothing", "home", "sports", "books"])
    def test_filter_category_electronics_updates_grid(self, catalog_page: CatalogPage, category) -> None:
        """Verify that filtering by category 'electronics' correctly mutates product grid."""

        #Initial product count
        initial_text = catalog_page.results_count.inner_text()
        total_count = int(initial_text.replace("products", "").strip())

        #Apply filtar 'electronics' category
        catalog_page.filter_category(category).click()

        expect(catalog_page.results_count).not_to_have_text(initial_text)

        filter_count = int(catalog_page.results_count.inner_text().replace("products", "").strip())

        assert filter_count < total_count


    @pytest.mark.usefixtures("authenticated_page")
    def test_filter_by_price_range(self, catalog_page: CatalogPage) -> None:
        """Verify that all filtered products strictly call within the selected price range."""

        min_price = 100.0
        max_price = 200.0

        catalog_page.apply_price_range(str(min_price), str(max_price))

        expect(catalog_page.product_price.first).to_be_visible()

        products_prices = catalog_page.product_price.all_inner_texts()
        assert len(products_prices) > 0, "Expected at least one product in rage"

        for price in products_prices:
            clean_price = float(price.replace("$", "").strip())
            assert min_price<= clean_price <= max_price, (
                f"Product price {clean_price} violates range [{min_price}, {max_price}]"
            )


    @pytest.mark.usefixtures("authenticated_page")
    def test_sort_products_price_ascending(self, catalog_page: CatalogPage) -> None:
        """Verify that products are sorted by price in ascending order."""

        #Select sort price-asc
        catalog_page.filter_sort.select_option("price-asc")
        prices_list = []
        product_text = catalog_page.product_price.all_inner_texts()

        for product in product_text:
            price = float(product.replace("$", "").strip())
            prices_list.append(price)

        assert prices_list == sorted(prices_list)


    @pytest.mark.usefixtures("authenticated_page")
    def test_sort_products_price_descending(self, catalog_page: CatalogPage) -> None:
        """Verify that products ar sorted by price in descending order."""

        #Select sort price-desc
        catalog_page.filter_sort.select_option("price-desc")
        price_list = []

        product_text = catalog_page.product_price.all_inner_texts()

        for product in product_text:
            price = float(product.replace("$", "").strip())
            price_list.append(price)

        assert price_list == sorted(price_list, reverse=True)



    @pytest.mark.usefixtures("authenticated_page")
    def test_sort_products_by_rating(self, catalog_page: CatalogPage) -> None:
        """Verify that products ar sorted by descending rating."""
        #Select sort by rating
        catalog_page.filter_sort.select_option("rating")

        rating_list = []

        product_text = catalog_page.product_rating.all_inner_texts()

        for product in product_text:
            split_rating = product.split("(")[0]
            rating = split_rating.count("★") + (0.5 if "½" in split_rating else 0.0)
            rating_list.append(rating)

        assert rating_list == sorted(rating_list, reverse=True)



    @pytest.mark.usefixtures("authenticated_page")
    def test_sort_products_by_name(self, catalog_page: CatalogPage) -> None:
        """Verify that products ar sorted by alphabetic order."""
        #Select sort by name
        catalog_page.filter_sort.select_option("name")


        product_names = catalog_page.product_name.all_inner_texts()

        assert product_names == sorted(product_names)



    @pytest.mark.usefixtures("authenticated_page")
    def test_filter_range_negative_values(self, catalog_page: CatalogPage) -> None:
        """Verify system behavior when entering negative price values."""

        catalog_page.apply_price_range("-100", "-200")

        expect(catalog_page.empty_catalog).to_be_visible()




