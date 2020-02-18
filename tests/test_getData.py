import pytest
import sys
import getData

def testProcessArgs(mocker):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclcNumbers.csv", "--operation", "retrieveMergedOCLCNumbers", "--outputDir", "samples/results"])    
    args = getData.processArgs()
    assert args.itemFile == "samples/oclcNumbers.csv"
    assert args.operation == "retrieveMergedOCLCNumbers"
    assert args.outputDir == "samples/results"                                