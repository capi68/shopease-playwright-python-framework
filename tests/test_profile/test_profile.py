

import allure
import pytest
import re
from playwright.sync_api import expect, Page

from components.footer import FooterComponent
from components.navbar import NavBarComponent
from pages.profile_page import ProfilePage

class TestProfile:
    """Tests for Profile UI."""

    @pytest.mark.profile
    def test_profile_page_display(
            self,
            profile_page: ProfilePage,
            navbar: NavBarComponent,
            footer: FooterComponent,
            request: pytest.FixtureRequest) -> None:
        """Verify that Profile page display correctly."""
        profile_page.navigate()

        current_role = request.node.callspec.params["authenticated_page"]

        expect(profile_page.profile_card).to_be_visible()
        expect(profile_page.profile_avatar).to_be_visible()
        expect(profile_page.profile_name).to_be_visible()
        expect(profile_page.profile_email).to_be_visible()
        expect(profile_page.profile_role).to_contain_text(
            re.compile(current_role, re.I)
        )
        expect(profile_page.stat_order).to_be_visible()
        expect(profile_page.total_spent).to_be_visible()
        expect(navbar.nav_bar).to_be_visible()
        expect(footer.footer).to_be_visible()