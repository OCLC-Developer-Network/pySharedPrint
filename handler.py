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
    return process_data.retrieveMergedOCLCNumbers(processConfig, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})

## file contains OCLC Numbers
def checkHoldingsByOCLCNumber(event, context):      
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveHoldingsByOCLCNumber(processConfig, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})

## file contains OCLC Numbers
def checkSPByOCLCNumber(event, context):  
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveSPbyOCLCNumber(processConfig, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})

## file contains OCLC Numbers
def checkInstitutionRetentionsbyOCLCNumber(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveInstitutionRetentionsbyOCLCNumber(processConfig, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})    

## file contains OCLC Symbols
def getInstitutionRetentions(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveAllInstitutionRetentions(processConfig, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})    
  