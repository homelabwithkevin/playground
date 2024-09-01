import json

from functions import utils
from views import view

def lambda_handler(event, context):
    print(event)

    code = None

    query_parameters = event['queryStringParameters']
    request_path = event['path']

    if query_parameters:
        if query_parameters.get('code'):
            code = event['queryStringParameters']['code']

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
        },
        "body": view.index()
    }
