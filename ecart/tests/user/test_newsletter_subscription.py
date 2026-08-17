import pytest
from ecart.configs.settings import TestData
from playwright.sync_api import expect
from pages.user.account_page import AccountPage


class TestNewsLetterSubscription:

    @pytest.mark.smoke
    def test_subscribe_newsletter(self, authenticated_page):
        """
        Test subscribe_newsletter functionality.
        """
        # 1. using fixture user is logged in, Make sure flow is on account page
        authenticated_page.goto(TestData.USER_LOGGED_IN_PAGE, wait_until="domcontentloaded")

        account_page = AccountPage(authenticated_page)

        expect(account_page.page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)

        # user click on newsletter link
        newsletter_page = account_page.click_on_newsletter()
        #
        # verify if newsletter page appears
        expect(newsletter_page.page).to_have_title(TestData.NEWSLETTER_PAGE_TITLE)
        #
        # # click on radio button - Yes
        # newsletter_page.click_yes_button()
        # subscribed_account_page = newsletter_page.click_continue_button()
        #
        # # verify the user lands on the account page again
        # expect(subscribed_account_page.page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)
        #
        # # verify text appears on account page
        # subscribed_account_page.verify_successful_subscription()
