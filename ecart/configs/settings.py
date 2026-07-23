"""
This page stores all configurations and test data
"""

import os
from pathlib import Path

from dotenv import load_dotenv

"""
to load .env file irrespective of the method its invoke
"""
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


class TestData:
    BASE_URL = "https://naveenautomationlabs.com/opencart/"
    LOGIN_PAGE = (
        "https://naveenautomationlabs.com/opencart/index.php?route=account/login"
    )
    LOGOUT_PAGE = (
        "https://naveenautomationlabs.com/opencart/index.php?route=account/logout"
    )
    USER_LOGGED_IN_PAGE = (
        "https://naveenautomationlabs.com/opencart/index.php?route=account/account"
    )
    HOME_PAGE_TITLE = "Your Store"
    REGISTER_PAGE_URL = (
        "https://naveenautomationlabs.com/opencart/index.php?route=account/register"
    )
    REGISTER_PAGE_TITLE = "Register Account"
    LOGIN_PAGE_TITLE = "Account Login"
    ACCOUNT_PAGE_TITLE = "My Account"
    SUCCESS_REGISTRATION = "Your Account Has Been Created!"

    EXCEL_SHEET = "data.xlsx"
    SHEET_NAME = "registration"
    TEXT_EMPTY_CART = "0 item(s) - $0.00"
    CART_TOTAL_MACBOOK = "1 item(s) - $602.00"
    ITEMS_CAROUSEL = (
        "Harley Davidson",
        "Dell",
        "Disney",
        "Starbucks",
        "Nintendo",
        "NFL",
        "RedBull",
        "Sony",
        "Coca Cola",
        "Burger King",
        "Canon",
    )
    PRODUCT = "macbook"

    """
    Fetch required environment variables and raise an error if they are not set.
    """

    def get_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Required environment variable '{name}' is not set.")
        return value

    # in CI: fetched from GitHub action environment
    GO_REST_TOKEN = get_env("GO_REST_TOKEN")
    BASE_URL_API = get_env("BASE_URL_API")
