## need to import the relevant files
import argparse
import yaml
from src import handle_files, process_data, make_requests
parser = argparse.ArgumentParser()
parser.add_argument('--itemFile', required=True, help='File you want to process')
parser.add_argument('--operation', required=True, choices=['retrieveMergedOCLCNumbers', 'retrieveHoldingsByOCLCNumber', 'retrieveSPByOCLCNumber', 'retrieveInstitutionRetentionsbyOCLCNumber', 'retrieveAllInstitutionRetentions'], help='Operation to run: retrieveMergedOCLCNumbers, retrieveHoldingsByOCLCNumber, retrieveSPByOCLCNumber, retrieveInstitutionRetentionsbyOCLCNumber, retrieveAllInstitutionRetentions')    
parser.add_argument('--outputDir', required=True, help='Directory to save output to')

args = parser.parse_args()

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

def process(args):
    item_file = handle_files.readFileFromLocal(args.itemFile) 
    
    operation = args.operation
    output_dir = args.outputDir
    
    # get a token
    scope = ['DISCOVERY']
    oauth_session = make_requests.createOAuthSession(key, secret, scope)
    
    processConfig = config.update({"oauth-session": oauth_session})
           
    if operation == "retrieveMergedOCLCNumbers":
        result = process_data.retrieveMergedOCLCNumbers(processConfig, item_file, {"output_dir": output_dir})
    elif operation == "retrieveHoldingsByOCLCNumber":
        result = process_data.retrieveHoldingsByOCLCNumber(processConfig, item_file, {"output_dir": output_dir})
    elif operation == "retrieveSPByOCLCNumber":
        result = process_data.retrieveSPByOCLCNumber(processConfig, item_file, {"output_dir": output_dir})
    elif operation == "retrieveInstitutionRetentionsbyOCLCNumber":
        result = process_data.retrieveInstitutionRetentionsbyOCLCNumber(processConfig, item_file, {"output_dir": output_dir})
    elif operation == "retrieveAllInstitutionRetentions":
        result = process_data.retrieveAllInstitutionRetentions(processConfig, item_file, {"output_dir": output_dir})
    else:
        result = "Operation not specified"
    
    return result

process(args)