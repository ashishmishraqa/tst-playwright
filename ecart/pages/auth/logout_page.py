from pages.base_page import BasePage
from playwright.sync_api import expect
from utilities.logger import get_logger


class LogoutPage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)

    @property
    def logout_text(self):
        return self.page.get_by_role("heading", name="Account Logout", level=1)

    def verify_logout_text(self):
        expect(self.logout_text).to_be_visible(timeout=5000)
