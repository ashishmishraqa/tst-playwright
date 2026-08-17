import pytest
from ecart.configs.settings import TestData
from ecart.tests.test_base import BaseTest
from playwright.sync_api import expect


class TestLogin(BaseTest):

    @pytest.mark.smoke
    def test_login_valid_credentials(self, login_page, credentials):
        """
        Test login with valid credentials on OpenCart.
        Verifies successful login by checking navigation to account page or presence of logout.
        """
        # 1. Get the login page from the fixture and login with valid credentials
        login_page.login(credentials["username"], credentials["password"])

        # 2. Ensure no error message is visible
        login_page.expect_no_error_message()

        # 3. Validate login is successful and Account page is loaded
        expect(login_page.page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)

    @pytest.mark.smoke
    def test_login_invalid_credentials(self, login_page, fetch_test_data):
        """
        Test login with invalid credentials on OpenCart.
        Verifies error message is displayed.
        """
        # 1. Get the login page from the fixture and login with invalid credentials
        credentials = fetch_test_data["invalid_user"]
        login_page.login(credentials["username"], credentials["password"])

        # 2. Verify error message
        login_page.verify_lockout_error()

    @pytest.mark.smoke
    def test_logout_functionality(self, login_page, credentials):
        """
        Test logout functionality after successful login on OpenCart.
        Assumes login works and logout link is available.
        """
        # 1. Get the login page from the fixture and login with valid credentials
        login_page.login(credentials["username"], credentials["password"])

        # 2. Ensure no error appears
        login_page.expect_no_error_message()

        # 3. Verify login success
        expect(login_page.page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)

        # 4. logout & verify the logout page is displayed
        logout_page = login_page.click_on_logout()
        expect(login_page.page).to_have_url(TestData.LOGOUT_PAGE)
        logout_page.verify_logout_text()
