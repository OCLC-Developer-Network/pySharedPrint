import pytest
import sys
import io
import getData
from src import handle_files, process_data, make_requests

def testProcessArgs(mocker):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--operation", "retrieveMergedOCLCNumbers", "--outputDir", "samples/results"])    
    args = getData.processArgs()
    assert args.itemFile == "samples/oclc_numbers.csv"
    assert args.operation == "retrieveMergedOCLCNumbers"
    assert args.outputDir == "samples/results"                   

def testProcessWrongOperation(mocker, capfd):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--operation", "junkrequest", "--outputDir", "samples/results"])    
    with pytest.raises(SystemExit):
        args = getData.processArgs()
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err
    assert "{retrieveMergedOCLCNumbers,retrieveHoldingsByOCLCNumber,retrieveSPByOCLCNumber,retrieveInstitutionRetentionsbyOCLCNumber,retrieveAllInstitutionRetentions}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: argument --operation: invalid choice: 'junkrequest' (choose from 'retrieveMergedOCLCNumbers', 'retrieveHoldingsByOCLCNumber', 'retrieveSPByOCLCNumber', 'retrieveInstitutionRetentionsbyOCLCNumber', 'retrieveAllInstitutionRetentions')" in captured.err  
        
def testProcessMissingArgumentItemFile(mocker, capfd):
    mocker.patch('sys.argv', ["", "--operation", "retrieveMergedOCLCNumbers", "--outputDir", "samples/results"])    
    with pytest.raises(SystemExit):
        args = getData.processArgs()
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err
    assert "{retrieveMergedOCLCNumbers,retrieveHoldingsByOCLCNumber,retrieveSPByOCLCNumber,retrieveInstitutionRetentionsbyOCLCNumber,retrieveAllInstitutionRetentions}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: the following arguments are required: --itemFile" in captured.err         
        
def testProcessMissingArgumentOperation(mocker, capfd):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--outputDir", "samples/results"])    
    with pytest.raises(SystemExit):
        args = getData.processArgs()
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err
    assert "{retrieveMergedOCLCNumbers,retrieveHoldingsByOCLCNumber,retrieveSPByOCLCNumber,retrieveInstitutionRetentionsbyOCLCNumber,retrieveAllInstitutionRetentions}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: the following arguments are required: --operation" in captured.err     
        
def testProcessMissingArgumentOutputDir(mocker, capfd):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--operation", "retrieveMergedOCLCNumbers"])    
    with pytest.raises(SystemExit):
        args = getData.processArgs() 
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err 
    assert "{retrieveMergedOCLCNumbers,retrieveHoldingsByOCLCNumber,retrieveSPByOCLCNumber,retrieveInstitutionRetentionsbyOCLCNumber,retrieveAllInstitutionRetentions}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: the following arguments are required: --outputDir" in captured.err
    
def testProcessRetrieveMergedOCLCNumbers(mocker, mockOAuthSession):
    mocker.patch("src.handle_files.readFileFromLocal", return_value=io.StringIO("oclcNumber\n2416076\n318877925\n829387251\n55887559\n70775700\n466335791\n713567391\n84838876\n960238778\n893163693"))
    mocker.patch("src.make_requests.createOAuthSession", return_value=mockOAuthSession)
    mocker.patch('src.process_data.retrieveMergedOCLCNumbers', return_value='success')
    mocker.patch('src.handle_files.saveFileLocal', return_value='success')
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--operation", "retrieveMergedOCLCNumbers", "--outputDir", "samples/results"])    
    args = getData.processArgs()
    result = getData.process(args);
    assert result == 'success'
    
# def testProcessRetrieveHoldingsByOCLCNumber(mocker):
#     args = ""
#     result = getData.process(args);
#     
# def testProcessRetrieveSPByOCLCNumber(mocker):
#     args = ""
#     result = getData.process(args);
#     
# def testProcessRetrieveInstitutionRetentionsbyOCLCNumber(mocker):
#     args = ""
#     result = getData.process(args);
#     
# def testProcessRetrieveAllInstitutionRetentions(mocker):
#     args = ""
#     result = getData.process(args);      