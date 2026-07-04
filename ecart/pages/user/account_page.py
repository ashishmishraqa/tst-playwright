from pages.base_page import BasePage
from utilities.logger import get_logger


class AccountPage(BasePage):
    
    log = get_logger(__name__)
    
    def __init__(self,page):
        super().__init__(page)


        