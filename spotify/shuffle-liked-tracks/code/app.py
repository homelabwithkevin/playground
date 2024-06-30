import os
from functions import authorization, spotify, utils

def lambda_handler(event, context):
    print(event)

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

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

            access_token, refresh_token = authorization.request_access_token(client_id, client_secret, code, redirect_uri)

            # Set some cookies
            res['headers']['Set-Cookie'] = f'access_token={access_token}'

            # Set Redirect
            res['headers']['Location'] = 'profile' 
            res['statusCode'] = 302

            res['body'] = """
            <html>
                Code redirect
            </html>
            """
    elif path == '/profile':
        # Get the cookies.
        cookies = event['headers']['Cookie']
        cookies_split = cookies.split(';')
        for c in cookies_split:
            key, value = c.split('=')
            if key == 'access_token':
                access_token = value

        user_profile = spotify.get_user_profile(access_token)

        res['body'] = f"""
        <html>
            <title>Profile</title>
            <h1>Profile</h1>
            <p>Welcome { user_profile['display_name'] } </p>
            <img src="{ user_profile['images'][1]['url'] }"/>
            <p><a href="/hello">Home</a></p>
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