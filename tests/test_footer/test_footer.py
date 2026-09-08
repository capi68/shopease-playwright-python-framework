

import allure
import pytest
from playwright.sync_api import expect, Page

from components.footer import FooterComponent


class TestFooter:
    """Tests Footer UI."""

    @pytest.mark.footer
    def test_footer_display(self, footer: FooterComponent) -> None:
        """Verify de correct display of footer component."""

        links = ["contact", "shipping","returns","profile","orders","wishlist"]

        for link in links:
            expect(footer.footer_link(link)).to_be_visible()

        expect(footer.copyright).to_be_visible()