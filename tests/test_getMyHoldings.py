import pytest
import json
import requests_mock
import pandas
import handler

with open('tests/mocks/myholdingsOCLCNumber.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_oclcnumber = json.loads(data)

with open('tests/mocks/my_holdings_barcode.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_barcode = json.loads(data)

with open('tests/mocks/my_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings = json.loads(data)

with open('tests/mocks/my_holdings_none.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_none = json.loads(data)

with open('tests/mocks/my_holdings_notfound.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_notfound = json.loads(data)

def test_getMyLibraryHoldingsOCLCNumber(requests_mock):
    oclcNumber = "70775700"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?oclcNumber=' + oclcNumber, status_code=200, json=my_holdings_oclcnumber)
    holdings = handler.getMyLibraryHoldings("oclcnumber", oclcNumber)
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == '70775700'
    assert len(holdings[1].split(',')) == 2
    assert holdings[1].split(',')[0] == '62378575'
    assert holdings[1].split(',')[1] == '58121871'
    assert holdings[2].split(',')[0] == '54321'
    assert holdings[2].split(',')[1] == '184108714091'
    assert len(holdings[2].split(',')) == 2
    assert holdings[3] == 2
    assert len(holdings[4].split(',')) == 2 
    assert holdings[5] == 'success' 

def test_getMyLibraryHoldingsBarcode(requests_mock):
    barcode = "CR963528"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?barcode=' + barcode, status_code=200, json=my_holdings_barcode)
    holdings = handler.getMyLibraryHoldings("barcode", barcode)
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "246197114"
    assert holdings[1] == '132422447'
    assert holdings[2].split(',')[0] == 'CR963528'
    assert len(holdings[2].split(',')) == 1 
    assert holdings[3] == 1
    assert len(holdings[4].split(',')) == 1 
    assert holdings[5] == 'success' 
    
def test_getMyLibraryHoldingsAccessionNumber(requests_mock):
    accession_number = "132422447"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings/' + accession_number, status_code=200, json=my_holdings)
    holdings = handler.getMyLibraryHoldings("accession_number", accession_number);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "246197114"
    assert holdings[1] == '132422447'
    assert holdings[2].split(',')[0] == 'CR963528'
    assert len(holdings[2].split(',')) == 1 
    assert holdings[3] == None
    assert len(holdings[4].split(',')) == 1 
    assert holdings[5] == 'success'
    
## need a test for a serial with multiple holding parts and barcodes     
    
def test_getMyLibraryHoldings_None(requests_mock):
    barcode = "CR963528"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?barcode=' + barcode, status_code=200, json=my_holdings_none)
    holdings = handler.getMyLibraryHoldings("barcode", barcode);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == ""
    assert holdings[1] == ""
    assert holdings[2] == "" 
    assert holdings[3] == 0
    assert holdings[4] == "none"
    assert holdings[5] == 'success'

def test_getMyLibraryHoldingsAccessionNumber_notFound(requests_mock):
    accession_number = "1"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings/' + accession_number, status_code=200, json=my_holdings_notfound)
    holdings = handler.getMyLibraryHoldings("accession_number", accession_number);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == ""
    assert holdings[1] == ""
    assert holdings[2] == "" 
    assert holdings[3] == None
    assert holdings[4] == "none"
    assert holdings[5] == 'success'       
    
    