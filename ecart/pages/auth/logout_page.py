from pages.base_page import BasePage
from utilities.logger import get_logger


class LogoutPage(BasePage):
    
    log = get_logger(__name__)
    
    def __init__(self,page):
        super().__init__(page)

        # locators for logout page
        self.LOGOUT_TEXT = page.get_by_role('heading', name='Account Logout', level=1)

