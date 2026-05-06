from pages.base_page import BasePage
from utilities import logger


class ProductPage(BasePage):

    log = logger.get_logger(__name__)

    def get_product_title(self):
        return self.get_title()


    def add_item_to_cart(self):
        self.page.locator('.fa.fa-shopping-cart').click()

    def verify_cart(self):
        self.page.locator('#cart-total').text_content()

    def click_checkout(self):
        self.page.get_by_text('Checkout', exact=True).click()