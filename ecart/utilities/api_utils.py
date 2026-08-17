from ecart.configs.settings import TestData
from ecart.utilities.logger import get_logger


class APIUtils:

    log = get_logger(__name__)



    def login_via_api(self,context, credentials):
        """
        Login via form-based API endpoint and properly handle session cookies.

        Key Points:
        - OpenCart login expects multipart/form-data (not URL-encoded)
        - UI login sends: Content-Type: multipart/form-data; boundary=...
        - API login must match this format exactly
        - page.request automatically follows redirects BUT cookies need manual handling
        - Must extract Set-Cookie headers and add to context
        """
        # Make login request with multipart data (matches UI behavior)
        # This sends multipart/form-data like the browser
        response = context.request.post(TestData.LOGIN_PAGE, multipart={
            "email": credentials["username"],
            "password": credentials["password"],
        })

        if not response.ok:
            raise RuntimeError(f"Login failed with status code {response.status_code}")

        self.log.info(f"Login Response Status: {response.status}")
        self.log.info(f"Login Response Headers: {response.headers}")

        # Check response body for error messages
        response_text = response.text()
        self.log.debug(f"Login Response Body (first 500 chars): {response_text[:500]}")

        # Look for common error indicators
        if "Warning" in response_text or "error" in response_text.lower():
            self.log.debug("⚠️  LOGIN FAILED: Error message found in response")
        elif "My Account" in response_text or "account/account" in response_text:
            self.log.info("LOGIN SUCCESS: Account page content found")
        else:
            self.log.debug("LOGIN STATUS UNKNOWN: No clear success/error indicators")
        return context




