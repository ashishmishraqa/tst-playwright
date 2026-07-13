
import pytest
from playwright.sync_api import expect
from configs.settings import TestData
from tests.test_base import BaseTest
from utilities.data_utils import fetch_products
from utilities.logger import get_logger


class TestCheckout(BaseTest):


    log = get_logger(__name__)


    """
    "fetch_products() returns a list of test data. Each item in that list is a dictionary representing one test case. 
    pytest.mark.parametrize iterates over the list and executes the test once per item. On each execution, 
    it passes one dictionary into the products parameter, allowing the same test logic to run against multiple 
    data sets without duplicating code."
    """
    @pytest.mark.smoke
    @pytest.mark.parametrize('products',fetch_products())
    def test_checkout(self, page, products, launch_home_page):
        """
        Test: Search a product, add to the cart and perform checkout
        """
        # 1. Validate home page is loaded
        expect(launch_home_page.page).to_have_title(TestData.HOME_PAGE_TITLE)

        # 2. Search for the product & validate if search page appears
        product_page = launch_home_page.search_product(products['product'])
        # expect(product_page.page).to_have_title(f'Search - {product}')

        # 3. Validate if product is found after search
        product_page.validate_if_product_found(products['product'])

        # 4. Add the product to cart & validate the cart total
        product_page.add_item_to_cart(products['product'])
        # time.sleep(3)

        # 5. validate the cart total
        assert product_page.return_total_cart_amount() == products['expected_price'], f'Error! {products['product']} amount is not matching as expected'

        # 6. Perform checkout & validate the result
        product_page.click_checkout()
