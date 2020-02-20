import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
holdings_list = json.loads(data)

with open('tests/mocks/no_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
no_holdings_list = json.loads(data)


def test_getBriefHoldings(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "2416076"
    country = "US"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/worldcat/v1/bibs-holdings?oclcNumber=' + oclcNumber + '&heldInCountry=' + country, status_code=200, json=holdings_list)
    bib = make_requests.getBriefHoldings(getTestConfig, oclcNumber, country);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '2416076'
    assert bib[1] == 16005
    assert len(bib[2].split(',')) == 16005 
    assert bib[3] == 'success' 
    
def test_getBriefHoldings_NoResults(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "2416076"
    country = "CH"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/worldcat/v1/bibs-holdings?oclcNumber=' + oclcNumber + '&heldInCountry=' + country, status_code=200, json=no_holdings_list)
    bib = make_requests.getBriefHoldings(getTestConfig, oclcNumber, country);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '2416076'
    assert bib[1] == 246
    assert bib[2] == ""
    assert bib[3] == 'success'     
    
    