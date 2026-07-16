from playwright.sync_api import expect
from locators.login_page_locators import LoginPageLocators
from ecart.pages.auth.logout_page import LogoutPage
from ecart.pages.base_page import BasePage
from ecart.pages.user.account_page import AccountPage
from ecart.utilities.logger import get_logger

class LoginPage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)


    @property
    def user_name_field(self):
        return self.page.get_by_role('textbox', name=LoginPageLocators.USERNAME_FIELD)

    @property
    def password_field(self):
        return self.page.get_by_role('textbox', name=LoginPageLocators.PASSWORD_FIELD)

    @property
    def login_button(self):
        return self.page.get_by_role('button', name=LoginPageLocators.LOGIN_BUTTON)

    @property
    def logout_button(self):
        return self.page.locator(LoginPageLocators.LOGOUT_LINK).get_by_role('link', name='Logout')

    @property
    def error_message(self):
        return self.page.locator('.alert-danger')  # Assuming error messages are in alert-danger


    def navigate_to_login_page(self, url):
        self.log.info(f"Opening Login page: {url}")
        self.go_to(url)


    def login(self, username, password):
        self.log.info(f"Logging in with username: {username}")
        self.enter_text(self.user_name_field, username)
        self.enter_text(self.password_field, password)
        self.click_on(self.login_button)
        return AccountPage(self.page)

    def click_on_logout(self):
        self.log.info("User is clicking on Log out button")
        self.click_on(self.logout_button)
        return LogoutPage(self.page)


    def expect_no_error_message(self):
        self.log.info("Checking if error message is not visible")
        expect(self.error_message).not_to_be_visible(timeout=5000)

    def verify_lockout_error(self):
        self.log.info("Get the error message appeared after the login")
        expect(self.error_message).to_contain_text("exceeded allowed number of login attempts")
