from playwright.sync_api import expect
from pages.auth.login_page import LoginPage
from pages.base_page import BasePage
from pages.product.product_page import ProductPage
from pages.auth.register_page import RegisterPage
from utilities.logger import get_logger


class HomePage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)

        # Locators as instance attribute
        self.MY_ACCOUNT = page.get_by_title('My Account')
        self.MY_ACCOUNT_BUTTON = page.get_by_role('link', name='My Account')
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
        self.log.info(f"Open home page: {url}")
        self.go_to(url)

    def click_login(self):
        self.log.info("clicking on login button from home page")
        self.click_on(self.MY_ACCOUNT)
        self.click_on(self.LOGIN)
        return LoginPage(self.page)

    def click_register(self):
        self.log.info("Open registration page from home")
        self.click_on(self.MY_ACCOUNT)
        self.click_on(self.REGISTER)
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
        return self.page.locator(self.ALL_LINKS)

    def get_all_links_count(self):
        count = self.get_all_links().count()
        return count

    def search_product(self, product):
        self.log.info(f"Search for product: {product}")
        self.enter_text(self.SEARCH, product)
        self.click_on(self.SEARCH_BUTTON)
        # create the Object
        product_page = ProductPage(self.page)
        # validate if Product page appears
        expect(product_page.page).to_have_title(f'Search - {product}')
        return product_page
