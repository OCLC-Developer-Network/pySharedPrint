import boto3
import yaml
import os
from src import handle_files, process_data, make_requests
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

credentials = boto3.Session().get_credentials()

s3 = boto3.client('s3')

# load key/secret config info
# read a configuration file
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
     
# get a token
scope = ['DISCOVERY']
oauth_session = make_requests.createOAuthSession(key, secret, scope)

def getMergedOCLCNumbers(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveMergedOCLCNumbers(oauth_session, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})

## file contains OCLC Numbers
def checkHoldingsByOCLCNumber(event, context):      
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveHoldingsByOCLCNumber(oauth_session, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})

## file contains OCLC Numbers
def checkSPByOCLCNumber(event, context):  
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveSPbyOCLCNumber(oauth_session, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})

## file contains OCLC Numbers
def checkInstitutionRetentionsbyOCLCNumber(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveInstitutionRetentionsbyOCLCNumber(oauth_session, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})    

## file contains OCLC Symbols
def getInstitutionRetentions(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    return process_data.retrieveAllInstitutionRetentions(oauth_session, item_file, {"bucket": bucket, "key": key, "output_dir":'s3'})    
  