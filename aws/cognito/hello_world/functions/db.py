import os
import boto3

table = os.environ["TABLE"]
client = boto3.client('dynamodb')

def get_item(id, user_info):
    response = client.get_item(
        TableName=table,
        Key={
            'id': {
                'S': id
            },
            'user_id': {
                'S': user_info.get('sub')
            },
        }
    )
    if 'Item' in response:
        return response['Item']

    return None
