from pages.auth.login_page import LoginPage
from pages.base_page import BasePage
from pages.product.product_page import ProductPage
from pages.register_page import RegisterPage
from utilities.logger import get_logger


class HomePage(BasePage):

    log = get_logger(__name__)


    # Locators
    MY_ACCOUNT = "'link', name='Login'"
    LOGIN_HEADING = "//h2[text()='Login to your account']"
    WEBSITE_HEADING = "img[src='/static/images/home/logo.png'][alt='Website for automation practice']"
    ALL_LINKS = "a[href]"
    SEARCH_BUTTON = '.fa.fa-search'

    def __init__(self, page):
        super().__init__(page)

    # ---------------------------
    # Actions
    # ---------------------------
    def navigate_to_home(self, url):
        self.log.info(f"Opening home page: {url}")
        self.go_to(url)

    def click_login(self):
        self.log.info("Clicking on login link")
        account_link = self.page.get_by_title('My Account')
        self.click(account_link)
        link = self.page.get_by_role('link', name='Login')
        self.click(link)
        return LoginPage(self.page)

    def click_register(self):
        self.log.info("Clicking on register link")
        account_link = self.page.get_by_title('My Account')
        self.click(account_link)
        link = self.page.get_by_role('link', name='Register')
        self.click(link)
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
        self.page.get_by_role('textbox', name='Search').fill(search_item)
        self.log.info("Searching item entered in the field")
        self.click(self.SEARCH_BUTTON)
        return ProductPage

