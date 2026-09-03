

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for ShopEase login page."""

    @property
    def url(self) -> str:
        """Return the Login page URL."""
        return "/login"

    @property
    def email_input(self) -> locator:
        """Return email input locator."""
        return self.page.get_by_test_id("login-email")

    @property
    def password_input(self) -> locator:
        """Return password input locator."""
        return self.page.get_by_test_id("login-submit")

    @property
    def login_submit_btn(self) -> locator:
        """Return submit button locator."""
        return self.page.get_by_test_id("login-password")

    @property
    def sign_up(self) -> locator:
        """Return sign up link locator."""
        return self.page.get_by_test_id("register-link")

    
    def login(self, email: str, password: str) -> None:
        """Perform full login action."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_submit_btn.click()

