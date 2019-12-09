import pytest
import json
import requests_mock

from src import process_data

def test_retrieveMergedOCLCNumbers():
    result = retrieveMergedOCLCNumbers(processConfig, item_file, fileInfo)
                              
def test_retrieveHoldingsByOCLCNumber(): 
    result = retrieveHoldingsByOCLCNumber(processConfig, item_file, fileInfo)
    
def test_retrieveSPByOCLCNumber():
    result = retrieveSPByOCLCNumber(processConfig, item_file, fileInfo)
    
def test_retrieveInstitutionRetentionsbyOCLCNumber(): 
    result = retrieveInstitutionRetentionsbyOCLCNumber(processConfig, item_file, fileInfo)

def test_retrieveAllInstitutionRetentions():
    retrieveAllInstitutionRetentions(processConfig, item_file, fileInfo)       
                                 