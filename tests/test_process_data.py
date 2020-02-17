import pytest
import json
import requests_mock
import io

from src import process_data

with open('tests/mocks/bibs-mergedOCLCNumbers.json', 'r') as myfile:
    data=myfile.read()
    
with open('tests/mocks/bibs-mergedOCLCNumbers2.json', 'r') as myfile:
    data2=myfile.read()
    
with open('tests/mocks/holdings_symbol.json', 'r') as myfile:
    data3=myfile.read()
    
with open('tests/mocks/holdings_symbol2.json', 'r') as myfile:
    data4=myfile.read()
    
with open('tests/mocks/retained_holdings_state_CA.json', 'r') as myfile:
    data5=myfile.read()

with open('tests/mocks/retained_holdings_state2.json', 'r') as myfile:
    data6=myfile.read()
    
with open('tests/mocks/retained_holdings-ocn-symbol.json', 'r') as myfile:
    data7=myfile.read()

with open('tests/mocks/retained_holdings-ocn-symbol2.json', 'r') as myfile:
    data8=myfile.read()  
    
with open('tests/mocks/retained_holdings_institution.json', 'r') as myfile:
    data9=myfile.read()

with open('tests/mocks/retained_holdings_institution2.json', 'r') as myfile:
    data10=myfile.read()                        

# parse file
merged_oclcnumbers = json.loads(data)
merged_oclcnumbers2 = json.loads(data2)

institution_holdings = json.loads(data3)
institution_holdings2 = json.loads(data4)

retained_byState = json.loads(data5)
retained_byState2 = json.loads(data6)

retained_bySymbol = json.loads(data7)
retained_bySymbol2 = json.loads(data8)

retained_holdings_institution = json.loads(data9)
retained_holdings_institution2 = json.loads(data10)


def test_retrieveMergedOCLCNumbers(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs/311684437', status_code=200, json=merged_oclcnumbers)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs/318877925', status_code=200, json=merged_oclcnumbers2)
    item_file = io.StringIO("oclcNumber\n311684437\n318877925")
    output_dir = tmpdir / "output.txt"
    fileInfo = {"output_dir": output_dir}
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveMergedOCLCNumbers(getTestConfig, item_file, fileInfo)
                              
def test_retrieveHoldingsByOCLCNumber(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    oclcSymbol = "OCPSB"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-detailed-holdings?oclcNumber=318877925&heldBy=' + oclcSymbol, status_code=200, json=institution_holdings)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-detailed-holdings?oclcNumber=191865523&heldBy=' + oclcSymbol, status_code=200, json=institution_holdings2)
    item_file = io.StringIO("oclcNumber\n318877925\n191865523")
    output_dir = tmpdir / "output.txt"
    fileInfo = {"output_dir": output_dir}     
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveHoldingsByOCLCNumber(getTestConfig, item_file, fileInfo, heldBy=oclcSymbol)
    
def test_retrieveSPByOCLCNumber(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    heldInState = "CA"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=776775878&heldInState=' + heldInState, status_code=200, json=retained_byState)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=1702614&heldInState=' + heldInState, status_code=200, json=retained_byState2)    
    item_file = io.StringIO("oclcNumber\n776775878\n1702614")
    output_dir = tmpdir / "output.txt"
    fileInfo = {"output_dir": output_dir}    
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveSPByOCLCNumber(getTestConfig, item_file, fileInfo, heldInState=heldInState)
    
def test_retrieveInstitutionRetentionsbyOCLCNumber(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    oclcSymbol = 'CCO'
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?oclcNumber=776775878&heldBy=' + oclcSymbol, status_code=200, json=retained_bySymbol)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?oclcNumber=1702614&heldBy=' + oclcSymbol, status_code=200, json=retained_bySymbol2)    
    item_file = io.StringIO("oclcNumber\n776775878\n1702614")
    output_dir = tmpdir / "output.txt"
    fileInfo = {"output_dir": output_dir}    
    getTestConfig.update({"oauth-session": mockOAuthSession}) 
    result = process_data.retrieveInstitutionRetentionsbyOCLCNumber(getTestConfig, item_file, fileInfo, oclcSymbol)

def test_retrieveAllInstitutionRetentions(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?heldBy=CCO', status_code=200, json=retained_holdings_institution)    
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?heldBy=CDU', status_code=200, json=retained_holdings_institution2)
    item_file = io.StringIO("symbol\nCCO\nCDU")
    output_dir = tmpdir / "output.txt"
    fileInfo = {"output_dir": output_dir}
    getTestConfig.update({"oauth-session": mockOAuthSession})
    process_data.retrieveAllInstitutionRetentions(getTestConfig, item_file, fileInfo)       
                                 