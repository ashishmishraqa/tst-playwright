from playwright.sync_api import Page
from pages.base_page import BasePage
from utilities.logger import get_logger


class Newsletter(BasePage):

    log = get_logger(__name__)

    def __init__(self, page: Page):
        super().__init__(page)


    @property
    def select_radio_button(self):
        return self.page.get_by_role("radio", name="Yes")

    @property
    def deselect_radio_button(self):
        return self.page.get_by_role("radio", name="No")

    @property
    def continue_button(self):
        return self.page.get_by_role('button', name='Continue')


    def click_yes_button(self):
        self.click_on(self.select_radio_button)
        self.log.info("Clicked on 'Yes' radio button")

    def click_continue_button(self):
        from pages.user.account_page import AccountPage
        self.click_on(self.continue_button)
        self.log.info("Clicked on 'Continue' radio button")
        return AccountPage(self.page)



