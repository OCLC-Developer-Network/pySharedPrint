import pytest
import json
import requests_mock
import pandas
import handler

with open('tests/mocks/bibs-mergedOCLCNumbers.json', 'r') as myfile:
    data=myfile.read()

# parse file
merged_oclcnumbers = json.loads(data)


def test_getMergedOCLCNumbers(requests_mock):
    oclcNumber = "311684437"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs/' + oclcNumber, status_code=200, json=merged_oclcnumbers)
    bib = handler.getMergedOCLCNumbers(oclcNumber);
    assert type(bib) is pandas.core.series.Series
    assert bib[0] == '311684437'
    assert len(bib[1].split(',')) == 9 
    assert bib[2] == 'success' 