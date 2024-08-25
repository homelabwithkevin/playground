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
    print(event)
    method = event['httpMethod']

    message = None

    if method == 'POST':
        message = event['body'].split('=')[1]
        if message:
            put_item(message)
            return {
                "statusCode": 200,
                "body": json.dumps(message)
            }
        else:
            return {
                "statusCode": 200,
                "body": f"No message."
            }

    elif method == 'GET':
        try:
            message = event['queryStringParameters']['message']
        except:
            pass

        if not message:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/html"
                },
                "body": f"""
                <html>
                  <script src="https://unpkg.com/htmx.org@2.0.2"></script>
                  <form hx-post="/Prod" hx-target="#test">
                    <input type="text" name="message" value="default" />
                    <button class="btn">
                      Click Me
                    </button>
                  </form>
                  <div>
                    <div id="test">
                      Initial Content
                    </div>
                </html>
                """
            }
    
        put_item(message)
    
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
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
