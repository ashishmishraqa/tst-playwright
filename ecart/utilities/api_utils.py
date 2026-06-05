import logging
from urllib import request

import pytest
import requests
from playwright.sync_api import Playwright
from pytest_playwright.pytest_playwright import playwright

from configs.config import TestData
from utilities import faker_helper
from utilities.logger import get_logger




class APIUtils:

    log = get_logger(__name__)

    def get_login_token(self, playwright: Playwright):
        api_request = playwright.request.new_context(base_url='https://rahulshettyacademy.com')
        user_payload = {'userEmail': "demo@playwright.com", 'userPassword': "Qwe@1234"}
        login_response = api_request.post('/api/ecom/auth/login',data = user_payload,
                                          headers={'content-type':'application/json'})
        assert login_response.ok
        return login_response.json()['token']

    def login_via_api(self, page, fetch_test_data):
        """
        Login via form-based API endpoint and properly handle session cookies.

        Key Points:
        - OpenCart login expects multipart/form-data (not URL-encoded)
        - UI login sends: Content-Type: multipart/form-data; boundary=...
        - API login must match this format exactly
        - page.request automatically follows redirects BUT cookies need manual handling
        - Must extract Set-Cookie headers and add to context
        """
        api_request = page.request

        # Use multipart form data to match UI behavior
        # Create form data that matches what the browser sends
        form_data = {
            'email': fetch_test_data['valid_user']['username'],
            'password': fetch_test_data['valid_user']['password']
        }

        # Make login request with multipart data (matches UI behavior)
        # This sends multipart/form-data like the browser
        login_response = api_request.post(TestData.LOGIN_PAGE,multipart=form_data)

        self.log.debug(f"Login Response Status: {login_response.status}")
        self.log.debug(f"Login Response Headers: {login_response.headers}")

        # Check response body for error messages
        response_text = login_response.text()
        self.log.debug(f"Login Response Body (first 500 chars): {response_text[:500]}")

        # Look for common error indicators
        if "Warning" in response_text or "error" in response_text.lower():
            self.log.debug("⚠️  LOGIN FAILED: Error message found in response")
        elif "My Account" in response_text or "account/account" in response_text:
            self.log.info("LOGIN SUCCESS: Account page content found")
        else:
            self.log.debug("LOGIN STATUS UNKNOWN: No clear success/error indicators")

        # Extract session cookie from Set-Cookie header in response
        set_cookie_header = login_response.headers.get('set-cookie', '')
        self.log.info(f"Set-Cookie Header: {set_cookie_header}")

        # After request, check all cookies in the page context
        # page.request automatically adds cookies from responses to the context
        cookies = page.context.cookies()
        return cookies



    def create_order(self, playwright: Playwright):
        token = self.get_login_token(playwright)
        api_request = playwright.request.new_context(base_url='https://rahulshettyacademy.com')
        response = api_request.get('/api/ecom/product/get-product-detail/68a961459320a140fe1ca57a',
                                    headers={'Authorization':token})
        print(response.status)
        assert response.ok
        print(f'product found successfully is : {response.json()['data']['productName']}')


    def create_orders(self,playwright:Playwright):
        api_request = playwright.request.new_context(base_url='https://rahulshettyacademy.com')
        response = api_request.get('/api/ecom/product/get-product-list',)







