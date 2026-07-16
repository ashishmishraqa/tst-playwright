import pytest
from ecart.tests.test_base import BaseTest
from ecart.configs.settings import TestData
from playwright.sync_api import expect
from ecart.utilities.logger import get_logger


class TestHome(BaseTest):
    log = get_logger(__name__)

    @pytest.mark.smoke
    def test_verify_home_page_title(self, home_page):
        """
        Verify: Home page loads with correct title
        """
        expect(home_page.page).to_have_title(TestData.HOME_PAGE_TITLE)
        self.log.info(f"✓ Home page title verified: {home_page.get_title()}")

    @pytest.mark.smoke
    def test_navigate_to_login_page(self, home_page):
        """
        Verify: Clicking on login button
        """
        home_page.click_login()
        self.log.info("Clicked on login button, waiting for login page to load")
        expect(home_page.page).to_have_title(TestData.LOGIN_PAGE_TITLE)
        self.log.info("Successfully navigated to login page and title verified")

    @pytest.mark.smoke
    def test_count_all_links(self, home_page):
        """
        Verify: Count all the links present on the home page
        """
        links_count = home_page.get_links_count()
        # Assert that the count is greater than 0
        assert links_count > 0, (
            f"Expected home page to have links, but found {links_count}. "
            "Page may not be fully loaded or selectors are incorrect.")
        self.log.info(f"Test passed: Found {links_count} links on the home page")


    @pytest.mark.smoke
    @pytest.mark.parametrize("products", ['macbook', 'iphone', 'canon','testing'],
                             ids=['search MacBook','search iPhone','search Canon','Negative scenario'])
    def test_item_search(self, home_page, products):
        """
        Verify: Item search for multiple products
        """
        # 1. search for the items
        home_page.search_product(products)

        # 2. sort assertion, Use expect() with built-in retry: retries every 100ms for 30s
        # Assert: soft assertion (retries for 30s)
        expected_title = f"Search - {products}"
        expect(home_page.page).to_have_title(expected_title)

        # 3. hard assertion, fail the test if search page is not visible
        heading = home_page.page.get_by_role('heading', name=f'Search - {products}', level=1)
        expect(heading).to_have_text(f'Search - {products}')
        self.log.info(f"✓ Search '{products}' | Title: {home_page.page.title()}")





