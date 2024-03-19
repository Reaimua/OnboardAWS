import json
import pandas as pd
import boto3

def lambda_handler(event, context):
    # Extract bucket name and object key from the S3 event
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda execution completed')
    }

def create_user_in_group_with_role (user_name, department, role_name, employee_type):
    iam_client = boto3.client('iam')

    #Create the IAM user
    iam_client.create_user(UserName=user_name)
    #Add User to their Department 
    iam_client.add_user_to_group(UserName= user_name, GroupName= department)
    #Add a Managerial or Employee Role to User
    if role_name == "Manager":
        iam_client.attach_user_to_policy(UserName=user_name, PolicyArn= f'arn:aws:iam::aws:policy/{role_name}')
    else: 
        iam_client.attach_user_to_policy(UserName=user_name, PolicyArn= f'arn:aws:iam::aws:policy/{role_name}')

