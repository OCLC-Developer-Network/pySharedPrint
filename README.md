# Shared Print examples

Custom application looks for new files in particular folders an S3 bucket and interacts with the API for shared print data based on the data in the delimited file

## Supposed use cases

Obtained list of libraries holding given OCLC Number

Obtain list of libraries with retention by OCLC Number by group or state
- Library identifies a group of records that are no longer in their library (e.g. via an inventory project) or have become damaged (e.g. water damage), and wishes to see who else in EAST owns these records, and if any of them are already under retention.  If under retention elsewhere retrieve 583 |3 (holdings). 


Obtain retained holdings for OCLC Symbol given by OCLC Number
- Confirm retentions in local catalog match what is recorded in OCLC.  (Search list of OCLC numbers and see if Shared Print flag set for that library) 


Obtain retained holdings for OCLC Symbol
How many unique retentions does a library have?   Are any of those uniquely held in EAST retained in other programs?  Also confirm number held in US (is it really rare or not). (Search list of OCLC numbers and return number of EAST retentions, other retentions and US holdings on each.)

Retrieve all OCLC numbers (current and merged record numbers) associated with a retention.  

## Installing Locally

### Step 1: Clone the repository
Clone this repository

```bash
$ git clone {url}
```
or download directly from GitHub.

Change into the application directory

### Step 2: Setup Virtual Environment

```
$ python -m venv venv
$ . venv/bin/activate
```

### Step 3: Install python dependencies

```
pip install -r requirements.txt
```

### Step 4: Run local tests

```
python -m pytest
```

### Step 5: Run code locally

```
python checkHoldingsByOCLCNumber.py

python checkSPByOCLCNumber.py

python checkInstitutionRetentionsbyOCLCNumber.py

python getInstitutionRetentions.py


```

## Running in AWS Lambda

### Step 1: Use npm to install dependencies needed to deploy code
Download node and npm and use the `install` command to read the dependencies JSON file 

```bash
$ npm install
```

### Step 2: AWS Setup

1. Install AWS Command line tools
- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
I recommend using pip.
2. Create an AWS user in IAM console. Give it appropriate permissions. Copy the key and secret for this user to use in the CLI. 
3. Configure the command line tools - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

- Make sure you add 
-- key/secret
-- region
    
### Step 3: Create an S3 Bucket for the files
1. Use the AWS Console to create a bucket. Note your bucket name!!!
2. Create folder collection_analysis/
3. Add a sample csv file named holdingsByOCLCNumber.csv with data to check for holdings
4.Add a sample csv file named retainedholdingsByOCLCNumber.csv with data to check for retained holdings


### Step 4: Test application locally
1. Alter s3-getHoldings.json to point to your bucket and your sample txt file.

2. Use serverless to test locally

```bash
serverless invoke local --function findUsers --path s3-getHoldings.json
```

3. Alter s3-getRetainedHoldings.json to point to your bucket and your sample csv file.

4. Use serverless to test locally

```bash
serverless invoke local --function getUsers --path s3-getRetainedHoldings.json
```

### Step 5: Deploy the code using serverless

```bash
$ serverless deploy
```
