from playwright.sync_api import expect
from ecart.pages.base_page import BasePage
from ecart.utilities import logger


class ProductPage(BasePage):

    def __init__(self,page):
        super().__init__(page)

    @property
    def add_to_cart_button(self):
        return self.page.get_by_role('button', name='Add to Cart')

    @property
    def cart_total(self):
        return self.page.locator('#cart-total')

    @property
    def checkout_button(self):
        return self.page.locator('//strong[normalize-space()="Checkout"]')

    @property
    def alert_item_added_to_cart(self):
        return self.page.locator('.alert.alert-success.alert-dismissible')

    log = logger.get_logger(__name__)

    def _get_product_container(self, product):
        """private repetitive method to get the product container"""
        return self.page.locator(".product-thumb", has=self.page.get_by_text(product,exact=True))


    def add_item_to_cart(self, product):
        """finding the product container on the page and adds it to the cart"""
        product_container = self._get_product_container(product)
        self.click_on(product_container.locator(self.add_to_cart_button))
        expect(self.alert_item_added_to_cart).to_be_visible()
        self.log.info(f'{product} added to cart')


    def return_total_cart_amount(self):
        """finding the total amount on the page and returns the total amount"""
        cart_total = self.cart_total.get_by_text('1 item(s)').text_content()
        self.log.info(f"Cart total amount: {cart_total}")
        return cart_total


    def click_checkout(self):
        self.click_on(self.cart_total)
        self.click_on(self.checkout_button)
        self.log.info("user clicked on checkout")


    def expect_product_on_search_page(self, product):
        """
        Finds the product container on the page and validates if it is visible. If the product is not found, an assertion error will be raised.
        """
        # 1. find the parent of the product button that contains the product name
        product_container = self._get_product_container(product)
        self.log.info(f'{product} found on the page total {product_container.count()} times')

        # 2. Validate if product container is visible
        expect(product_container).to_be_visible()

