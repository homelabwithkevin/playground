import json
import boto3
import os
import base64

from functions import utils

table = os.environ["TABLE"]

client = boto3.client('dynamodb')

def post(body=None, user_info=None, source_ip=None, user_agent=None):
    decoded_body = base64.b64decode(body).decode('utf-8')
    data = decoded_body.split('=')[1]

    body = f"""
    <div>
        Success: {data}
    </div>
    """

    try:
        client.put_item(
            TableName=table,
            Item={
                'id': {
                    'S': str(utils.today())
                },
                'utc_now': {
                    'S': str(utils.utc_now())
                },
                'user_id': {
                    'S': user_info.get('sub')
                },
                'source_ip': {
                    'S': source_ip
                },
                'user_agent': {
                    'S': user_agent
                },
                'message': {
                    'S': data
                },
            }
        )
    except Exception as e:
        print(f'Failed to put item: {e}')
        body = f"""
        <div>
            Failed to save to database
        </div>
        """

    return_data = {
        "statusCode": 200,                
        "headers": {
            "Content-Type": "application/html",
        },
        "body": body
    }

    return return_data
