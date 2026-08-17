from ecart.pages.base_page import BasePage
from ecart.utilities.logger import get_logger


class Mp3PlayersPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    log = get_logger(__name__)


    @property
    def sort_by_dropdown(self):
        return self.page.get_by_label('Sort By:')

    @property
    def product_names_locator(self):
        return self.page.locator('.product-thumb .caption h4 a')

    @property
    def product_prices_locator(self):
        return self.page.locator('.price')

    def select_sorting_options(self, sort_option):
        self.log.info("Selecting sorting options from the dropdown")
        self.sort_by_dropdown.select_option(sort_option)
        self.page.wait_for_load_state('load')
        self.log.info("Clicked on 'Show All MP3 Players' link, wait to load the page")


    """fetch list of product names"""
    def get_product_names(self):
        # using list comprehension to store names of all the products in a list
        product_name_elements = [element.strip() for element in self.product_names_locator.all_inner_texts()]
        self.log.info(f"Fetched product names from the page: {product_name_elements}")
        return product_name_elements

    """fetch list of product prices"""
    def get_product_prices(self):
        product_prices = [price.strip() for price in self.product_prices_locator.all_inner_texts()]
        self.log.info(f"Fetched product prices from the page: {product_prices}")
        return product_prices


