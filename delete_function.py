import os
import boto3

# Get DynamoDB table name from environment variable
import os
import boto3
from decouple import config


def delete_handler(event, context):
    # Configure boto3 to use access keys
    aws_access_key_id = config('aws_access_key_id')
    aws_secret_access_key = config('aws_secret_access_key')
    aws_region = config('aws_region')
    table_name =config('DynamoDBTableName')
    # Create a DynamoDB client with the provided access keys and region
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Validate presence of 'id' attribute in the event
    if 'token' not in event :
        return {'statusCode': 401, 'body': 'Missing authorisation attributes.'}
    else:
        if event['token']!="allowme":
            return {'statusCode': 401, 'body': 'You are not authorized to perform this tasl.'}
    if 'id' not in event:
        return {'statusCode': 400, 'body': 'Missing required attribute: id'}

    # Get the id of the item to delete
    item_id = event['id']

    try:
        # Delete the item from DynamoDB table
        dynamodb.delete_item(
            TableName=table_name,
            Key={'id': {'S': item_id}}
        )
    except Exception as e:
        return {'statusCode': 500, 'body': f'Failed to delete item: {str(e)}'}

    return {'statusCode': 200, 'body': 'Item deleted successfully'}
