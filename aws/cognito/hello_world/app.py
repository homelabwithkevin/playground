import json

from functions import utils, handler
from views import view

def lambda_handler(event, context):
    print(event)

    code = None
    query_parameters = None
    cookies = None

    request_context = event['requestContext']
    method = request_context['http']['method']
    request_path = request_context['http']['path']

    # User Information
    source_ip = request_context['http']['sourceIp']
    user_agent = request_context['http']['userAgent']

    try:
        cookies = event['cookies']
        user_info = utils.get_user_info_from_cookies(cookies)
    except Exception as e:
        print(f'No cookies found: {e}')

    if method == 'POST':
        result_post = handler.post(event['body'], user_info, source_ip, user_agent)
        return result_post 

    try:
        query_parameters = event['queryStringParameters']
    except Exception as e:
        print(f'No query string parameters found: {e}')
            
    if query_parameters:
        if query_parameters.get('code'):
            code = query_parameters.get('code')

    if '/post' in request_path:
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
            },
            "body": view.post(request_path, user_info)
        }
    if '/logout' in request_path:
        return {
            "isBase64Encoded": False,
            "statusCode": 302,
            "headers": {
                "Content-Type": "text/html",
                "Location": "/",
            },
            "cookies": utils.clear_cookies(cookies),
            "body": view.logout()
        }

    if '/dashboard' in request_path:
        return {

            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html",
            },
            "body": view.dashboard(user_info)
        }

    if 'callback' in request_path:
        cookies = utils.handle_callback(code)

        return {
            "statusCode": 302,
            "headers": {
                "Content-Type": "text/html",
                "Location": "/dashboard",
            },
            "cookies": cookies,
            "body": view.callback(code)
        }

    # Index
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
        },
        "body": view.index()
    }
