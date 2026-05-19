import time
import pytest
from playwright.sync_api import expect
from configs.config import TestData
from pages.auth.home_page import HomePage
from tests.test_base import BaseTest
from utilities.logger import get_logger


class TestCheckout(BaseTest):


    log = get_logger(__name__)

    @pytest.mark.smoke
    def test_checkout(self, page):
        """
        Test checkout functionality after successful login
        """
        # launch the app
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        self.log.info(f"Page title: {home.get_home_title()}")
        expect(page).to_have_title('Your Store')
        product_page = home.search_item(TestData.PRODUCT)
        expect(page).to_have_title('Search - macbook')
        product_page.add_item_to_cart()
        time.sleep(2)  # Wait for the cart to update
        amount = product_page.verify_cart()
        self.log.info(f"Amount of product added: {amount}")
        product_page.click_checkout()
