## need to import the relevant files
import argparse
import yaml
from src import handle_files, process_data, make_requests
import sys
import string
import os

if os.environ['testConfig']:
    configFile = os.environ['testConfig']
else:
    configFile = 'config.yml'
    
def processArgs():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--itemFile', required=True, help='File you want to process')
        parser.add_argument('--operation', required=True, choices=['retrieveMergedOCLCNumbers', 'retrieveHoldingsByOCLCNumber', 'retrieveSPByOCLCNumber', 'retrieveInstitutionRetentionsbyOCLCNumber', 'retrieveAllInstitutionRetentions'], help='Operation to run: retrieveMergedOCLCNumbers, retrieveHoldingsByOCLCNumber, retrieveSPByOCLCNumber, retrieveInstitutionRetentionsbyOCLCNumber, retrieveAllInstitutionRetentions')    
        parser.add_argument('--outputDir', required=True, help='Directory to save output to')                
        
        if "retrieveInstitutionRetentionsbyOCLCNumber" in sys.argv:
            parser.add_argument('--heldBy', required=True, help='OCLC Symbol to check holdings/retentions for')
        elif "retrieveHoldingsByOCLCNumber" in sys.argv:
            group = parser.add_mutually_exclusive_group(required=True)          
            group.add_argument('--heldBy', help='OCLC Symbol to check holdings/retentions for')
            group.add_argument('--heldByGroup', help='Group OCLC Symbol to check holdings/retentions for')
        elif "retrieveSPByOCLCNumber" in sys.argv:
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument('--heldByGroup', help='Group OCLC Symbol to check holdings/retentions for')
            group.add_argument('--heldInState', help='State to check retentions')
    
        args = parser.parse_args()
        return args
    except SystemExit:
        raise

def process(args):
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    item_file = handle_files.readFileFromLocal(args.itemFile) 
    
    operation = args.operation
    output_dir = args.outputDir
    
    # get a token
    scope = ['wcapi']
    try:
        oauth_session = make_requests.createOAuthSession(config, scope)
    
        config.update({"oauth-session": oauth_session})
        processConfig = config
        csv_read = handle_files.loadCSV(item_file) 
        if operation == "retrieveAllInstitutionRetentions":   
            results = []        
            for index, row in csv_read.iterrows():
                csv_read_institution = process_data.retrieveAllInstitutionRetentions(processConfig, row['symbol'])
                result = handle_files.saveFileLocal(csv_read_institution, output_dir)
                results.append(row['symbol'] + ": " + result)
            
            return ",".join(results)      
        else:
            if operation == "retrieveMergedOCLCNumbers":
                csv_read = process_data.retrieveMergedOCLCNumbers(processConfig, csv_read)
            elif operation == "retrieveHoldingsByOCLCNumber":
                if hasattr(args, 'heldBy'):
                    heldBy = args.heldBy
                elif hasattr(args, 'heldByGroup'):
                    heldByGroup = args.heldByGroup
                csv_read = process_data.retrieveHoldingsByOCLCNumber(processConfig, csv_read, heldByGroup, heldBy)
    
            elif operation == "retrieveSPByOCLCNumber":                
                csv_read = process_data.retrieveSPByOCLCNumber(processConfig, csv_read, heldByGroup, heldInState) 
                if hasattr(args, 'heldByGroup'):
                    heldByGroup = args.heldByGroup
                elif hasattr(args, 'heldInState'):     
                    heldInState = args.heldInState  
            elif operation == "retrieveInstitutionRetentionsbyOCLCNumber":
                heldBy = args.heldBy
                csv_read = process_data.retrieveInstitutionRetentionsbyOCLCNumber(processConfig, csv_read, heldBy)        
        
            return handle_files.saveFileLocal(csv_read, output_dir)

    except BaseException as err:
        result = 'no access token ' + str(err)
        return result   

if __name__ == '__getData__':
    try:
        args = processArgs()
        print(process(args))
    except SystemExit:
        print("Invalid Operation specified")
else:
    try:
        args = processArgs()
        print(process(args))
    except SystemExit:
        print("Invalid Operation specified")
        
    