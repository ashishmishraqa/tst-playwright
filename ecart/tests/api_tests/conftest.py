import json
import pathlib
import pytest
import requests
from configs.settings import TestData


@pytest.fixture(scope="function")
def auth_token():
    return TestData.GO_REST_TOKEN

@pytest.fixture(scope="function")
def api_auth(auth_token):
    api_request = requests.session()
    api_request.headers.update({'Authorization': auth_token})
    return api_request

@pytest.fixture(scope="function")
def get_schema():
    schema_path = pathlib.Path(__file__).resolve().parent.parent.parent / 'configs' / 'schema.json'
    with open(schema_path) as f:
        schema_json = json.load(f)
    return schema_json


