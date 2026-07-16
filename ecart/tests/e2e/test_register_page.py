import pytest
from playwright.sync_api import expect
from ecart.tests.test_base import BaseTest
from ecart.configs.settings import TestData

class TestRegisterPage(BaseTest):


    @pytest.mark.smoke
    def test_submit_registration(self, page, home_page, valid_registration_user):
        """ Test the submit registration page """
        # 1. verify the home page appears
        expect(page).to_have_title(TestData.HOME_PAGE_TITLE)

        # 2. click on the register button on home page & verify the page title
        register_page = home_page.click_register()
        expect(page).to_have_title(TestData.REGISTER_PAGE_TITLE)

        # 3. Perform the registration & verify if registration is successful
        register_page.register_user(valid_registration_user)
        expect(page).to_have_title(TestData.SUCCESS_REGISTRATION)

