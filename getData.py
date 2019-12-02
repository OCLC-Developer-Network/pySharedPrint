## need to import the relevant files
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--itemFile', required=True, help='File you want to process')
parser.add_argument('--operation', required=True, choices=['retrieveMergedOCLCNumbers', 'retrieveHoldingsByOCLCNumber', 'retrieveSPByOCLCNumber', 'retrieveInstitutionRetentionsbyOCLCNumber', 'retrieveAllInstitutionRetentions'], help='Operation to run: retrieveMergedOCLCNumbers, retrieveHoldingsByOCLCNumber, retrieveSPByOCLCNumber, retrieveInstitutionRetentionsbyOCLCNumber, retrieveAllInstitutionRetentions')    
parser.add_argument('--outputDir', required=True, help='Directory to save output to')

args = parser.parse_args()

item_file = readFileFromLocal(args.itemFile) 

operation = args.operation
output_dir = args.outputDir
       
if operation == "retrieveMergedOCLCNumbers":
    result = retrieveMergedOCLCNumbers(item_file, {"output_dir": output_dir})
elif operation == "retrieveHoldingsByOCLCNumber":
    result = retrieveHoldingsByOCLCNumber(item_file, {"output_dir": output_dir})
elif operation == "retrieveSPByOCLCNumber":
    result = retrieveSPByOCLCNumber(item_file, {"output_dir": output_dir})
elif operation == "retrieveInstitutionRetentionsbyOCLCNumber":
    result = retrieveInstitutionRetentionsbyOCLCNumber(item_file, {"output_dir": output_dir})
elif operation == "retrieveAllInstitutionRetentions":
    result = retrieveAllInstitutionRetentions(item_file, {"output_dir": output_dir})
else:
    result = "Operation not specified"

return result