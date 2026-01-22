from tests.test_base import BaseTest
from pages.home_page import HomePage
from configs.config import TestData
from playwright.sync_api import expect
from utils.logger import get_logger


class TestHome(BaseTest):
    log = get_logger(__name__)

    def test_has_title(self, page):
        home = HomePage(page)

        home.navigate_to_home(TestData.BASE_URL)
        self.log.info(f"Page title: {home.get_home_title()}")
        expect(page).to_have_title("Automation Exercise")

    def test_get_started_link(self, page):
        home = HomePage(page)

        home.navigate_to_home(TestData.BASE_URL)
        home.click_login_link()
        self.log.info("Login link clicked")
        expect(home.get_login_heading()).to_be_visible()

    def test_website_heading_visible(self, page):
        home = HomePage(page)

        home.navigate_to_home(TestData.BASE_URL)
        self.log.info("Verifying 'Website for automation practice' heading is visible")
        expect(home.get_website_heading()).to_be_visible()

    def test_count_all_links(self, page):
        home = HomePage(page)

        home.navigate_to_home(TestData.BASE_URL)
        links_count = home.get_all_links_count()
        self.log.info(f"Total number of links found: {links_count}")

        # Assert that the count is greater than 0
        assert links_count > 0, f"Expected links count to be greater than 0, but found {links_count}"
        self.log.info(f"Test passed: Found {links_count} links on the home page")
