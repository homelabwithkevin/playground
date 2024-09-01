import boto3
import requests
import os
import json

from views import view

cognito = boto3.client("cognito-idp")

user_pool_id = os.environ["USER_POOL_ID"]
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
redirect_uri = os.environ["REDIRECT_URI"]
domain = os.environ["DOMAIN"]

def create_cognito_hosted_uri():
    return f"https://{domain}.auth.us-east-1.amazoncognito.com/oauth2/authorize?client_id={client_id}&response_type=code&scope=email+openid&redirect_uri={redirect_uri}"

def load_tailwind():
    return """
    <script src="https://cdn.tailwindcss.com"></script>
    """
#https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
def cognito_login(code):
    response = requests.post(
        f"https://{domain}.auth.us-east-1.amazoncognito.com/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )

    if response.status_code == 200:
        response_json = json.loads(response.content)
        id_token = response_json.get("id_token")
        access_token = response_json.get("access_token")
        refresh_token = response_json.get("refresh_token")
        return id_token, access_token, refresh_token

    return None

def get_user_info(access_token):
    response = requests.get(
        f"https://{domain}.auth.us-east-1.amazoncognito.com/oauth2/userInfo",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code == 200:
        response_json = json.loads(response.content)
        sub = response_json.get("sub")
        email_verified = response_json.get("email_verified")
        email = response_json.get("email")
        username = response_json.get("username")
        return sub, email_verified, email, username

    return None

def handle_callback(code):
    id_token, access_token, refresh_token = None, None, None
    id_token, access_token, refresh_token = cognito_login(code)
    sub, email_verified, email, username = get_user_info(access_token)

    cookies = [
        f"id_token={id_token}",
        f"access_token={access_token}",
        f"refresh_token={refresh_token}",
        f"email={email}",
        f"username={username}",
    ]
    return cookies

def parse_request_headers(request_headers):
    headers = request_headers.split(";")
    new_headers = {}
    for header in headers:
        key, value = header.split("=")
        new_headers[key] = value

    return new_headers


def handle_login(query_parameters, code):
    headers = {
        "Content-Type": "text/html",
    }

    cognito_response = None
    # https://repost.aws/questions/QU4VpxEkw_Q6yQotN5JhkBEA/lambda-function-url-not-returning-multiple-cookies
    cookies = [None]

    id_token, access_token, refresh_token = None, None, None

    if code:
        cognito_response = cognito_login(code)
        if cognito_response:
            id_token = cognito_response["id_token"]
            access_token = cognito_response["access_token"]
            refresh_token = cognito_response["refresh_token"]
            cookies = [
                    f"id_token={id_token}",
                    f"access_token={access_token}",
                    f"refresh_token={refresh_token}",
            ]

    return {
        "statusCode": 200,
        "headers": headers,
        "multiValueHeaders": {
            "Set-Cookie": cookies,
        },
        "body": f"""
        <html>
            {view.navigation()}
            <p>{query_parameters}</p>
            {view.example()}
            <p>Code: {code}</p>
            <p>
                <p>Cognito</p>
                <p>ID Token: {id_token}</p>
                <p>Access Token: {access_token}</p>
                <p>Refresh Token: {refresh_token}</p>
            </p>
        </html>

        """
    }
