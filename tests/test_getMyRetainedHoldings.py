import pytest
import json
import requests_mock
import pandas
import handler

with open('tests/mocks/my_retained_holdingsOCN.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_retained_holdings_oclcnumber = json.loads(data)

with open('tests/mocks/my_retained_holdings_serial.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_retained_holdings_serial = json.loads(data)

with open('tests/mocks/my_retained_holdingsBarcode.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_retained_holdings_barcode = json.loads(data)

with open('tests/mocks/no_holdings.json', 'r') as myfile:
    data=myfile.read()

# parse file
my_retainedholdings_none = json.loads(data)


def test_getMyLibraryRetainedHoldingsOCLCNumber(requests_mock):
    oclcNumber = "156891904"
    oclcSymbol = "OCWMS"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?oclcNumber=' + oclcNumber + "&heldBy=" + oclcSymbol, status_code=200, json=my_retained_holdings_oclcnumber)
    holdings = handler.getMyLibraryRetainedHoldings(oclcSymbol, {"type": "oclcnumber", "value": oclcNumber})
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == '156891904'
    assert len(holdings[1].split(',')) == 10
    assert '220309732' in holdings[1].split(',')   
    assert len(holdings[2].split(',')) == 1
    assert len(holdings[3].split(',')) == 1 
    assert holdings[4] == 'success'
    
def test_getMyLibraryRetainedHoldingsOCLCNumberSerial(requests_mock):
    oclcNumber = "456314438"
    oclcSymbol = "OCWMS"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?oclcNumber=' + oclcNumber + "&heldBy=" + oclcSymbol, status_code=200, json=my_retained_holdings_serial)
    holdings = handler.getMyLibraryRetainedHoldings(oclcSymbol, {"type": "oclcnumber", "value": oclcNumber})
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == '456314438'
    assert len(holdings[1].split(',')) == 1
    assert holdings[1].split(',')[0] == '222309835'   
    assert len(holdings[2].split(',')) == 2
    assert '0987654321' in holdings[2].split(',')
    assert '1234567890' in holdings[2].split(',')
    assert len(holdings[3].split(',')) == 1
    assert holdings[4] == 'success'     

def test_getMyLibraryRetainedHoldingsBarcode(requests_mock):
    barcode = "305100416722V"
    oclcSymbol = "OCWMS"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?barcode=' + barcode + "&heldBy=" + oclcSymbol, status_code=200, json=my_retained_holdings_barcode)
    holdings = handler.getMyLibraryRetainedHoldings(oclcSymbol, {"type": "barcode", "value": barcode})
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == "544175"
    assert holdings[1] == '122418193'
    assert holdings[2].split(',')[0] == '305100416722V'
    assert len(holdings[2].split(',')) == 1 
    assert holdings[3] == "OCWMS-MAIN-MAIN-STACKS"
    assert len(holdings[3].split(',')) == 1 
    assert holdings[4] == 'success'    
    
def test_getMyLibraryRetainedHoldings_None(requests_mock):
    barcode = "CR963528"
    oclcSymbol = "OCWMS"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?barcode=' + barcode + "&heldBy=" + oclcSymbol, status_code=200, json=my_retainedholdings_none)
    holdings = handler.getMyLibraryRetainedHoldings(oclcSymbol, {"type": "barcode", "value": barcode});
    assert type(holdings) is pandas.core.series.Series
    assert holdings[0] == ""
    assert holdings[1] == ""
    assert holdings[2] == "" 
    assert holdings[3] == "none"
    assert holdings[4] == 'success'   
    
    