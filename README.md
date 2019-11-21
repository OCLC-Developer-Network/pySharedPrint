# Shared Print examples

Custom application looks for new files in particular folders an S3 bucket and interacts with the API for shared print data based on the data in the delimited file

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

### Step 4: Use npm to install dependencies needed to deploy code
Download node and npm and use the `install` command to read the dependencies JSON file 

```bash
$ npm install
```

### Step 5: Run local tests

```
python -m pytest
```

### Step 6: AWS Setup

1. Install AWS Command line tools
- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
I recommend using pip.
2. Create an AWS user in IAM console. Give it appropriate permissions. Copy the key and secret for this user to use in the CLI. 
3. Configure the command line tools - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

- Make sure you add 
-- key/secret
-- region
    
### Step 7: Create an S3 Bucket for the files
1. Use the AWS Console to create a bucket. Note your bucket name!!!
2. Create folder collection_analysis/
3. Add a sample csv file named holdingsByOCLCNumber.csv with data to check for holdings
4.Add a sample csv file named retainedholdingsByOCLCNumber.csv with data to check for retained holdings


### Step 8: Test application
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

## Installing in AWS Lambda

1. Download and setup the application, see Installing locally
2. Deploy the code using serverless

```bash
$ serverless deploy
```
