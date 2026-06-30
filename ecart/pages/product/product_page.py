from pages.base_page import BasePage
from utilities import logger


class ProductPage(BasePage):

    def __init__(self,page):
        super().__init__(page)

        # locator
        self.BUTTON_ADD_TO_CART = page.locator('.row')
        self.CART_TOTAL = page.locator('#cart-total')
        self.BUTTON_CHECKOUT = page.locator('//strong[normalize-space()="Checkout"]')
        self.items_thumb = page.locator('.product-thumb', has=page.get_by_role('link',name='MacBook'))

    log = logger.get_logger(__name__)

    def get_product_title(self):
        return self.get_title()

    def add_item_to_cart(self,page,seq,product):
        product_container = page.locator(".product-thumb").get_by_role('link', name=product).nth(seq)
        print('container found')

        add_to_cart_btn = product_container.get_by_role('button',name='add_to_cart')
        print('add to cart button found')

        add_to_cart_btn.click()
        # self.BUTTON_ADD_TO_CART.nth(seq).get_by_text('Adddd to Cart', exact=True).nth(seq).click()


    def return_total_cart_amount(self):
        return self.CART_TOTAL.text_content()

    def click_checkout(self):
        self.click_on(self.CART_TOTAL)
        self.click_on(self.BUTTON_CHECKOUT)
        self.log.info("user clicked on checkout")

    """
    method to check if the product is available on after search
    """
    def get_product_sequence_if_visible(self, product):
        """
            Finds the index of a product's 'Add to Cart' button based on the product name.
            """
        # 1. Iterate through all available product buttons
        for seq in range(self.BUTTON_ADD_TO_CART.count()):
            # 2. Scope the locator dynamically using the passed product_name
            product_locator = self.BUTTON_ADD_TO_CART.nth(seq).get_by_role(
                'link', name=product).get_by_text(product, exact=True)

            # 3. Check visibility
            if product_locator.is_visible():
                return seq

        # 4. Only return False if the loop finishes without finding the item
        return False

