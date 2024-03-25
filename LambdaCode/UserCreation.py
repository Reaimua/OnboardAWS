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
        newUsers, newEmails, userAssignments = UserVerification (excel_file)
        
        # Initialize AWS Lambda client
        lambda_client = boto3.client("lambda", region_name="us-west-1")
        
        # Payload for the other Lambda functions
        user_assignment_payload = {
            "newUsers": newUsers,
            "userAssignments": userAssignments
        }
        welcome_email_payload = {
            "newUsers": newUsers,
            "newEmails": newEmails
        }
        
        # Invoke UserAssignment Lambda function
        user_assignment_resp = lambda_client.invoke(
            FunctionName="UserAssignment",
            InvocationType="Event",  # Asynchronous invocation
            Payload=json.dumps(user_assignment_payload)
        )
        
        # Invoke WelcomeEmail Lambda function
        welcome_email_resp = lambda_client.invoke(
            FunctionName="WelcomeEmail",
            InvocationType="Event",  # Asynchronous invocation
            Payload=json.dumps(welcome_email_payload)
        )
        
        print("Invoked UserAssignment and WelcomeEmail Lambda functions.")
    else:
        print(f"Ignoring file upload with key: {key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda execution completed')
    }
  
    # Extract bucket name and object key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Check if the uploaded file matches the desired prefix
    if key.startswith('NewUserTemplate'):
        # Process the uploaded Excel file
        excel_file = f"s3://{bucket}xx/{key}"
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
    userAssignments = []
    

def UserVerification(excel_file):
    # Read Excel file from S3
    data = pd.read_excel(excel_file)

    newUsers = []
    newEmails = []
    userAssignments = []

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
        elif employeeType == "Temporary" or "Student":
            username = 't-' + username

        newUsers.append(username)
        newEmails.append(email)
        
        userAssignments.append({
            'username': username,
            'department': department,
            'position': position,
            'employee_type': employeeType
        })
        
    return newUsers, newEmails, userAssignments