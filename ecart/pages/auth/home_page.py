from playwright.sync_api import expect, Locator
from ecart.pages.auth.login_page import LoginPage
from ecart.pages.base_page import BasePage
from ecart.pages.product.product_page import ProductPage
from ecart.pages.auth.register_page import RegisterPage
from ecart.utilities.logger import get_logger
from locators.home_page_locators import HomePageLocators


class HomePage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)

    # ---------------------------
    # Locators (as @property for freshness)
    # ---------------------------
    @property
    def my_account_button(self) -> Locator:
        return self.page.get_by_title(HomePageLocators.MY_ACCOUNT_LINK)

    @property
    def login_link(self) -> Locator:
        return self.page.get_by_role('link', name=HomePageLocators.LOGIN_LINK)

    @property
    def register_link(self) -> Locator:
        return self.page.get_by_role('link', name=HomePageLocators.REGISTER_LINK)

    @property
    def search_box(self) -> Locator:
        return self.page.get_by_role('textbox', name=HomePageLocators.SEARCH_BOX)


    @property
    def search_button(self) -> Locator:
        return self.page.locator(HomePageLocators.SEARCH_BUTTON)

    @property
    def all_links(self) -> Locator:
        return self.page.locator(HomePageLocators.ALL_LINKS)


    # ---------------------------
    # Actions (page interactions only)
    # ---------------------------
    def navigate_to_home(self, url: str) -> None:
        self.log.info(f"Navigating to home page: {url}")
        self.go_to(url)

    def click_login(self) -> LoginPage:
        """Navigate to login page via dropdown."""
        self.log.info("Navigating to login page")
        self.click_on(self.my_account_button)
        self.login_link.wait_for(state="visible", timeout=5000)
        self.click_on(self.login_link)
        return LoginPage(self.page)

    def click_register(self) -> RegisterPage:
        """Navigate to registration page via dropdown."""
        self.log.info("Navigating to registration page")
        self.click_on(self.my_account_button)
        self.register_link.wait_for(state="visible", timeout=5000)
        self.click_on(self.register_link)
        return RegisterPage(self.page)


    def search_product(self, product_name: str) -> ProductPage:
        """Search for a product and return product page object."""
        self.log.info(f"Searching for product: '{product_name}'")
        self.enter_text(self.search_box, product_name)
        self.click_on(self.search_button)
        return ProductPage(self.page)


    # ---------------------------
    # Data Getters (optional—only if tests need them)
    # ---------------------------
    def get_links_count(self) -> int:
        """Return count of all links on homepage."""
        count = self.all_links.count()
        self.log.debug(f"Total links on homepage: {count}")
        return count


