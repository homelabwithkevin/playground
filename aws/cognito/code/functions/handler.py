import json
import boto3
import os
import base64

from functions import utils

table = os.environ["TABLE"]

client = boto3.client('dynamodb')

def post(body=None, user_info=None, source_ip=None, user_agent=None):
    decoded_body = base64.b64decode(body).decode('utf-8')

    # form_type=message&message=example
    # Not the best way to parse this, but it works for now
    try:
        split_decoded = decoded_body.split('&')

        for s in split_decoded:
            key, value = s.split('=')

            if key == 'form_type':
                form_type = value

            if key == 'message':
                data = value

    except:
        pass


    body = f"""
    <div>
        Success: {decoded_body}
    </div>
    """

    try:
        client.put_item(
            TableName=table,
            Item={
                'id': {
                    'S': utils.random_string(10)
                },
                'date': {
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
                'form_type': {
                    'S': form_type
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
