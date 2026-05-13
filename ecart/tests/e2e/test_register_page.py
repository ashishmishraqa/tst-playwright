from webbrowser import register
import pytest
from playwright.sync_api import expect
from pages.auth.home_page import HomePage
from tests.test_base import BaseTest
from utilities.logger import get_logger
from configs.config import TestData




class TestRegisterPage(BaseTest):

    @pytest.mark.smoke
    def test_verify_title(self,page):
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        expect(page).to_have_title(TestData.HOME_PAGE_TITLE)
        home.click_register()
        expect(page).to_have_title(TestData.REGISTER_PAGE_TITLE)


    @pytest.mark.smoke
    def test_submit_registration(self,page):
        home = HomePage(page)
        home.navigate_to_home(TestData.BASE_URL)
        expect(page).to_have_title(TestData.HOME_PAGE_TITLE)
        register_page = home.click_register()
        expect(page).to_have_title(TestData.REGISTER_PAGE_TITLE)
        register_page.user_registration()
        expect(page).to_have_title(TestData.SUCCESS_REGISTRATION)

