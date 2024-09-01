import json

from functions import utils, handler
from views import view

def lambda_handler(event, context):
    print(event)

    code = None

    query_parameters = event['queryStringParameters']
    method = event['httpMethod']
    request_path = event['path']
    request_headers = event['headers'].get('Cookie')

    if method == 'POST':
        access_token = utils.get_access_token(request_headers)
        sub, email_verified, email, username = utils.get_user_info(access_token)
        print(access_token)
        result_post = handler.post(event['body'], username)
        return result_post 

    if query_parameters:
        if query_parameters.get('code'):
            code = event['queryStringParameters']['code']
            print(code)

    if '/logout' in request_path:
        cookies = utils.clear_cookies(request_headers)

        return {
            "statusCode": 301,
            "headers": {
                "Content-Type": "text/html",
                "Location": "/Prod",
            },
            "multiValueHeaders": {
                "Set-Cookie": cookies,
            },
            "body": view.logout()
        }

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
