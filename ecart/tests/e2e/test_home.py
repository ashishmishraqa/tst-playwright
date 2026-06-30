import pytest
from tests.test_base import BaseTest
from pages.auth.home_page import HomePage
from configs.settings import TestData
from playwright.sync_api import expect
from utilities.logger import get_logger


class TestHome(BaseTest):
    log = get_logger(__name__)

    @pytest.mark.smoke
    def test_verify_title(self, page):
        """
        Verify: Verify the title of the home page
        """
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        self.log.info(f"Page title: {home.get_home_title()}")
        expect(page).to_have_title(TestData.HOME_PAGE_TITLE)

    @pytest.mark.smoke
    def test_clicking_on_login(self, page):
        """
        Verify: Clicking on login button
        """
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        home.click_login()
        self.log.info("my account link clicked")
        expect(page).to_have_title(TestData.LOGIN_PAGE_TITLE)

    @pytest.mark.regression
    def test_count_all_links(self, page):
        """
        Verify: Count all the links present on the home page
        """
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        links_count = home.get_all_links_count()
        self.log.info(f"Total number of links found: {links_count}")
        # Assert that the count is greater than 0
        assert links_count > 0, f"Expected links count to be greater than 0, but found {links_count}"
        self.log.info(f"Test passed: Found {links_count} links on the home page")



    @pytest.mark.parametrize("products", ['macbook', 'iphone', 'canon','testing'],
                             ids=['search products','search products','search products','Negative scenario'])
    def test_item_search(self, page, products):
        """
        Verify: Item search for multiple products
        """
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)

        # search for the items
        home.search_item(products)

        # sort assertion, Use expect() with built-in retry: retries every 100ms for 30s
        expect(page).to_have_title(f'Search - {products}')

        # hard assertion, fail the test if search page is not visible
        heading = page.get_by_role('heading', name=f'Search - {products}', level=1)
        expect(heading).to_have_text(f'Search - {products}')
        self.log.info(f"Search passed for {products} and title: {page.title()}")




