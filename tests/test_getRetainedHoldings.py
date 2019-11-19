import pytest
import json
import requests_mock
import pandas
import handler

with open('tests/mocks/retained_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
retained_holdings_list = json.loads(data)

with open('tests/mocks/retained_holdings_group.json', 'r') as myfile:
    data=myfile.read()

# parse file
retained_holdings_group = json.loads(data)

with open('tests/mocks/retained_holdings_state.json', 'r') as myfile:
    data=myfile.read()

# parse file
retained_holdings_state = json.loads(data)

with open('tests/mocks/no_retained_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
no_retained_holdings = json.loads(data)

def test_getRetainedHoldings(requests_mock):
    oclcNumber = "1752384"
    group = "ASRL"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=' + oclcNumber, status_code=200, json=retained_holdings_list)
    bib = handler.getRetainedHoldings(oclcNumber);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '1752384'
    assert bib[1] == 716
    assert len(bib[2].split(',')) == 1 
    assert bib[3] == 'success'

def test_getRetainedHoldings_HeldByGroup(requests_mock):
    oclcNumber = "1752384"
    group = "ASRL"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=' + oclcNumber + '&heldByGroup=' + group, status_code=200, json=retained_holdings_group)
    bib = handler.getRetainedHoldings(oclcNumber, heldByGroup=group);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '1752384'
    assert bib[1] == 716
    assert len(bib[2].split(',')) == 1 
    assert bib[3] == 'success' 

def test_getRetainedHoldings_HeldInState(requests_mock):
    oclcNumber = "1752384"
    state = "GA"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=' + oclcNumber + '&heldInState=' + state, status_code=200, json=retained_holdings_state)
    bib = handler.getRetainedHoldings(oclcNumber, heldInState=state);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '1752384'
    assert bib[1] == 716
    assert len(bib[2].split(',')) == 1 
    assert bib[3] == 'success'
    
def test_getRetainedHoldings_NoResults(requests_mock):
    oclcNumber = "2416076"
    state = "CA"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=' + oclcNumber + '&heldInState=' + state, status_code=200, json=no_retained_holdings)
    bib = handler.getRetainedHoldings(oclcNumber, heldInState=state);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '2416076'
    assert bib[1] == 246
    assert bib[2] == ""
    assert bib[3] == 'success'        
    
    