from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import pandas as pd  
import json
import requests

def createOAuthSession(config, scope):
    auth = HTTPBasicAuth(config.get('key'), config.get('secret'))
    client = BackendApplicationClient(client_id=config.get('key'), scope=scope)
    oauth_session = OAuth2Session(client=client)
    try:
        token = oauth_session.fetch_token(token_url=config.get('token_url'), auth=auth)
        return oauth_session
    except BaseException as err:
        return err
    
def getMergedOCLCNumbers(config, oclcnumber):
    oauth_session = config.get('oauth-session')
    try:
        r = oauth_session.get(config.get('discovery_service_url') + config.get('base_path') +"/bibs/" + oclcnumber, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('identifier').get('mergedOclcNumbers'):
                mergedOCLCNumbers = ",".join(result.get('identifier').get('mergedOclcNumbers'))
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

def getBriefHoldings(config, oclcnumber, heldInCountry):
    oauth_session = config.get('oauth-session')
    try:
        r = oauth_session.get(config.get('discovery_service_url') + config.get('base_path') +"/bibs-holdings?oclcNumber=" + oclcnumber + "&heldInCountry=" + heldInCountry, headers={"Accept":"application/json"})
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

def getHoldings(config, oclcnumber, heldByGroup="", heldby=""):
    oauth_session = config.get('oauth-session')
    try:
        request_url = config.get('discovery_service_url') + config.get('base_path') + "/bibs-detailed-holdings?oclcNumber=" + oclcnumber
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

def getRetainedHoldings(config, oclcnumber, heldByGroup="", heldInState=""):
    oauth_session = config.get('oauth-session')
    request_url = config.get('discovery_service_url') + config.get('base_path') + "/bibs-retained-holdings?oclcNumber=" + oclcnumber
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

def getMyLibraryHoldings(config, identifierType, identifierValue):
    oauth_session = config.get('oauth-session')
    request_url = config.get('discovery_service_url') + config.get('base_path') + "/my-holdings"
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
        
        
def getMyLibraryRetainedHoldings(config, oclcSymbol, identifier):
    oauth_session = config.get('oauth-session')
    request_url = config.get('discovery_service_url') + config.get('base_path') + "/retained-holdings?heldBy=" + oclcSymbol
    if identifier['type'] == "oclcnumber":
        request_url += "&oclcNumber=" + identifier['value']
    elif identifier['type'] == "barcode":
        request_url += "&barcode=" + identifier['value']
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
                
                lhrHoldingParts = [i for i in lhrHoldingParts if i]                 
                holdingParts = [y for x in lhrHoldingParts for y in x]
                       
                barcodeList = map(lambda row: row.get('pieceDesignation'), holdingParts)
                barcodeList = list(set(barcodeList))
                barcodes = ",".join(item for item in barcodeList if item)
                
                oclcnumberList = map(lambda row: row.get('oclcNumber'), LHRList)
                oclcnumberList = list(set(oclcnumberList))
                oclcnumbers = ",".join(oclcnumberList)
                
                holdingsList = map(lambda row: parseLocation(row), LHRList)
                holdingsList = list(set(holdingsList))
                retained_holdings = ",".join(holdingsList) 
            else:
                accession_numbers = ""
                barcodes = ""
                oclcnumbers = ""
                retained_holdings = "none"                
            status = "success"
        except json.decoder.JSONDecodeError:
            accession_numbers = ""
            barcodes = ""
            oclcnumbers = ""
            retained_holdings = "none"                  
            status = "failed"
    except requests.exceptions.HTTPError as err:
        accession_numbers = ""
        barcodes = ""
        oclcnumbers = ""
        retained_holdings = "none"      
        status = "failed"
    return pd.Series([oclcnumbers, accession_numbers, barcodes, retained_holdings, status])
    
def getLibraryRetainedHoldings(config, df, oclc_symbol):
    oauth_session = config.get('oauth-session')
    request_url = config.get('discovery_service_url') + config.get('base_path') + "/retained-holdings?heldBy=" + oclc_symbol
    try:
        r = oauth_session.get(request_url, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            if result.get('detailedHoldings'):
                for lhr in result.get('detailedHoldings'):
                    lhrset = pd.Series(data=[lhr.get('oclcNumber'), lhr.get('lhrControlNumber')], index=['oclcnumber', 'accession_number'])
                    df = pd.concat([df, lhrset.to_frame().T], ignore_index=True)
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

def parseLocation(LHR):
    if LHR.get('location').get('holdingLocation') and LHR.get('location').get('sublocationCollection') and LHR.get('location').get('shelvingLocation'):
        location = LHR.get('location').get('holdingLocation') + "-" + LHR.get('location').get('sublocationCollection') + "-" + LHR.get('location').get('shelvingLocation')
    else:
        location = ""    
    return location  