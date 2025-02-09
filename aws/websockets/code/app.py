import json
import boto3
import os

from dotenv import load_dotenv

load_dotenv()

ws_server = os.getenv('WS_SERVER')
client = boto3.client('apigatewaymanagementapi', endpoint_url=ws_server)

def send_message(connection_id, message):
    client.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(message)
    )

def lambda_handler(event, context):
    print(event)
    body = event['body']

    connection_id = event['requestContext']['connectionId']
    send_message(connection_id, f'Thanks for your message {body}')

    return {
        "statusCode": 200,
        "body": {
            "message": "hello world",
        },
    }
