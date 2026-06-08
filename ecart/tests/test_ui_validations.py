import time
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.skip
def test_ui_validations(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_role('combobox').select_option('teach')
    page.get_by_label('username').fill('rahulshettyacademy')
    page.get_by_label('password').fill('Learning@830$3mK2')
    page.locator('#terms').click()
    time.sleep(2)
    page.get_by_role('button', name='Sign In').click()
    # add products to the cart
    product_iphone = page.locator('app-card').filter(has_text='iphone X')
    product_iphone.get_by_role('button', name='Add').click()
    product_iphone = page.locator('app-card').filter(has_text='Nokia Edge')
    product_iphone.get_by_role('button', name='Add').click()
    page.get_by_text('Checkout').click()
    expect(page.locator('.media-body')).to_have_count(2)

@pytest.mark.skip
def test_new_window(page:Page):
    page.goto('https://rahulshettyacademy.com/loginpagePractise/')

    time.sleep(2)
    with page.expect_popup() as popup:
        page.get_by_role('link', name='Free Access to InterviewQues/ResumeAssistance/Material').click()
        childpage = popup.value
        expect(childpage.get_by_text('Documents request')).to_be_visible()


@pytest.mark.skip
def test_more_checks(page:Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.locator('#name')).to_be_visible()
    page.get_by_role('button', name='Hide').click()
    expect(page.locator('#name')).to_be_visible()
    # alert this is event created prior to the action
    time.sleep(2)
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role('button', name='Alert').click()
    time.sleep(2)
    # frame handling
    page_frame = page.frame_locator('#courses-iframe')
    page_frame.get_by_role('link', name='All Access plan').click()
    expect(page_frame.get_by_text('All Access Subscription')).to_be_visible()
    expect(page_frame.locator('body')).to_contain_text('All Access Subscription')

@pytest.mark.skip
def test_tables(page:Page):
    page.goto('https://rahulshettyacademy.com/seleniumPractise/#/offers')
    #identify col and row get the price
    col_price = None
    for i in range(page.locator('th').count()):
        if page.locator('th').nth(i).text_content()=='Price':
            col_price = i
            print(f'Price column: {col_price}')
    row_rice = page.locator('tr').filter(has_text='Rice').locator('td').nth(col_price).text_content()


@pytest.mark.skip
def test_api_testing(page:Page):
    page.goto('https://rahulshettyacademy.com/client/#/auth/login')
    expect(page.get_by_text('Ecom')).to_be_visible()
