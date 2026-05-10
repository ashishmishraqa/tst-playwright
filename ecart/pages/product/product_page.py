from pydantic.v1.utils import sequence_like

import pages
from pages.base_page import BasePage
from utilities import logger


class ProductPage(BasePage):

    def __init__(self,page):
        super().__init__(page)

        # locator
        self.BUTTON_ADD_TO_CART = page.locator('.row')
        self.CART_TOTAL = page.locator('#cart-total')
        self.BUTTON_CHECKOUT = page.locator('//strong[normalize-space()="Checkout"]')

    log = logger.get_logger(__name__)

    def get_product_title(self):
        return self.get_title()

    def add_item_to_cart(self):
        seq= 0
        for i in range(self.BUTTON_ADD_TO_CART.count()):
             if self.BUTTON_ADD_TO_CART.nth(i).get_by_role('link',name='MacBook').get_by_text("MacBook", exact=True).is_visible():
                 seq= i
                 break
        self.BUTTON_ADD_TO_CART.nth(seq).get_by_text('Add to Cart', exact=True).nth(seq).click()


    def verify_cart(self):
        return self.CART_TOTAL.text_content()

    def click_checkout(self):
        self.CART_TOTAL.click()
        self.BUTTON_CHECKOUT.click()
        self.log.info(f"Checkout successful")