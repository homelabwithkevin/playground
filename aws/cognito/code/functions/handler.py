import json
import boto3
import os
import base64

from functions import utils

table = os.environ["TABLE"]

client = boto3.client('dynamodb')

def post(body=None, user_info=None, source_ip=None, user_agent=None):
    decoded_body = base64.b64decode(body).decode('utf-8')
    password = None
    encryption = False

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

            if key == 'password':
                password = value
    except:
        pass

    if user_info.get('password'):
        password = user_info.get('password')

    if password:
        encryption = True

    if form_type == 'password':
        body = f"""
        <div>
            <p>Successfully Set Password</p>
            <p>Success: {data}</p>
        </div>
        """
    else:
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
                    'password': {
                        'S': str(password)
                    },
                    'encryption': {
                        'S': str(encryption)
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
    
    if form_type == 'password':
        return_data['cookies'] = [ f"password={data}" ]

    return return_data
