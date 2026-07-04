import pytest
from playwright.sync_api import expect
from configs.settings import TestData
from tests.test_base import BaseTest
from utilities.logger import get_logger


class TestCheckout(BaseTest):


    log = get_logger(__name__)

    @pytest.mark.smoke
    @pytest.mark.parametrize("product, expected_price",
                             [(   'MacBook', ' 1 item(s) - $602.00'),
                              ('iPhone', ' 1 item(s) - $123.20')])
    def test_checkout(self, page, product, expected_price, launch_home_page):
        """
        Test: Search a product, add to the cart and perform checkout
        """
        # 1. Validate home page is loaded
        expect(launch_home_page.page).to_have_title(TestData.HOME_PAGE_TITLE)

        # 2. Search for the product & validate if search page appears
        product_page = launch_home_page.search_product(product)
        # expect(product_page.page).to_have_title(f'Search - {product}')

        # 3. Validate if product is found after search
        product_page.validate_if_product_found(product)

        # 4. Add the product to cart & validate the cart total
        product_page.add_item_to_cart(product)

        # 5. validate the cart total
        assert product_page.return_total_cart_amount() == expected_price, f'Error! {product} amount is not matching as expected'

        # 6. Perform checkout & validate the result
        product_page.click_checkout()
