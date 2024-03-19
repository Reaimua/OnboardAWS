import json
import pandas as pd
import boto3

def lambda_handler(event, context):
    # Extract bucket name and object key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Check if the uploaded file matches the desired prefix
    if key.startswith('NewUserTemplate'):
        # Process the uploaded Excel file
        excel_file = f"s3://{bucket}/{key}"
        newUsers, newEmails = UserVerification(excel_file)
        print("New Users:", newUsers)
        print("New Emails:", newEmails)
    else:
        print(f"Ignoring file upload with key: {key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda execution completed')
    }

def UserVerification(excel_file):
    # Read Excel file from S3
    data = pd.read_excel(excel_file)

    # Initialize IAM client
    iam_client = boto3.client('iam')

    # Get existing IAM usernames
    response = iam_client.list_users()
    iam_usernames = [user['UserName'] for user in response['Users']]

    newUsers = []
    newEmails = []

    # Parse data from Excel file
    for index, row in data.iterrows():
        first_name = row['First Name']
        last_name = row['Last Name']
        department = row['Department']
        position =  row['Position']
        username = row['Username']
        email = row['Email']
        employeeType = row['Employee Type']

        # Modify usernames for type of employee
        if employeeType == "Vendor":
            username = 'ven-' + username
        elif employeeType == "Temporary":
            username = 't-' + username

        # Check if username already exists in IAM
        if username in iam_usernames:
            print(f"User: '{username}' already exists in IAM. Skipping.")
        else:
            print(f"User: '{username}' is new.")
            newUsers.append(username)
            newEmails.append(email)

    return newUsers, newEmails


