import time
from playwright.sync_api import Page, expect, Playwright



# Note: by default, playwright will launch in headless mode
# It has global fixture as playwright provided by pytest-playwright package
# chromium will support chrome and Edge, can be passed as channel value
def test_playwright(playwright):
    browser = playwright.chromium.launch(channel = 'chrome', headless=False) # it will return a browser object
    # browser = playwright.firefox.launch(headless=False)  # it will return a browser object
    context = browser.new_context() # it will launch a new incognito window of the new browser
    page = context.new_page()
    page.goto("http://www.rahulshettyacademy.com/")


# the default Chrome browser in headless mode will be launched
# Better way: to import the page fixture from the Page class from
def test_playwright_other(page: Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    print(page.title())
    try:
        #label text should be referred to as id of an element or input tag should inside the label
        page.get_by_label('username').fill('rahulshettyacademy')
        page.get_by_label('word').fill('learning')
        page.get_by_role('combobox').select_option('teach')
        page.get_by_label('terms').click()
        page.get_by_role('button', name= 'Sign In').click()
        # to add assertion
        expect(page.get_by_text('Incorrect username/password.')).to_be_visible()
        time.sleep(5)
    except Exception as err:
        print(f'Exception found : {err}')


def test_playwright_expr(page: Page):
    page.goto("https://rahulshettyacademy.com/client/#/auth/login")
    print(page.title())
    try:
        # It will find element based on text present under label
        page.get_by_role('textbox', name = 'email@example.com').fill('test@test.com')
        page.get_by_role('textbox', name = 'enter your passsword').fill('test@12345')
        time.sleep(2)
    except Exception as err:
        print(f'Exception found : {err}')


"""Dynamic TC : add product- iphoneX and nokia edge name no matter where it is positioned,to the cart and checkout"""
def test_product_checkout(page:Page):
    try:
        page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        print(page.title())
        page.get_by_label('username').fill('rahulshettyacademy')
        page.get_by_label('word').fill('learning')
        page.get_by_role('combobox').select_option('teach')
        page.get_by_label('terms').click()
        page.get_by_role('button', name='Sign In').click()
        time.sleep(5)
        # expect(page.get_by_text('Incorrect username/password.')).to_be_visible()
        #First way: find element based on tagName- css selector and has text as - iphone X
        product_iphone = page.locator('app-card', has_text='iphone X')
        product_iphone.get_by_role('button', name='Add').click()
        time.sleep(2)
        #Second Way: applied filter to find text
        product_iphone = page.locator('app-card').filter(has_text='Nokia Edge')
        # product_iphone.get_by_role('button', name='Add').click()
        product_iphone.get_by_role('button').filter(has_text='Add').click()
        time.sleep(2)
        page.get_by_text('Checkout').click()
        # verify products are present
        expect(page.locator('.media-body')).to_have_count(count=2)
    except Exception as err:
        print(f'Exception found {err}')



"""switch control to a new page """
def test_new_window(page:Page):
    try:

        page.goto("https://rahulshettyacademy.com/loginpagePractise/")


        # when any of the step written below to the expect pop up and any pop up appears then the page will be passed to the variable popup
        with page.expect_popup() as popup:
            print('test--------------------------')
            print(page.locator('.text-center').filter(has_text='username is ').text_content())
            page.get_by_text('Free Access').click()
            new_page = popup.value
            # expect(page.get_by_text('JOIN NOW')).to_be_visible()
            text = new_page.get_by_text('JOIN NOW').text_content()
            print(text)
            time.sleep(3)
    except Exception as err:
        print(err)


def test_ui_checks(page:Page):
    try:
        # to check hide and show feature on a page
        page.goto('https://rahulshettyacademy.com/AutomationPractice/')
        expect(page.get_by_placeholder('Hide/Show Example')).to_be_visible()
        page.locator('#hide-textbox').filter(has_text='Hide').click()
        expect(page.get_by_placeholder('Hide/Show Example')).to_be_hidden()
        time.sleep(2)
        # to handel JavaScript dialog box with an event handler - on
        page.on('dialog', lambda dialog: dialog.accept())
        page.get_by_role('button', name='Confirm').click()
        time.sleep(2)

        # frame handling
        page_frame = page.frame_locator('#courses-iframe')
        # if more than elements are found then first get the locator assert if there is only one locator then performa actions
        locator_access_plan = page_frame.get_by_role('link', name = 'All Access plan')
        expect(locator_access_plan).to_have_count(1)
        locator_access_plan.click()
        time.sleep(2)
    except Exception as err:
        print(f'Exception found: {err}')

#table activity: Check the price of rice =37 ,
# When the column position is dynamic, the safest approach is:
# Identify the column index for Price from the header (<th>).
# Locate the row that has the desired item (e.g., "Rice").
# Extract the value from the cell at the same column index.
def test_table(page:Page):
    page.goto('https://rahulshettyacademy.com/seleniumPractise/#/offers')
    # find the price column: it can be 2nd, 3rd 4th etc
    count_col = page.locator('th').count()
    position_col = None
    for i in range(count_col):
        if page.locator('th').nth(i).text_content() == 'Price':
            position_col=i
            break
    print(f'position of price item is : {position_col}')
    row_item = page.locator('tr').filter(has_text='Rice')
    price = row_item.locator('td').nth(position_col).text_content().strip()
    print(f'Price of the rice is : {price}')
    time.sleep(4)


"""API + UI Test: Login to UI application Make API call place an order get the order ID and verify that order on UI
#userame=demo@playwright.com && Password=Qwe@1234"""
# @pytest.mark.parametrize('fetch_test_data', fetch_test_data)
def test_end_to_end(playwright: Playwright, fetch_test_data):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://rahulshettyacademy.com/client')
    expect(page).to_have_title("Let's Shop")  # assert the page title
    # print(fetch_test_data)

    # page.locator('#userEmail').fill(fetch_test_data['user'])
    # page.locator('#userPassword').fill(fetch_test_data['password'])
    # page.get_by_role('button', name='login').click()
    # expect(page.get_by_text('Home |')).to_have_count(2)
    # time.sleep(3)
    # api_utils = APIUtils()
    # api_utils.create_order(playwright)








