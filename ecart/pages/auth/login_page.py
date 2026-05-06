from pages.base_page import BasePage
from utilities import logger


class LoginPage(BasePage):

    log = logger.get_logger(__name__)

    def get_login_page_title(self):
        return self.get_title()

