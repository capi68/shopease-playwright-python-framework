"""Tests for Footer UI component."""

import allure
import pytest
from playwright.sync_api import expect

from components.footer import FooterComponent


@allure.epic("EPIC-02: Catalog & Navigation")
@allure.feature("Footer Module")
@pytest.mark.footer
class TestFooter:
    """Test suite for Footer UI component functionality."""

    @pytest.mark.regression
    @allure.story("Footer Navigation & Legal")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Verify footer links and copyright text are properly displayed")
    def test_footer_display(self, footer: FooterComponent) -> None:
        """Verify the correct display of footer component elements."""
        links = ["contact", "shipping", "returns", "profile", "orders", "wishlist"]

        for link in links:
            expect(footer.footer_link(link)).to_be_visible()

        expect(footer.copyright).to_be_visible()