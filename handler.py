import yaml
import os
from src import handle_files, process_data, make_requests
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# load key/secret config info
# read a configuration file
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
     
# get a token
scope = ['DISCOVERY']
oauth_session = make_requests.createOAuthSession(config, scope)

processConfig = config.update({"oauth-session": oauth_session})

def getMergedOCLCNumbers(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.retrieveMergedOCLCNumbers(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)

## file contains OCLC Numbers
def checkHoldingsByOCLCNumber(event, context):      
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.retrieveHoldingsByOCLCNumber(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)

## file contains OCLC Numbers
def checkSPByOCLCNumber(event, context):  
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.retrieveSPbyOCLCNumber(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)

## file contains OCLC Numbers
def checkInstitutionRetentionsbyOCLCNumber(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.retrieveInstitutionRetentionsbyOCLCNumber(processConfig, csv_read) 
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)   

## file contains OCLC Symbols
def getInstitutionRetentions(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)  
    results = []  
    for index, row in csv_read.iterrows():
        retained_holdings = process_data.retrieveAllInstitutionRetentions(processConfig, row['symbol'])
        result = handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_"+ row['symbol'] + "_retained", retained_holdings)
        results.append(row['symbol'] + ": " + result)
    
    return ",".join(results)    
  