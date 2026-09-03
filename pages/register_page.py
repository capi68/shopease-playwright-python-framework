


from pages.base_page import BasePage
from playwright.sync_api import Locator

class RegisterPage(BasePage):
    """Page Object for ShopEase register page."""

    @property
    def url(self) -> str:
        """Return the register page URL."""
        return "/register"
    
    @property
    def register_name(self) -> Locator:
        """Return Register Name field locator."""
        return self.page.get_by_test_id("register-name")
    
    @property
    def register_email(self) -> Locator:
        """Return register email field locator."""
        return self.page.get_by_test_id("register-email")
    
    @property
    def register_password(self) -> Locator:
        """Return register password field locator."""
        return self.page.get_by_test_id("register-password")
    
    @property
    def confirm_password(self) -> Locator:
        """Return confirm password field locator."""
        return self.page.get_by_test_id("register-confirm")

    @property
    def create_account_btn(self) -> Locator:
        """Return create count submit button locator."""
        return self.page.get_by_test_id("register-submit")

    def register_account(self, name: str, email: str, password: str, confirm_password: str) -> None:
        """Perform full register action."""
        self.register_name.fill(name)
        self.register_email.fill(email)
        self.register_password.fill(password)
        self.confirm_password.fill(confirm_password)
        self.create_count_btn.click()
    