from pages.auth.logout_page import LogoutPage
from pages.base_page import BasePage
from pages.user.account_page import AccountPage
from utilities.logger import get_logger

class LoginPage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)

        # Locators for OpenCart
        self.USERNAME = page.get_by_role('textbox', name='E-Mail Address')
        self.PASSWORD = page.get_by_role('textbox', name='Password')
        self.LOGIN_BUTTON = page.get_by_role('button', name='Login')
        self.LOGOUT_BUTTON = page.locator('#column-right').get_by_role('link', name='Logout')
        self.ERROR_MESSAGE = page.locator('.alert-danger')  # Assuming error messages are in alert-danger

    def navigate_to_login_page(self, url):
        self.log.info(f"Opening Login page: {url}")
        self.go_to(url)


    def login(self, username, password):
        self.log.info(f"Logging in with username: {username}")
        self.enter_text(self.USERNAME, username)
        self.enter_text(self.PASSWORD, password)
        self.click_on(self.LOGIN_BUTTON)
        return AccountPage(self.page)

    def logout(self):
        self.log.info("Logging out")
        self.click_on(self.LOGOUT_BUTTON)
        return LogoutPage(self.page)

