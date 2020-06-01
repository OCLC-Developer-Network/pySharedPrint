import pytest
import json
import requests_mock
import pandas

from src import make_requests

with open('tests/mocks/bibs-mergedOCLCNumbers.json', 'r') as myfile:
    data=myfile.read()

# parse file
merged_oclcnumbers = json.loads(data)

def test_getMergedOCLCNumbers(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "311684437"
    requests_mock.register_uri('GET', 'https://americas.discovery.api.oclc.org/worldcat/v2/bibs/' + oclcNumber, status_code=200, json=merged_oclcnumbers)    
    bib = make_requests.getMergedOCLCNumbers(getTestConfig, oclcNumber);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '311684437'
    assert len(bib[1].split(',')) == 9 
    assert bib[2] == 'success' 