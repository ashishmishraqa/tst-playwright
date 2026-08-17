from playwright.sync_api import expect

from ecart.pages.base_page import BasePage
from ecart.utilities.logger import get_logger
from ecart.pages.user.newsletter_page import Newsletter


class AccountPage(BasePage):

    log = get_logger(__name__)

    def __init__(self, page):
        super().__init__(page)

    @property
    def newsletter_link(self):
        return self.page.get_by_role("link", name="Subscribe / unsubscribe to newsletter", exact=True)

    @property
    def success_message(self):
        return self.page.locator('.fa.fa-check-circle')


    def click_on_newsletter(self):
        self.click_on(self.newsletter_link)
        return Newsletter(self.page)

    def verify_successful_subscription(self):
        expect(self.success_message).to_be_visible()
        self.log.info('Successful newsletter subscription verified.')