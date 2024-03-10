import os
import boto3
from decouple import config

# Get DynamoDB table name from environment variable


def create_handler(event, context):
    # Configure boto3 to use access keys
    aws_access_key_id = config('aws_access_key_id')
    aws_secret_access_key = config('aws_secret_access_key')
    aws_region = config('aws_region')
    table_name =config('table_name')
    # Create a DynamoDB client with the provided access keys and region
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Validate presence of 'id' and 'Weather'
    if 'token' not in event :
        return {'statusCode': 401, 'body': 'Missing authorisation attributes.'}
    else:
        if event['token']!="allowme":
            return {'statusCode': 401, 'body': 'You are not authorized to perform this tasl.'}

        
    
    if 'id' not in event or 'Weather' not in event:
        return {'statusCode': 400, 'body': 'Missing required attributes.'}
    
    # Validate only 'id' and 'Weather' are present
    if len(event) > 2:
        return {'statusCode': 400, 'body': 'Extra attributes are not allowed.'}

    # Insert data into DynamoDB table
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'id': {'S': event['id']},
            'Weather': {'S': event['Weather']}
        }
    )

    return {'statusCode': 200, 'body': 'Successfully inserted data!'}