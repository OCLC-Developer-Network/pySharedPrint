import pytest
import json
import requests_mock
import io
import pandas
from pandas.testing import assert_frame_equal

from src import handle_files, process_data

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


def test_retrieveMergedOCLCNumbers(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs/311684437', status_code=200, json=merged_oclcnumbers)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs/318877925', status_code=200, json=merged_oclcnumbers2)
    item_file = io.StringIO("oclcNumber\n311684437\n318877925")
    csv_read = handle_files.loadCSV(item_file) 
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveMergedOCLCNumbers(getTestConfig, csv_read)
    assert type(result) is pandas.DataFrame
    #assert result.columns == ["oclcNumber", "mergedOCNs", "status"]
    final_result = pandas.DataFrame(data={"oclcNumber": [311684437, 318877925], "mergedOCNs":['261176486,330361568,377707240,426228842,701739996,716923895,731216527,887752101,945738851', '877908501,979175514,981548811,990719089,993246604,1005002644,1011917725,1016539262,1020206933,1057597575'], "status": ['success', 'success']})
    assert_frame_equal(result, final_result)
                              
def test_retrieveHoldingsByOCLCNumber(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    oclcSymbol = "OCPSB"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-detailed-holdings?oclcNumber=318877925&heldBy=' + oclcSymbol, status_code=200, json=institution_holdings)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-detailed-holdings?oclcNumber=191865523&heldBy=' + oclcSymbol, status_code=200, json=institution_holdings2)
    item_file = io.StringIO("oclcNumber\n318877925\n191865523")  
    csv_read = handle_files.loadCSV(item_file)    
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveHoldingsByOCLCNumber(getTestConfig, csv_read, heldBy=oclcSymbol)
    assert type(result) is pandas.DataFrame 
    final_result = pandas.DataFrame(data={"oclcNumber": [318877925, 191865523], "total_holding_count":[246, 3355], "holding_symbols": ['OCPSB', 'OCPSB'], "status": ['success', 'success']})
    assert_frame_equal(result, final_result)  
    
def test_retrieveSPByOCLCNumber(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    heldInState = "CA"
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=776775878&heldInState=' + heldInState, status_code=200, json=retained_byState)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/bibs-retained-holdings?oclcNumber=1702614&heldInState=' + heldInState, status_code=200, json=retained_byState2)    
    item_file = io.StringIO("oclcNumber\n776775878\n1702614")
    csv_read = handle_files.loadCSV(item_file)    
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveSPByOCLCNumber(getTestConfig, csv_read, heldInState=heldInState)
    assert type(result) is pandas.DataFrame
    final_result = pandas.DataFrame(data={"oclcNumber": [776775878, 1702614], "total_holding_count":[50, 395], "retained_symbols": ['CCO', 'CCO'], "status": ['success', 'success']})
    #assert_frame_equal(result, final_result)        
    
def test_retrieveInstitutionRetentionsbyOCLCNumber(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    oclcSymbol = 'CCO'
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?oclcNumber=776775878&heldBy=' + oclcSymbol, status_code=200, json=retained_bySymbol)
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?oclcNumber=1702614&heldBy=' + oclcSymbol, status_code=200, json=retained_bySymbol2)    
    item_file = io.StringIO("oclcNumber\n776775878\n1702614")
    csv_read = handle_files.loadCSV(item_file)    
    getTestConfig.update({"oauth-session": mockOAuthSession}) 
    result = process_data.retrieveInstitutionRetentionsbyOCLCNumber(getTestConfig, csv_read, oclcSymbol)
    assert type(result) is pandas.DataFrame
    final_result = pandas.DataFrame(data={"oclcNumber": [776775878, 1702614], "accession_numbers":['236528690', '272142932'], "barcodes": [None, None], "locations": [None, None], "status": ['success', 'success']})
    # blanks don't match
    #assert_frame_equal(result, final_result)         

def test_retrieveAllInstitutionRetentions(mockOAuthSession, getTestConfig, tmpdir, requests_mock):
    requests_mock.register_uri('GET', 'https://americas.api.oclc.org/discovery/v1/worldcat/retained-holdings?heldBy=CCO', status_code=200, json=retained_holdings_institution)    
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveAllInstitutionRetentions(getTestConfig, 'CCO')
    assert type(result) is pandas.DataFrame
    final_result = pandas.DataFrame(data={"oclcnumber": ['776775878', '1702614', '16983586', '24134802', '51725778', '2983534', '18026674', '1132109', '10233631', '1310939'], "accession_number":['236528690', '272142932', '272153205', '272159905', '272172660', '272144447', '272156949', '272142620', '272154843', '272145080']})
    assert_frame_equal(result, final_result)      
                                 