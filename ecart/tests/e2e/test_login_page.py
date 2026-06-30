import pytest
from playwright.sync_api import expect
from configs.settings import TestData
from pages.auth.login_page import LoginPage
from tests.test_base import BaseTest
from utilities.api_utils import APIUtils


class TestLogin(BaseTest):


    @pytest.mark.smoke
    def test_login_valid_credentials(self, page, credentials):
        """
        Test login with valid credentials on OpenCart.
        Verifies successful login by checking navigation to account page or presence of logout.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)
        login_page.login(credentials['username'], credentials['password'])

        # After login attempt if any error appears: fail the test, else: assert the title of user home page
        if login_page.is_error_visible():
            error_text = login_page.get_error_message()
            pytest.fail(f"Login Failed:{error_text}")
        expect(page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)  # Assuming title changes


    @pytest.mark.smoke
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
        assert login_page.is_error_visible(), "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour."
        error_text = login_page.get_error_message()
        assert "Warning" in error_text, f"Error message should contain 'Warning', got: {error_text}"


    @pytest.mark.smoke
    def test_logout_functionality(self, page, credentials):
        """
        Test logout functionality after successful login on OpenCart.
        Assumes login works and logout link is available.
        """
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # Login first
        login_page.login(credentials['username'], credentials['password'])
        # Verify error message
        if login_page.is_error_visible():
            error_text = login_page.get_error_message()
            pytest.fail(f"Login Failed:{error_text}")
        expect(page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)  # Verify login success

        # If login successful, look for logout
        login_page.logout()
        expect(page).to_have_url(TestData.LOGOUT_PAGE)



    @pytest.mark.smoke
    def test_fake_login(self, page, credentials):
        """
        Test login via API - Hybrid approach.

        Why this works:
        - Network tab shows: POST returns 302 redirect + Set-Cookie (OCSESSID)
        - page.request uses same context as page
        - Cookies from 302 response automatically added to page.context
        - After login, navigate to authenticated page with valid session

        Key learnings:
        - 302 != failure, it's success with redirect
        - Form-based login sets cookies in response headers
        - page.request auto-handles cookies for page context
        - Must ensure page.context has cookies before navigation
        """
        api_utils = APIUtils()

        # 1. Login via API (POST to form endpoint)
        # This returns 302 + OCSESSID cookie
        api_utils.login_via_api(page,credentials)
        # print(f"[DEBUG] Login complete. Cookies: {cookies}")

        # 2. Navigate to account page (uses cookies from page.context)
        page.goto(TestData.USER_LOGGED_IN_PAGE, wait_until='domcontentloaded')

        # 3. Verify login success
        expect(page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)
