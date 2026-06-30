import time
import pytest
from playwright.sync_api import expect
from configs.settings import TestData
from pages.auth.home_page import HomePage
from tests.test_base import BaseTest
from utilities.logger import get_logger


class TestCheckout(BaseTest):


    log = get_logger(__name__)

    @pytest.mark.parametrize("product",['MacBook'])
    def test_checkout(self, page, product):
        """
        Test checkout functionality for product as macbook
        """
        # launch the app
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        assert home.get_home_title() == TestData.HOME_PAGE_TITLE , 'Error ! Home page is not opened'
        product_page = home.search_item(product)
        product_search_page = f'Search - {product}'
        time.sleep(3)
        assert home.get_home_title() == product_search_page, 'Error ! product page is not opened'

        seq = product_page.get_product_sequence_if_visible(product)
        time.sleep(3)
        if seq:
            self.log.info(f'{product} found on the sequence: {seq}')
            product_page.add_item_to_cart(page, seq, product)
        else:
            pytest.fail(f'Error! sequence returned as {seq}, so could not find product {product}')

        cart_total = eval(f'TestData.CART_TOTAL_{product.upper()}')
        print(f'CART TOTAL: {cart_total}')
        assert product_page.return_total_cart_amount() == cart_total, f'Error! {product} amount is not matching as expected'
        product_page.click_checkout()
