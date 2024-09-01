import json

from functions import utils

def lambda_handler(event, context):
    print(event)

    code = None

    query_parameters = event['queryStringParameters']

    if query_parameters:
        if query_parameters.get('code'):
            code = event['queryStringParameters']['code']

    return utils.handle_login(query_parameters, code)
