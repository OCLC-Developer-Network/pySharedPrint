import os
import pytest
import json
import requests_mock
import pandas
import numpy as np
import io

from src import handle_files

def test_readFileFromBucket(s3_bucket, s3_event_payload):
    event = s3_event_payload('test_csv')
    result = handle_files.readFileFromBucket(event)    
    # test file string
    assert type(result) is str
    assert result == "oclcnumber\n2416076\n318877925\n829387251\n55887559\n70775700\n466335791\n713567391\n84838876\n960238778\n893163693"
    
def test_loadCSV():
    item_file = "oclcnumber\n2416076\n318877925\n829387251\n55887559\n70775700\n466335791\n713567391\n84838876\n960238778\n893163693"     
    result = handle_files.loadCSV(io.StringIO(item_file))
    assert type(result) is pandas.DataFrame
    assert list(result.columns.values) == ['oclcnumber']
    
def test_saveFileToBucket(s3_bucket):
    bucket = "mock-test-bucket"
    filename = "saved_file.csv"
    pandasDataFrame = pandas.DataFrame(np.array([["2416076", "2"], ["70775700", "55"]]), columns=['oclcNumber', 'accession_number'])
    result = handle_files.saveFileToBucket(bucket, filename, pandasDataFrame)
    assert result == "success"
    
def test_readFileFromLocal():
    pathToFile = 'samples/oclc_numbers.csv'
    result = handle_files.readFileFromLocal(pathToFile)
    file_string = "oclcNumber\n2416076\n318877925\n829387251\n55887559\n70775700\n466335791\n713567391\n84838876\n960238778\n893163693"
    assert type(result) is str
    #assert result == file_string
    
def test_saveFileLocal(tmpdir):
    pandasDataFrame = pandas.DataFrame(np.array([["2416076", "2"], ["70775700", "55"]]), columns=['oclcNumber', 'accession_number'])
    output_dir = tmpdir / "output.txt"    
    result = handle_files.saveFileLocal(pandasDataFrame, output_dir)
    assert len(tmpdir.listdir()) == 1
    data = pandas.read_csv(output_dir)
    assert list(data.columns.values) == ['oclcNumber', 'accession_number']
    
                 
                                 