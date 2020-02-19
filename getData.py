## need to import the relevant files
import argparse
import yaml
from src import handle_files, process_data, make_requests
import sys

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
    
def processArgs():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--itemFile', required=True, help='File you want to process')
        parser.add_argument('--operation', required=True, choices=['retrieveMergedOCLCNumbers', 'retrieveHoldingsByOCLCNumber', 'retrieveSPByOCLCNumber', 'retrieveInstitutionRetentionsbyOCLCNumber', 'retrieveAllInstitutionRetentions'], help='Operation to run: retrieveMergedOCLCNumbers, retrieveHoldingsByOCLCNumber, retrieveSPByOCLCNumber, retrieveInstitutionRetentionsbyOCLCNumber, retrieveAllInstitutionRetentions')    
        parser.add_argument('--outputDir', required=True, help='Directory to save output to')
    
        args = parser.parse_args()
        return args
    except SystemExit:
        raise

def process(args):
    item_file = handle_files.readFileFromLocal(args.itemFile) 
    
    operation = args.operation
    output_dir = args.outputDir
    
    # get a token
    scope = ['DISCOVERY']
    oauth_session = make_requests.createOAuthSession(config, scope)
    
    processConfig = config.update({"oauth-session": oauth_session})
    
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
            csv_read = process_data.retrieveHoldingsByOCLCNumber(processConfig, csv_read)
        elif operation == "retrieveSPByOCLCNumber":
            csv_read = process_data.retrieveSPByOCLCNumber(processConfig, csv_read)
        elif operation == "retrieveInstitutionRetentionsbyOCLCNumber":
            csv_read = process_data.retrieveInstitutionRetentionsbyOCLCNumber(processConfig, csv_read)        
    
        return handle_files.saveFileLocal(csv_read, output_dir)
    

if __name__ == '__getData__':
    try:
        args = processArgs()
        print(process(args))
    except SystemExit:
        print("Invalid Operation specified")    
    