import json

from playwright.sync_api import Playwright


class APIUtils:

    def get_login_token(self, playwright: Playwright):
        api_request = playwright.request.new_context(base_url='https://rahulshettyacademy.com')
        user_payload = {'userEmail': "demo@playwright.com", 'userPassword': "Qwe@1234"}
        login_response = api_request.post('/api/ecom/auth/login',data = user_payload,
                                          headers={'content-type':'application/json'})
        assert login_response.ok
        return login_response.json()['token']

    def login_via_api(self, page):
        # Use the same request context as the page
        api_request = page.request
        user_payload = {'email': "allenamy@example.net", 'password': "ioY=^Y2(@0:Y"}

        login_response = api_request.post(
            'https://naveenautomationlabs.com/opencart/index.php?route=account/login',
            data=user_payload
        )

        assert login_response.ok
        # print(login_response.jsonn())

        # # Playwright automatically handles cookies if you use page.request
        # # or you can explicitly capture and set them:
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



