import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/holdings_group.json', 'r') as myfile:
    data=myfile.read()

# parse file
holdings_group = json.loads(data)

with open('tests/mocks/holdings_symbol.json', 'r') as holdingsymbolfile:
  holding_symbol_data=holdingsymbolfile.read()

# parse file
holdings_symbol = json.loads(holding_symbol_data)

with open('tests/mocks/no_detailed_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
no_detailed_holdings = json.loads(data)

def test_getHoldings_HeldByGroup(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "1752384"
    group = "ASRL"
    requests_mock.register_uri('GET', 'https://americas.discovery.api.oclc.org/worldcat/v2/bibs-detailed-holdings?oclcNumber=' + oclcNumber + '&heldByGroup=' + group, status_code=200, json=holdings_group)
    bib = make_requests.getHoldings(getTestConfig, oclcNumber, heldByGroup=group);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '1752384'
    assert bib[1] == 716
    assert len(bib[2].split(',')) == 26 
    assert bib[3] == 'success'

def test_getHoldings_HeldBySymbol(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "318877925"
    institution_symbol = "OCPSB"
    requests_mock.register_uri('GET', 'https://americas.discovery.api.oclc.org/worldcat/v2/bibs-detailed-holdings?oclcNumber=' + oclcNumber + '&heldBy=' + institution_symbol, status_code=200, json=holdings_symbol)
    bib = make_requests.getHoldings(getTestConfig, oclcNumber, heldBy=institution_symbol);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '318877925'
    assert bib[1] == 246
    assert len(bib[2].split(',')) == 1 
    assert bib[3] == 'success' 
    
def test_getHoldings_NoResults(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "2416076"
    institution_symbol = "OCPSB"
    requests_mock.register_uri('GET', 'https://americas.discovery.api.oclc.org/worldcat/v2/bibs-detailed-holdings?oclcNumber=' + oclcNumber + '&heldBy=' + institution_symbol, status_code=200, json=no_detailed_holdings)
    bib = make_requests.getHoldings(getTestConfig, oclcNumber, heldBy=institution_symbol);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '2416076'
    assert bib[1] == 246
    assert bib[2] == "none"
    assert bib[3] == 'success'       
    
    