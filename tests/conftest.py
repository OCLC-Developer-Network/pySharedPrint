import pytest
import yaml
import json
import requests_mock

from src import make_requests

with open('tests/mocks/access_token.json', 'r') as myfile:
    data=myfile.read()

# parse file
oauth_response = json.loads(data)

@pytest.fixture(scope="function")
def mockOAuthSession(requests_mock, getTestConfig):
    requests_mock.register_uri('POST', getTestConfig.get('token_url') , status_code=200, json=oauth_response)
    oauth_session = make_requests.createOAuthSession(getTestConfig, 'DISCOVERY')    
    return oauth_session

@pytest.fixture(scope="function")
def getTestConfig():
    with open("tests/test_config.yml", 'r') as stream:
        config = yaml.safe_load(stream)
    
    return config

