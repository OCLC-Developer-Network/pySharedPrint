import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/retained-holdings-bySymbol.json', 'r') as myfile:
    data=myfile.read()

# parse file
merged_oclcnumbers = json.loads(data)


def test_getLibraryRetainedHoldings(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcSymbol = "ANZSL"
    df = pandas.DataFrame(columns=['oclcnumber', 'accession_number'])
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/worldcat/v1/retained-holdings?heldBy=' + oclcSymbol, status_code=200, json=merged_oclcnumbers)
    retainedholdingList = make_requests.getLibraryRetainedHoldings(getTestConfig, df, oclcSymbol);
    assert type(retainedholdingList) is pandas.DataFrame
    assert list(retainedholdingList.columns.values) == ['oclcnumber', 'accession_number']
    assert len(retainedholdingList.index) == 10
    assert retainedholdingList.iloc[0]['oclcnumber'] == '25748966'
    assert retainedholdingList.iloc[0]['accession_number'] == '168860541'