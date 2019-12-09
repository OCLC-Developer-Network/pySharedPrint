import pytest
import json
import requests_mock
from requests_oauthlib import OAuth2Session

from src import make_requests

with open('tests/mocks/access_token.json', 'r') as myfile:
    data=myfile.read()

# parse file
oauth_response = json.loads(data)

def test_createOAuthSession(requests_mock, getTestConfig):
    #?grant_type=client_credentials&scope=DISCOVERY
    requests_mock.register_uri('POST', 'https://oauth.oclc.org/token', status_code=200, json=oauth_response)
    oauth_session = make_requests.createOAuthSession(getTestConfig, 'DISCOVERY') 
    assert type(oauth_session) is OAuth2Session
    assert oauth_session.access_token == 'tk_12345'
     