import pytest
from configs.settings import TestData
from tests.test_base import BaseTest
from utilities.faker_helper import FakerDataGenerator
from utilities.logger import get_logger
from jsonschema import validate


class TestApi(BaseTest):
    log = get_logger(__name__)

    fake = FakerDataGenerator()

    """
    Dependency marker is added for learning and understanding purpose not a standard, IN production grade systems 
    Best way to use common test data is via fixtures
    """


    @pytest.mark.smoke
    @pytest.mark.order(1)
    @pytest.mark.dependency(name="create user")
    def test_user_creation(self,api_auth, get_schema, pytestconfig  ):
        # arrange
        request_url = f'{TestData.BASE_URL_API}/public/v2/users'
        self.log.info(f"POST request to {request_url} for user creation")
        payload = self.fake.generate_go_rest_post_body()

        # act
        api_response = api_auth.post(request_url, json=payload )
        http_response_code = api_response.status_code

        # assert
        assert http_response_code == 201, f'Expected 201 but got {http_response_code}'
        self.log.info(f"POST request to {request_url} returned status code {http_response_code}")
        validate(instance=api_response.json(), schema=get_schema)
        pytestconfig.cache.set("id", api_response.json()['id'])


    @pytest.mark.dependency(depends=["create user"])
    @pytest.mark.order(2)
    @pytest.mark.smoke
    def test_get_request(self,api_auth, pytestconfig):
        # 1. Arrange: get the id from the previous test
        user_id = pytestconfig.cache.get("id", default="")
        request_url = f"{TestData.BASE_URL_API}/public/v2/users/{user_id}"

        # 2. Act: Make the GET request call
        api_response = api_auth.get(request_url)
        self.log.info(f"GET request to {request_url} returned status code {api_response.status_code}")

        # 3. Assert: Check the response
        assert api_response.status_code == 200, 'Error! response code is not matching as expected '

