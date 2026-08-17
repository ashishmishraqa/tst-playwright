import pytest
from playwright.sync_api import expect
from ecart.configs.settings import TestData


class TestWishList:


    @pytest.mark.smoke
    def test_user_login_with_authenticates_session(self, authenticated_page):
        """
        Test user login using an authenticated session via API.
        This test demonstrates logging in via API, preserving session cookies, and verifying access to the account page.
        """

        # 1. Navigate to account page (uses cookies from page.context)
        authenticated_page.goto(TestData.USER_LOGGED_IN_PAGE, wait_until="domcontentloaded")

        # 2. Verify login success
        expect(authenticated_page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)

