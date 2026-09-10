

from pages.base_page import BasePage
from playwright.sync_api import Locator

class ProfilePage(BasePage):
    """Page Object for ShopEase profile page."""
    
    @property
    def url(self) -> str:
        """Return the url profile page."""
        return "/profile"
    
    @property
    def profile_card(self) -> Locator:
        """Return profile car locator."""
        return self.page.get_by_test_id("profile-card")
    
    @property
    def profile_avatar(self) -> Locator:
        """Return profile avatar locator."""
        return self.page.get_by_test_id("profile-avatar")
    
    @property
    def profile_name(self) -> Locator:
        """Return profile name locator."""
        return self.page.get_by_test_id("profile-name")

    @property
    def profile_email(self) -> Locator:
        """Return profile email locator."""
        return self.page.get_by_test_id("profile-email")
    
    @property
    def profile_role(self) -> Locator:
        """Return profile role locator."""
        return self.page.get_by_test_id("profile-role")
    
    @property
    def stat_order(self) -> Locator:
        """Return stat orders locator."""
        return self.page.get_by_test_id("stat-orders")
    
    @property
    def total_spent(self) -> Locator:
        """Return total spent locator."""
        return self.page.get_by_test_id("stat-total-spent")