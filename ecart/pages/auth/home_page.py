from pages.base_page import BasePage
from utilities.logger import get_logger


class HomePage(BasePage):

    log = get_logger(__name__)


    # Locators
    LOGIN_HEADING = "//h2[text()='Login to your account']"
    WEBSITE_HEADING = "img[src='/static/images/home/logo.png'][alt='Website for automation practice']"
    ALL_LINKS = "a[href]"

    def __init__(self, page):
        super().__init__(page)
        # self.log = get_logger(__name__)

    # ---------------------------
    # Actions
    # ---------------------------
    def navigate_to_home(self, url):
        self.log.info(f"Opening home page: {url}")
        self.go_to(url)

    def click_my_account_link(self):
        self.log.info("Clicking on login link")
        login_link = self.page.get_by_role("link", name="Login")
        self.click(login_link)

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
