import json

from functions import utils
from views import view

def lambda_handler(event, context):
    print(event)

    code = None

    query_parameters = event['queryStringParameters']
    request_path = event['path']
    request_headers = event['headers'].get('Cookie')

    if query_parameters:
        if query_parameters.get('code'):
            code = event['queryStringParameters']['code']
            print(code)

    if '/dashboard' in request_path:
        return {

            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
            },
            "body": view.dashboard(request_headers)
        }

    if 'callback' in request_path:
        cookies = utils.handle_callback(code)

        return {
            "statusCode": 301,
            "headers": {
                "Content-Type": "text/html",
                "Location": "/Prod/dashboard",
            },
            "multiValueHeaders": {
                "Set-Cookie": cookies,
            },
            "body": view.callback(code)
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
        },
        "body": view.index()
    }
