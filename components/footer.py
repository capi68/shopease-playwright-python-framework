

from components.base_component import BaseComponent
from playwright.sync_api import Locator


class Footer(BaseComponent):
    """Component Object for ShopEase footer."""

    @property
    def footer(self) -> Locator:
        """Return footer locator."""
        return self.root


    def footer_link(self, link_name: str) -> Locator:
        """Return contact us link locator."""
        return self.root.get_by_test_id(f"footer-{link_name.lower()}")

    @property
    def copyright(self) -> Locator:
        """Return copyright locator."""
        return self.root.get_by_test_id("footer-copyright")



