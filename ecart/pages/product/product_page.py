from playwright.sync_api import expect

from pages.base_page import BasePage
from utilities import logger


class ProductPage(BasePage):

    def __init__(self,page):
        super().__init__(page)

        # locator
        self.BUTTON_ADD_TO_CART = page.get_by_role('button',name='Add to Cart')
        self.CART_TOTAL = page.locator('#cart-total')
        self.BUTTON_CHECKOUT = page.locator('//strong[normalize-space()="Checkout"]')
        self.alert_item_added_to_cart = page.locator('.alert.alert-success.alert-dismissible')

    log = logger.get_logger(__name__)

    def add_item_to_cart(self, product):
        product_container = self.page.locator(".product-thumb", has=self.page.get_by_text(product,exact=True))
        self.click_on(product_container.locator(self.BUTTON_ADD_TO_CART))
        expect(self.alert_item_added_to_cart).to_be_visible()
        self.log.info(f'{product} added to cart')



    def return_total_cart_amount(self):
        cart_total = self.CART_TOTAL.get_by_text('1 item(s)').text_content()
        self.log.info(f"Cart total amount: {cart_total}")
        return cart_total

    def click_checkout(self):
        self.click_on(self.CART_TOTAL)
        self.click_on(self.BUTTON_CHECKOUT)
        self.log.info("user clicked on checkout")

    """
    method to check if the product is available on after search
    """
    def validate_if_product_found(self, product):
        """
        Finds the product container on the page and validates if it is visible. If the product is not found, an assertion error will be raised.
        """
        # 1. find the parent of the product button that contains the product name
        product_container = self.page.locator(".product-thumb", has=self.page.get_by_text(product,exact=True))
        self.log.info(f'{product} found on the page total {product_container.count()} times')

        # 2. Validate if product container is visible
        expect(product_container).to_be_visible()

