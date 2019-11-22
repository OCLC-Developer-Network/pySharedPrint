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
from cffi.ffiplatform import flatten
from StdSuites.AppleScript_Suite import event
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

def getMergedOCLCNumbers(oclcnumber):
    try:
        r = oauth_session.get(serviceURL + base_path +"/bibs/" + oclcnumber, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if mergedOCLCNumbers:
                mergedOCLCNumbers = ""
            else:
                mergedOCLCNumbers = ""
            status = "success"
        except json.decoder.JSONDecodeError:
            mergedOCLCNumbers = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        mergedOCLCNumbers = ""
        status = "failed"
    return pd.Series([oclcnumber, mergedOCLCNumbers, status])        

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
            oclcnumber = ""
            holdingsList = "none" 
            total_holding_count = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        oclcnumber = ""
        holdingsList = "none" 
        total_holding_count = ""
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
            oclcnumber = ""
            holdingsList = "none" 
            total_holding_count = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        oclcnumber = ""
        holdingsList = "none" 
        total_holding_count = ""
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
            oclcnumber = ""
            retained_holdings = "none" 
            total_holding_count = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        oclcnumber = ""
        retained_holdings = "none" 
        total_holding_count = ""
        status = "failed"
    return pd.Series([oclcnumber, total_holding_count, retained_holdings, status]) 

def getMyLibraryHoldings(identifierType, identifierValue):
    request_url = serviceURL + base_path + "/retained-holdings"
    if identifierType == "oclcnumber":
        request_url += "?oclcNumber=" + identifierValue
    elif identifierType == "barcode":
        request_url += "?barcode=" + identifierValue
    elif identifierType == "accession_number":
        request_url += '/' + identifierValue
    else:
        request_url = request_url

    try:
        r = oauth_session.get(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('detailedHoldings'):
                LHRList = result.get('detailedHoldings')
                accession_numberList = map(lambda row: row.get('lhrControlNumber'), LHRList)
                accession_numbers = ",".join(accession_numberList)
                
                lhrHoldingParts = list(map(lambda row: row.get('holdingParts'), LHRList))
                holdingParts = [y for x in lhrHoldingParts for y in x]
                       
                barcodeList = map(lambda row: row.get('pieceDesignation'), holdingParts)
                barcodeList = list(set(barcodeList))
                barcodes = ",".join(item for item in barcodeList if item)
                
                oclcnumberList = map(lambda row: row.get('oclcNumber'), LHRList)
                oclcnumberList = list(set(oclcnumberList))
                oclcnumbers = ",".join(oclcnumberList)
                
                holdingsList = map(lambda row: row.get('location').get('holdingLocation') + "-" + row.get('location').get('sublocationCollection') + "-" + row.get('location').get('shelvingLocation'), LHRList)
                holdingsList = list(set(holdingsList))
                holdings = ",".join(holdingsList)  
            elif result.get('lhrControlNumber'):
                accession_numbers = result.get('lhrControlNumber');
                barcodeList = map(lambda row: row.get('pieceDesignation'), result.get('holdingParts'))
                barcodes = ",".join(item for item in barcodeList if item)
                oclcnumbers = result.get('oclcNumber')
                holdings = result.get('location').get('holdingLocation') + "-" + result.get('location').get('sublocationCollection') + "-" + result.get('location').get('shelvingLocation')                
            
            else:
                accession_numbers = ""
                barcodes = ""
                oclcnumbers = ""               
                holdings = "none";
            total_holding_count = result.get('numberOfHoldings')              
            status = "success"
        except json.decoder.JSONDecodeError:
            accession_numbers = ""
            barcodes = ""
            oclcnumbers = ""
            holdings = "none" 
            total_holding_count = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        accession_numbers = ""
        barcodes = ""
        oclcnumbers = ""
        holdings = "none" 
        total_holding_count = ""
        status = "failed"
    return pd.Series([oclcnumbers, accession_numbers, barcodes, total_holding_count, holdings, status])        
        
        
def getMyLibraryRetainedHoldings(oclcnumber, barcode):
    request_url = serviceURL + base_path + "/retained-holdings"
    if oclcNumber:
        request_url += "?oclcNumber=" + oclcnumber
    elif barcode:
        request_url += "?barcode=" + barcode
    else:
        request_url = request_url
        
    try:
        r = oauth_session.get(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('detailedHoldings'):
                accession_number = ""
                barcode = ""
                oclcnumber = ""
                holdingsList = map(lambda row: row.get('holdingLocation') + "-" + row.get('holdingLocation').get('sublocationCollection') + "-" + row.get('holdingLocation').get('sublocationCollection').get('shelvingLocation'), result.get('detailedHoldings').get('location'))
                retained_holdings = ",".join(retained_holdingsList)
            else:
                accession_number = ""
                barcode = ""
                oclcnumber = ""
                retained_holdings = "none"  
            total_holding_count = result.get('numberOfHoldings')              
            status = "success"
        except json.decoder.JSONDecodeError:
            accession_number = ""
            barcode = ""
            oclcnumber = ""
            retained_holdings = "none" 
            total_holding_count = ""                         
            status = "failed"
    except requests.exceptions.HTTPError as err:
        accession_number = ""
        barcode = ""
        oclcnumber = ""
        retained_holdings = "none" 
        total_holding_count = ""       
        status = "failed"
    return pd.Series([oclcnumber, accession_number, barcode, total_holding_count, holdingsList, status])
    
def getLibraryRetainedHoldings(df, oclc_symbol):
    request_url = serviceURL + base_path + "/retained-holdings"
    try:
        r = oauth_session.get(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('detailedHoldings'):
                df['oclcnumber', 'lhr_accession_number'] = pd.Series[oclcnumber, accession_number]
                 
            else:
                oclcnumber = ""
                accession_number = ""                              
            status = "success"
        except json.decoder.JSONDecodeError:
            oclcnumber = ""
            accession_number = ""                        
            status = "failed"
    except requests.exceptions.HTTPError as err:
        accession_number = ""
        oclcnumber = ""       
        status = "failed"
    
    return df       


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

def checkInstitutionRetentions (event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, sep="|", dtype={'Item_Call_Number': 'object'}, index_col=False)
    
    for index, row in csv_read.iterrows():
        #make a new file for each institution
        df = pd.DataFrame(columns=['oclcnumber', 'accession_number'])
        retained_holdings = getLibraryRetainedHoldings(df, institution_symbol)
        saveFile(bucket, key + "_"+ institution_symbol + "_retained", retained_holdings)    
  