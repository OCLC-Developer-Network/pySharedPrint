import pytest
import sys
import getData
from src import handle_files, process_data, make_requests

def testProcessArgs(mocker):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--operation", "retrieveMergedOCLCNumbers", "--outputDir", "samples/results"])    
    args = getData.processArgs()
    assert args.itemFile == "samples/oclc_numbers.csv"
    assert args.operation == "retrieveMergedOCLCNumbers"
    assert args.outputDir == "samples/results"                   