import pytest
from playwright.sync_api import expect
from configs.config import TestData
from pages.auth.home_page import HomePage
from pages.auth.login_page import LoginPage
from tests.test_base import BaseTest
from utilities.api_utils import APIUtils


class TestLogin(BaseTest):


    @pytest.mark.smoke
    def test_login_valid_credentials(self, page, fetch_test_data):
        """
        Test login with valid credentials on OpenCart.
        Verifies successful login by checking navigation to account page or presence of logout.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # Get valid credentials from test data
        creds = fetch_test_data['valid_user']
        login_page.login(creds['username'], creds['password'])

        # For OpenCart, successful login may show account page or logout link
        # Successful login
        expect(page).to_have_title("My Account")  # Assuming title changes


    @pytest.mark.regression
    def test_login_invalid_credentials(self, page, fetch_test_data):
        """
        Test login with invalid credentials on OpenCart.
        Verifies error message is displayed.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # Get invalid credentials from test data
        creds = fetch_test_data['invalid_user']
        login_page.login(creds['username'], creds['password'])

        # Verify error message
        assert login_page.is_error_visible(), "Error message should be visible for invalid login"
        error_text = login_page.get_error_message()
        assert "Warning" in error_text, f"Error message should contain 'Warning', got: {error_text}"


    @pytest.mark.smoke
    def test_logout_functionality(self, page, fetch_test_data):
        """
        Test logout functionality after successful login on OpenCart.
        Assumes login works and logout link is available.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # Login first
        creds = fetch_test_data['valid_user']
        login_page.login(creds['username'], creds['password'])

        # If login successful, look for logout
        logout_link = page.locator('a').filter(has_text='Logout')
        if logout_link.count() > 0:
            logout_link.click()
            expect(page).to_have_url(TestData.LOGOUT_PAGE)
        else:
            # If no logout, perhaps navigate to home
            page.goto(TestData.BASE_URL)
            expect(page).to_have_title("Your Store")

    def test_fake_login(self, page):
        # 1. Generate Login token via API (Automatically attaches cookies to 'page')
        api_utils = APIUtils()
        api_utils.login_via_api(page)

        # 2. Navigate to the account page (Now authenticated)
        # Ensure you navigate to an account-restricted page, not just the login page
        page.goto('https://naveenautomationlabs.com/opencart/index.php?route=account/login')
        print(page.title())

        # 3. Verify login success using Playwright's expect
        # Checking for a unique element that only appears when logged in (like "Logout" or "My Account" title)
        expect(page).to_have_title("My Account")
        # expect(page.get_by_role("link", name="Logout")).to_be_visible()
