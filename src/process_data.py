from src import handle_files
from src import make_requests

import pandas as pd

def retrieveMergedOCLCNumbers(processConfig, item_file, fileInfo):
    csv_read = handle_files.loadCSV(item_file)
    csv_read[['oclcnumber', 'mergedOCNs', 'status']] = csv_read.apply (lambda row: make_requests.getMergedOCLCNumbers(processConfig, row['oclcNumber']), axis=1)    
         
    if (fileInfo['output_dir'] == 's3'):
        return handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read) 
    else:
        return handle_files.saveFileLocal(csv_read, fileInfo['output_dir'])    


def retrieveHoldingsByOCLCNumber(processConfig, item_file, fileInfo, heldByGroup="", heldBy=""):
    csv_read = handle_files.loadCSV(item_file)
    csv_read[['oclcnumber', 'total_holding_count', 'holding_symbols', 'status']] = csv_read.apply (lambda row: make_requests.getHoldings(processConfig, row['oclcNumber'], heldByGroup=heldByGroup, heldBy=heldBy), axis=1)    
         
    if (fileInfo['output_dir'] == 's3'):
        return handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)
    else:
        return handle_files.saveFileLocal(csv_read, fileInfo['output_dir'])

## file contains OCLC Numbers
def retrieveSPByOCLCNumber(processConfig, item_file, fileInfo, heldByGroup="", heldInState=""):  
    csv_read = handle_files.loadCSV(item_file)
    csv_read[['oclcnumber', 'total_holding_count', 'retained_symbols', 'status']] = csv_read.apply (lambda row: make_requests.getRetainedHoldings(processConfig, row['oclcNumber'], heldByGroup=heldByGroup, heldInState=heldInState), axis=1)    
     
    if (fileInfo['output_dir'] == 's3'):
        return handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read) 
    else:
        return handle_files.saveFileLocal(csv_read, fileInfo['output_dir'])

def retrieveInstitutionRetentionsbyOCLCNumber(processConfig, item_file, fileInfo, oclcSymbol):
    csv_read = handle_files.loadCSV(item_file)
    csv_read[['oclcnumber', 'accession_numbers', 'barcodes', 'locations', 'status']] = csv_read.apply (lambda row: make_requests.getMyLibraryRetainedHoldings(processConfig, oclcSymbol, {"type": 'oclcnumber', "value": row['oclcNumber']}), axis=1)
    
    if (fileInfo['output_dir'] == 's3'):
        return handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read) 
    else:
        return handle_files.saveFileLocal(csv_read, fileInfo['output_dir'])

def retrieveAllInstitutionRetentions(processConfig, item_file, fileInfo):    
    csv_read = handle_files.loadCSV(item_file)
    
    for index, row in csv_read.iterrows():
        #make a new file for each institution
        df = pd.DataFrame(columns=['oclcnumber', 'accession_number'])
        retained_holdings = make_requests.getLibraryRetainedHoldings(processConfig, df, row['symbol'])
        
        if (fileInfo['output_dir'] == 's3'):
            return handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_"+ institution_symbol + "_retained", retained_holdings)
        else:
            return handle_files.saveFileLocal(retained_holdings, fileInfo['output_dir'])    