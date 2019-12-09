import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/myholdingsOCLCNumber.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_oclcnumber = json.loads(data)

with open('tests/mocks/my_holdings_serial_multipleLHRs.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_oclcnumber_serial = json.loads(data)

with open('tests/mocks/my_holdings_barcode.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_barcode = json.loads(data)

with open('tests/mocks/my_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings = json.loads(data)


with open('tests/mocks/my_holdings_serial.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_serial = json.loads(data)


with open('tests/mocks/my_holdings_serial_2.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_serial2 = json.loads(data)

with open('tests/mocks/my_holdings_none.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_none = json.loads(data)

with open('tests/mocks/my_holdings_notfound.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_holdings_notfound = json.loads(data)

def test_getMyLibraryHoldingsOCLCNumber(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "70775700"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?oclcNumber=' + oclcNumber, status_code=200, json=my_holdings_oclcnumber)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "oclcnumber", oclcNumber)
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == '70775700'
    assert len(holdings[1].split(',')) == 2
    assert holdings[1].split(',')[0] == '62378575'
    assert holdings[1].split(',')[1] == '58121871'
    assert '184108714091' in holdings[2].split(',')
    assert '54321' in holdings[2].split(',')    
    assert len(holdings[2].split(',')) == 2
    assert holdings[3] == 2
    assert len(holdings[4].split(',')) == 2 
    assert holdings[5] == 'success'
    
def test_getMyLibraryHoldingsOCLCNumberSerial(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    oclcNumber = "2445677"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?oclcNumber=' + oclcNumber, status_code=200, json=my_holdings_oclcnumber_serial)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "oclcnumber", oclcNumber)
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == '2445677'
    assert len(holdings[1].split(',')) == 10
    assert holdings[1].split(',')[0] == '223667789'
    assert holdings[1].split(',')[1] == '223667393'
    assert holdings[1].split(',')[2] == '223603680'
    assert holdings[1].split(',')[3] == '223603435'
    assert holdings[1].split(',')[4] == '223603835'
    assert holdings[1].split(',')[5] == '223604406'
    assert holdings[1].split(',')[6] == '223604491'
    assert holdings[1].split(',')[7] == '223605910'
    assert holdings[1].split(',')[8] == '223606436'
    assert holdings[1].split(',')[9] == '223607240'    
    assert len(holdings[2].split(',')) == 34
    assert holdings[3] == 14
    assert len(holdings[4].split(',')) == 2
    assert holdings[5] == 'success'     

def test_getMyLibraryHoldingsBarcode(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    barcode = "CR963528"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?barcode=' + barcode, status_code=200, json=my_holdings_barcode)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "barcode", barcode)
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "246197114"
    assert holdings[1] == '132422447'
    assert holdings[2].split(',')[0] == 'CR963528'
    assert len(holdings[2].split(',')) == 1 
    assert holdings[3] == 1
    assert len(holdings[4].split(',')) == 1 
    assert holdings[5] == 'success' 
    
def test_getMyLibraryHoldingsAccessionNumber(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    accession_number = "132422447"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings/' + accession_number, status_code=200, json=my_holdings)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "accession_number", accession_number);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "246197114"
    assert holdings[1] == '132422447'
    assert holdings[2].split(',')[0] == 'CR963528'
    assert len(holdings[2].split(',')) == 1 
    assert holdings[3] == None
    assert len(holdings[4].split(',')) == 1 
    assert holdings[5] == 'success'
    
def test_getMyLibraryHoldingsAccessionNumberSerial(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    accession_number = "223603680"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings/' + accession_number, status_code=200, json=my_holdings_serial)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "accession_number", accession_number);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "2445677"
    assert holdings[1] == '223603680'
    assert holdings[2].split(',')[0] == 'oclc1'
    assert len(holdings[2].split(',')) == 1 
    assert holdings[3] == None
    assert len(holdings[4].split(',')) == 1 
    assert holdings[5] == 'success'
    
def test_getMyLibraryHoldingsAccessionNumberSerial2(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    accession_number = "223604491"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings/' + accession_number, status_code=200, json=my_holdings_serial2)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "accession_number", accession_number);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "2445677"
    assert holdings[1] == '223604491'
    assert holdings[2].split(',')[0] == 'oclc5'
    assert holdings[2].split(',')[1] == 'oclc5b'
    assert len(holdings[2].split(',')) == 2 
    assert holdings[3] == None
    assert len(holdings[4].split(',')) == 1 
    assert holdings[5] == 'success'        
    
## need a test for a serial with multiple holding parts and barcodes     
    
def test_getMyLibraryHoldings_None(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    barcode = "CR963528"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings?barcode=' + barcode, status_code=200, json=my_holdings_none)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "barcode", barcode);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == ""
    assert holdings[1] == ""
    assert holdings[2] == "" 
    assert holdings[3] == 0
    assert holdings[4] == "none"
    assert holdings[5] == 'success'

def test_getMyLibraryHoldingsAccessionNumber_notFound(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    accession_number = "1"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/my-holdings/' + accession_number, status_code=200, json=my_holdings_notfound)
    holdings = make_requests.getMyLibraryHoldings(getTestConfig, "accession_number", accession_number);
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == ""
    assert holdings[1] == ""
    assert holdings[2] == "" 
    assert holdings[3] == None
    assert holdings[4] == "none"
    assert holdings[5] == 'success'       
    
    