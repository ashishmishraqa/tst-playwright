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
        # 1. launch the login page of the app
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # 2. Enter the credentials
        print(credentials)
        login_page.login(credentials['username'], credentials['password'])

        # 3. Ensure no error message is visible
        expect(login_page.ERROR_MESSAGE, 'Error ! after entering the credentials ').not_to_be_visible()

        # 4. Validate login is successful and Account page is loaded
        expect(page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)


    @pytest.mark.smoke
    def test_login_invalid_credentials(self, page, fetch_test_data):
        """
        Test login with invalid credentials on OpenCart.
        Verifies error message is displayed.
        """
        # 1. Launch the login page
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # 2. Get invalid credentials from test data
        creds = fetch_test_data['invalid_user']
        login_page.login(creds['username'], creds['password'])

        # 3. Verify error message
        expect(login_page.ERROR_MESSAGE, "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour.").to_be_visible()


    @pytest.mark.smoke
    def test_logout_functionality(self, page, credentials):
        """
        Test logout functionality after successful login on OpenCart.
        Assumes login works and logout link is available.
        """
        # 1. Launch the login page
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(TestData.LOGIN_PAGE)

        # 2. Login with valid credentials
        login_page.login(credentials['username'], credentials['password'])

        # 3. Ensure no error appears
        expect(login_page.ERROR_MESSAGE, 'Error ! after entering the credentials ').not_to_be_visible()

        # 4. Verify login success
        expect(page).to_have_title(TestData.ACCOUNT_PAGE_TITLE)

        # 5. logout & verify the logout page is displayed
        logout_page = login_page.logout()
        expect(page).to_have_url(TestData.LOGOUT_PAGE)
        expect(logout_page.LOGOUT_TEXT, 'Error! logout page could not be found').to_be_visible()



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
