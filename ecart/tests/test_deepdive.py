import time

import pytest
from playwright.sync_api import Page, expect, Playwright

from utilities.base_utils import APIUtils

fake_no_orders_response ={"data":[],"message":"No Orders"}

def intercept_response(route):
    route.fulfill(json=fake_no_orders_response)

@pytest.mark.skip
def test_network(page:Page):
    page.goto('https://rahulshettyacademy.com/client')
    expect(page).to_have_title("Let's Shop")
    print(f'Page has title as {page.title()}')
    # intercept the call to get orders -> Simulate the fake response -> validate the rendered fake response
    page.route('https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*', handler=intercept_response)
    # Login
    page.locator('#userEmail').fill('demo@playwright.com')
    page.locator('#userPassword').fill('Qwe@1234')
    page.get_by_role('button', name='login').click()
    time.sleep(5)
    #click on orders
    page.get_by_role('button', name='ORDERS').click()
    text= page.locator(".mt-4").text_content()

    print(f'text appears as :{text}' )


def intercept_request(route):
    route.continue_(url='https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=68d3527c1233')

@pytest.mark.skip
def test_network_2(page:Page):
    page.goto('https://rahulshettyacademy.com/client')
    expect(page).to_have_title("Let's Shop")
    print(f'Page has title as {page.title()}')
    # intercept the call to get orders -> Simulate the fake response -> validate the rendered fake response
    page.route('https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*', handler=intercept_request)
    # Login
    page.locator('#userEmail').fill('demo@playwright.com')
    page.locator('#userPassword').fill('Qwe@1234')
    page.get_by_role('button', name='login').click()
    time.sleep(5)
    #click on orders
    page.get_by_role('button', name='ORDERS').click()
    page.get_by_role('button', name='View').click()
    time.sleep(2)
    print(page.locator('.blink_me').text_content())


@pytest.mark.skip
def test_inject_cookie(playwright: Playwright):
    api_utils= APIUtils()
    token = api_utils.get_login_token(playwright)
    log.info(f'token received as : {token}')
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Generate Login token and inject to cookies- local storage
    page.add_init_script(f"""localStorage.setItem('token','{token}')""")
    page.goto('https://rahulshettyacademy.com/client/')
    print('landed on home page!')
    time.sleep(2)
    page.get_by_role('button', name='ORDERS').click()
    expect(page.get_by_text('Your Orders')).to_be_visible()
    time.sleep(2)
    print('landed on order list page!')


