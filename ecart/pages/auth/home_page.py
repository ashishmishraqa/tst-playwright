from pages.auth.login_page import LoginPage
from pages.base_page import BasePage
from pages.product.product_page import ProductPage
from pages.auth.register_page import RegisterPage
from utilities.logger import get_logger


class HomePage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)

        # Locators
        self.MY_ACCOUNT = page.get_by_title('My Account')
        self.LOGIN = page.get_by_role('link', name='Login')
        self.REGISTER = page.get_by_role('link', name='Register')
        self.LOGIN_HEADING = "//h2[text()='Login to your account']"
        self.SEARCH = page.get_by_role('textbox', name='Search')
        self.WEBSITE_HEADING = "img[src='/static/images/home/logo.png'][alt='Website for automation practice']"
        self.ALL_LINKS = "a[href]"
        self.SEARCH_BUTTON = '.fa.fa-search'

    # ---------------------------
    # Actions
    # ---------------------------
    def navigate_to_home(self, url):
        self.log.info(f"Opening home page: {url}")
        self.go_to(url)

    def click_login(self):
        self.log.info("Clicking on login link")
        self.MY_ACCOUNT.click()
        self.LOGIN.click()
        return LoginPage(self.page)

    def click_register(self):
        self.log.info("Clicking on register link")
        self.MY_ACCOUNT.click()
        self.REGISTER.click()
        return RegisterPage(self.page)

    # ---------------------------
    # Getters
    # ---------------------------
    def get_home_title(self):
        return self.get_title()

    def get_login_heading(self):
        return self.page.locator(self.LOGIN_HEADING)

    def get_website_heading(self):
        return self.page.locator(self.WEBSITE_HEADING)

    def get_all_links(self):
        self.log.info("Getting all links on the page")
        return self.page.locator(self.ALL_LINKS)

    def get_all_links_count(self):
        count = self.get_all_links().count()
        self.log.info(f"Total links found on home page: {count}")
        return count

    def search_item(self, search_item):
        self.log.info("Searching item")
        self.SEARCH.fill(search_item)
        self.log.info("Searching item entered in the field")
        self.click(self.SEARCH_BUTTON)
        return ProductPage(self.page)
