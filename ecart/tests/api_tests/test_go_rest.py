import pytest
from configs.settings import TestData
from tests.test_base import BaseTest
from utilities.faker_helper import FakerDataGenerator
from utilities.logger import get_logger
from jsonschema import validate


class TestApi(BaseTest):
    log = get_logger(__name__)

    fake = FakerDataGenerator()

    # @pytest.mark.skip
    @pytest.mark.dependency(depends=["TestApi::test_user_creation"])
    @pytest.mark.smoke
    def test_get_request(self,api_auth, pytestconfig):
        id = pytestconfig.cache.get("id", default="")
        request_url = f"{TestData.BASE_URL_API}/public/v2/users/{id}"
        api_response = api_auth.get(request_url)
        self.log.info(f"GET request to {request_url} returned status code {api_response}")
        assert api_response.status_code == 200


    @pytest.mark.smoke
    def test_user_creation(self,api_auth, get_schema, pytestconfig  ):
        # arrange
        request_url = f'{TestData.BASE_URL_API}/public/v2/users'
        self.log.info(f"POST request to {request_url} for user creation")
        payload = self.fake.generate_go_rest_post_body()

        # act
        api_response = api_auth.post(request_url, json=payload )
        self.log.info(f"POST request to {request_url} returned status code {api_response.json()}")

        # assert
        assert api_response.status_code == 201, f'Expected 201, received {api_response.status_code}'
        validate(instance=api_response.json(), schema=get_schema)
        pytestconfig.cache.set("id", api_response.json()['id'])
