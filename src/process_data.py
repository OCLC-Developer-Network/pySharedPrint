from .handle_files import *
from .make_requests import *

import pandas as pd

def retrieveMergedOCLCNumbers(oauth_session, item_file, fileInfo):
    csv_read = loadCSV(item_file)
    csv_read[['oclcnumber', 'mergedOCNs']] = csv_read.apply (lambda row: make_requests.getMergedOCLCNumbers(row['oclcNumber']), axis=1)    
         
    if (fileInfo['output_dir'] == 's3'):
        return saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read) 
    else:
        return saveFileLocal(csv_read, fileInfo['output_dir'])    


def retrieveHoldingsByOCLCNumber(oauth_session, item_file, fileInfo):
    csv_read = loadCSV(item_file)
    csv_read[['oclcnumber', 'total_holding_count', 'holding_symbols', 'status']] = csv_read.apply (lambda row: make_requests.getHoldings(row['oclcNumber']), axis=1)    
         
    if (fileInfo['output_dir'] == 's3'):
        return saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)
    else:
        return saveFileLocal(csv_read, fileInfo['output_dir'])

## file contains OCLC Numbers
def retrieveSPByOCLCNumber(oauth_session, item_file, fileInfo):  
    csv_read = loadCSV(item_file)
    csv_read[['oclcnumber', 'total_holding_count', 'retained_symbols', 'status']] = csv_read.apply (lambda row: make_requests.getRetainedHoldings(row['oclcNumber']), axis=1)    
     
    if (fileInfo['output_dir'] == 's3'):
        return saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read) 
    else:
        return saveFileLocal(csv_read, fileInfo['output_dir'])

def retrieveInstitutionRetentionsbyOCLCNumber(oauth_session, item_file, fileInfo):
    csv_read = loadCSV(item_file)
    csv_read[['oclcnumber', 'accession_numbers', 'barcodes' 'locations', 'status']] = csv_read.apply (lambda row: make_requests.getMyLibraryRetainedHoldings(row['oclcNumber']), axis=1)
    
    if (fileInfo['output_dir'] == 's3'):
        return saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read) 
    else:
        return saveFileLocal(csv_read, fileInfo['output_dir'])

def retrieveAllInstitutionRetentions(oauth_session, item_file, fileInfo):    
    csv_read = loadCSV(item_file)
    
    for index, row in csv_read.iterrows():
        #make a new file for each institution
        df = pd.DataFrame(columns=['oclcnumber', 'accession_number'])
        retained_holdings = make_requests.getLibraryRetainedHoldings(df, institution_symbol)
        
        if (fileInfo['output_dir'] == 's3'):
            return saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_"+ institution_symbol + "_retained", retained_holdings)
        else:
            return saveFileLocal(retained_holdings, fileInfo['output_dir'])    