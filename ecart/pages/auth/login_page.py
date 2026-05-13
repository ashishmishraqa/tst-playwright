from pages.base_page import BasePage
from utilities.logger import get_logger


class LoginPage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)
        # Locators for OpenCart
        self.USERNAME = page.locator('#input-email')
        self.PASSWORD = page.locator('#input-password')
        self.LOGIN_BUTTON = page.locator('input[value="Login"]')
        self.LOGOUT_BUTTON = page.locator('#column-right').get_by_role('link', name='Logout')
        self.ERROR_MESSAGE = page.locator('.alert-danger')  # Assuming error messages are in alert-danger

    def navigate_to_login_page(self, url):
        self.log.info(f"Opening Login page: {url}")
        self.go_to(url)


    def get_login_page_title(self):
        return self.get_title()

    def login(self, username, password):
        self.log.info(f"Logging in with username: {username}")
        self.USERNAME.fill(username)
        self.PASSWORD.fill(password)
        self.LOGIN_BUTTON.click()
        return self  # Return self or the next page if needed

    def logout(self):
        self.log.info(f"Logging out")
        self.LOGOUT_BUTTON.click()

    def get_error_message(self):
        return self.ERROR_MESSAGE.text_content()

    def is_error_visible(self):
        return self.ERROR_MESSAGE.is_visible()
