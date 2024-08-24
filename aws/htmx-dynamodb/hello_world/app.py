import boto3
import json
import os
from datetime import datetime

table_name = os.environ['TABLE_NAME']

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def put_item(message):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'id': today(),
            'message': message
        }
    )

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'POST':
        return {
            "statusCode": 200,
            "body": json.dumps(event)
        }

    elif method == 'GET':
        message = event['queryStringParameters']['message']
    
        if not message:
            return {
                "statusCode": 400,
                "body": "Bad Request"
            }
    
        put_item(message)
    
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": f"""
            <html>
                <body>
                    <h1>Message: {message}</h1>
                    <h2>Time: {today()}</h1>
                </body>
            </html>
            """
        }
