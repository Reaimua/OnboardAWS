import boto3

def lambda_handler(event, context):
    # Extract username, email, and name from the event
    username = event['username']
    email = event['email']
    name = event['name']
    
    # Construct message
    message = f"Hello {name}! Your assigned username is: {username},\n\nReach out to your system administrator for your password."
    
    # Publish message to SNS topic
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn='YOUR_SNS_TOPIC_ARN',  # Replace with your SNS topic ARN
        Message=message,
        Subject='Account Successfully Created!',  # Adjust subject as needed
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email
            }
        }
    )
    
    # Log response
    print(response)