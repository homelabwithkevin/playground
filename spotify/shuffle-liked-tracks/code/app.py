import os
from functions import authorization, spotify, utils

def lambda_handler(event, context):
    print(event)

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    print(client_id, client_secret, redirect_uri)

    path = event['path']

    code = None

    res = {
        'headers': {
            'statusCode': 200,
            'Content-Type': '*/*',
            'Set-Cookie': 'kevin=awesome'
        },
    }

    if path == '/callback':
        if (event['queryStringParameters']) and (event['queryStringParameters']['code']):
            code = event['queryStringParameters']['code']
            res['headers']['Location'] = 'profile'
            res['headers']['Set-Cookie'] = 'cats=awesome'
            res['statusCode'] = 302
            res['body'] = """
            <html>
                Code redirect
            </html>
            """
    elif path == '/profile':
        res['body'] = f"""
        <html>
            <title>Profile</title>
            <h1>Profile</h1>
            <p>Profile</p>
        </html>
        """
    else:
        url = authorization.request_user_authorization(redirect_uri, client_id, client_secret)

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
            </html>
            """
        }
    return res