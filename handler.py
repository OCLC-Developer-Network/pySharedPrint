import boto3
import yaml
import json
import pandas as pd  
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import requests
import pymarc
from pymarc import Record, Field
import os
from io import StringIO
import time
from xml.etree import ElementTree
from docutils.nodes import row
from botocore.vendored.requests.api import request
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

credentials = boto3.Session().get_credentials()

s3 = boto3.client('s3')

# load key/secret config info
# read a configuration file
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
    
serviceURL = config.get('discovery_service_url')
base_path = config.get('base_path')  
institution_symbol = config.get('institution_symbol')  
# get a token
scope = ['DISCOVERY']
auth = HTTPBasicAuth(config.get('key'), config.get('secret'))
client = BackendApplicationClient(client_id=config.get('key'), scope=scope)
oauth_session = OAuth2Session(client=client)

try:
    token = oauth_session.fetch_token(token_url=config.get('token_url'), auth=auth)
except BaseException as err:
    print(err)
    
def getBriefHoldings(oclcnumber, heldInCountry):
    try:
        r = oauth_session.get(serviceURL + base_path +"/bibs-holdings?oclcNumber=" + oclcnumber + "&heldInCountry=" + heldInCountry, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('briefRecords') and result.get('briefRecords')[0].get('institutionHolding').get('briefHoldings'):
                holdingsList = map(lambda row: row.get('oclcSymbol'), result.get('briefRecords')[0].get('institutionHolding').get('briefHoldings'))
                holdings = ",".join(holdingsList)            
            else:
                holdings = ""    
            total_holding_count = result.get('briefRecords')[0].get('institutionHolding').get('totalHoldingCount')
            status = "success"
        except json.decoder.JSONDecodeError:
            new_oclc_number = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        new_oclc_number = ""
        status = "failed"
    return pd.Series([oclcnumber, total_holding_count, holdings, status])

def getHoldings(oclcnumber, heldByGroup="", heldby=institution_symbol):
    try:
        request_url = serviceURL + base_path +"/bibs-detailed-holdings?oclcNumber=" + oclcnumber
        if heldByGroup:
             request_url +="&heldByGroup=" + heldByGroup
        else:
            request_url +="&heldBy=" + heldby
        r = oauth_session.get(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('briefRecords') and result.get('briefRecords')[0].get('institutionHolding').get('detailedHoldings'):
                holdingsList = map(lambda row: row.get('location').get('holdingLocation'), result.get('briefRecords')[0].get('institutionHolding').get('detailedHoldings'))
                holdingsList = list(set(holdingsList))
                holdings = ",".join(holdingsList)                
            else:                
                holdings = ""
            total_holding_count = result.get('briefRecords')[0].get('institutionHolding').get('totalHoldingCount')
            status = "success"
        except json.decoder.JSONDecodeError:
            new_oclc_number = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        new_oclc_number = ""
        status = "failed"
    return pd.Series([oclcnumber, total_holding_count, holdings, status])

def getRetainedHoldings(oclcnumber, heldByGroup="", heldInState=""):
    request_url = serviceURL + base_path + "/bibs-retained-holdings?oclcNumber=" + oclcnumber
    if heldByGroup:
        request_url +="&heldByGroup=" + heldByGroup
    elif heldInState:
        request_url +="&heldInState=" + heldInState
    else:
        #throw exception
        request_url = request_url
        
    try:
        r = oauth_session.get(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('briefRecords') and result.get('briefRecords')[0].get('institutionHolding').get('detailedHoldings'):
                retained_holdingsList = map(lambda row: row.get('location').get('holdingLocation'), result.get('briefRecords')[0].get('institutionHolding').get('detailedHoldings'))
                retained_holdings = ",".join(retained_holdingsList)
            else:
                retained_holdings = ""
            total_holding_count = result.get('briefRecords')[0].get('institutionHolding').get('totalHoldingCount')
            status = "success"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"
    return pd.Series([oclcnumber, total_holding_count, retained_holdings, status]) 

def getMyLibraryHoldings(accession_number, oclcnumber, barcode):
    request_url = serviceURL + base_path + "/my-holdings"
    if oclcNumber:
        request_url += "?oclcNumber=" + oclcnumber
    elif barcode:
        request_url += "?barcode=" + barcode
    elif accession_number:
        request_url += '/' + accession_number
    else:
        request_url = request_url
        
        
def getMyLibraryRetainedHoldings(oclcnumber, barcode):
    request_url = serviceURL + base_path + "/retained-holdings"
    if oclcNumber:
        request_url += "?oclcNumber=" + oclcnumber
    elif barcode:
        request_url += "?barcode=" + barcode
    else:
        request_url = request_url
        
    try:
        r = oauth_session.post(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('briefRecords') and result.get('briefRecords')[0].get('institutionHolding'):
                retained_holdingsList = map(lambda row: row.get('location').get('holdingLocation'), result.get('briefRecords')[0].get('institutionHolding').get('detailedHoldings'))
                retained_holdings = ",".join(retained_holdingsList)
            else:
                retained_holdings = "none";  
            total_holding_count = result.get('briefRecords')[0].get('institutionHolding').get('totalHoldingCount')              
            status = "success"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"
    return pd.Series([oclcnumber, total_holding_count, retained_holdings, status])
    
    
def saveFile(bucket, filename, csv_dict):
    csv_buffer = StringIO()    
    csv_dict.to_csv(csv_buffer, sep="|", index=False)

    try:
        write_response = s3.put_object(Bucket=bucket, key= filename, Body=csv_buffer.getvalue())
        return "success"
    except ClientError as err:
        error_message = "Operation complete - output write failed"
        if err.response['Error']['Code']:
            error_message += err.response['Error']['Code']
        return error_message 

def checkHoldingsByOCLCNumber(event, context):  
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, sep="|", dtype={'Item_Call_Number': 'object'}, index_col=False)
    csv_read[['oclcnumber', 'total_holding_count', 'holding_symbols', 'status']] = csv_read.apply (lambda row: getHoldings(row['oclcNumber']), axis=1)    
         
    return saveFile(bucket, key + "_updated", csv_read)    

def checkSPByOCLCNumber(event, context):  
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, sep="|", dtype={'Item_Call_Number': 'object'}, index_col=False)
    csv_read[['oclcnumber', 'total_holding_count', 'retained_symbols', 'status']] = csv_read.apply (lambda row: getRetainedHoldings(row['oclcNumber']), axis=1)    
     
    return saveFile(bucket, key + "_updated", csv_read)
  