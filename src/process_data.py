from src import handle_files
from src import make_requests

import pandas as pd

def retrieveMergedOCLCNumbers(processConfig, csv_read):
    csv_read[['oclcNumber', 'mergedOCNs', 'status']] = csv_read.apply (lambda row: make_requests.getMergedOCLCNumbers(processConfig, row['oclcNumber']), axis=1)    
    return csv_read         


def retrieveHoldingsByOCLCNumber(processConfig, csv_read, heldByGroup="", heldBy=""):
    csv_read[['oclcNumber', 'total_holding_count', 'holding_symbols', 'status']] = csv_read.apply (lambda row: make_requests.getHoldings(processConfig, row['oclcNumber'], heldByGroup=heldByGroup, heldBy=heldBy), axis=1)    
         
    return csv_read

## file contains OCLC Numbers
def retrieveSPByOCLCNumber(processConfig, csv_read, heldByGroup="", heldInState=""):  
    csv_read[['oclcNumber', 'total_holding_count', 'retained_symbols', 'status']] = csv_read.apply (lambda row: make_requests.getRetainedHoldings(processConfig, row['oclcNumber'], heldByGroup=heldByGroup, heldInState=heldInState), axis=1)    
     
    return csv_read

def retrieveInstitutionRetentionsbyOCLCNumber(processConfig, csv_read, oclcSymbol):
    csv_read[['oclcNumber', 'accession_numbers', 'barcodes', 'locations', 'status']] = csv_read.apply (lambda row: make_requests.getMyLibraryRetainedHoldings(processConfig, oclcSymbol, {"type": 'oclcnumber', "value": row['oclcNumber']}), axis=1)
    
    return csv_read

def retrieveAllInstitutionRetentions(processConfig, oclcSymbol):        
    #make a new file for each institution
    df = pd.DataFrame(columns=['oclcnumber', 'accession_number'])
    retained_holdings = make_requests.getLibraryRetainedHoldings(processConfig, df, oclcSymbol)
    return retained_holdings            