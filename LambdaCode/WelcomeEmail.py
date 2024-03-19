import boto3

def lambda_handler(event, context):
    # Extract username and email from the event
    username = event['username']
    email = event['email']
    
    # Construct message
    message = f"Hello {username},\n\nThis is a test email sent from AWS Lambda and SNS."
    
    # Publish message to SNS topic
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn='YOUR_SNS_TOPIC_ARN',
        Message=message,
        Subject='Test Email from AWS Lambda',
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email
            }
        }
    )
    
    # Log response
    print(response)