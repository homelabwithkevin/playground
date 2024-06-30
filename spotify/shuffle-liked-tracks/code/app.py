import os
from functions import authorization, spotify, utils

def lambda_handler(event, context):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    print(client_id, client_secret, redirect_uri)

    url = authorization.request_user_authorization(redirect_uri, client_id, client_secret)

    if (event['queryStringParameters']) and (event['queryStringParameters']['code']):
        code = event['queryStringParameters']['code']

    res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': '*/*',
            'Set-Cookie': 'kevin=awesome'
        },
        'body': f"""
        <html>
            <title>Spotify Login</title>
            <h1>Spotify Login</h1>
            <a href="{ url }" target="_blank">Login Here</a>
            <p>Code: { code }</p>
        </html>
        """
    }

    return res