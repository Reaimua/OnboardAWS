import json
import pandas as pd
import boto3

def lambda_handler(event, context):
    # Extract data from the event
    newUsers, newEmails, userAssignments = event['newUsers'], event['newEmails'], event['userAssignments']
    
    # Iterate over each user assignment
    for assignment in userAssignments:
        # Extract relevant data
        username = assignment['username']
        department = assignment['department']
        position = assignment['position']
        employee_type = assignment['employee_type']
        
        # Create user in group with role
        create_user_in_group_with_role(username, department, position, employee_type)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda execution completed')
    }

def create_user_in_group_with_role(user_name, department, position, employee_type):
    iam_client = boto3.client('iam')

    # Create the IAM user
    iam_client.create_user(UserName=user_name)
    # Add User to their Department 
    iam_client.add_user_to_group(UserName=user_name, GroupName=department)
    # Add a Managerial or Employee Role to User
    if position == "Manager":
        iam_client.attach_user_to_policy(UserName=user_name, PolicyArn=f'arn:aws:iam::aws:policy/{position}')
    else: 
        iam_client.attach_user_to_policy(UserName=user_name, PolicyArn=f'arn:aws:iam::aws:policy/{position}')