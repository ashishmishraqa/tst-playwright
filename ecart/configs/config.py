"""
This page stores all configurations and test data
"""
from utilities.secret_manager import SecretsManager
import os
from dotenv import load_dotenv

load_dotenv()

class TestData:
    BASE_URL = 'https://naveenautomationlabs.com/opencart/'
    LOGIN_PAGE = 'https://naveenautomationlabs.com/opencart/index.php?route=account/login'
    LOGOUT_PAGE = 'https://naveenautomationlabs.com/opencart/index.php?route=account/logout'
    USER_LOGGED_IN_PAGE = 'https://naveenautomationlabs.com/opencart/index.php?route=account/account'
    # PRACTICE_PAGE = 'https://automationexercise.com/'
    HOME_PAGE_TITLE = 'Your Store'
    REGISTER_PAGE_URL= 'https://naveenautomationlabs.com/opencart/index.php?route=account/register'
    REGISTER_PAGE_TITLE ='Register Account'
    LOGIN_PAGE_TITLE = 'Account Login'
    ACCOUNT_PAGE_TITLE = 'My Account'
    SUCCESS_REGISTRATION = 'Your Account Has Been Created!'

    EXCEL_SHEET ='data.xlsx'
    SHEET_NAME = 'registration'
    TEXT_EMPTY_CART = '0 item(s) - $0.00'
    CART_TOTAL_1_ITEM = '1 item(s) - $602.00'
    ITEMS_CAROUSEL = ('Harley Davidson','Dell','Disney','Starbucks','Nintendo','NFL','RedBull','Sony','Coca Cola','Burger King','Canon')
    PRODUCT = "macbook"

    secrets = SecretsManager().get_secret(
        "valid_user"
    )

    USERNAME = secrets["username"]
    PASSWORD = secrets["password"]


    # go rest related information
    GO_REST_TOKEN = "Bearer 1fc7a9600574fdad7ea52e876b79ef83815dec12887fa380ed7d18796c8154b5"
    BASE_URL_API = os.getenv("BASE_URL_API")
    PATH_SCHEMA = '../ecart/configs/schema.json'




# april.lastname@test.com
# Test@12345