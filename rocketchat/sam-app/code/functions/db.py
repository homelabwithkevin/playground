import boto3
import os

client = boto3.client('dynamodb')
table = os.getenv('TABLE')

def put_item(item):
    client.put_item(
        TableName = table,
        Item = {
            "id": {
                "S": item['message_id']
            },
            "timestamp": {
                "S": item['timestamp']
            },
            "user_id": {
                "S": item['user_id']
            },
            "channel_name": {
                "S": item['channel_name']
            },
            "user_name": {
                "S": item['user_name']
            },
            "text": {
                "S": item['text']
            }
        }
    )
