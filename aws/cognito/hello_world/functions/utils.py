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

#https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
def cognito_login(code):
    response = requests.post(
        f"https://homelabwithkevin-develop.auth.us-east-1.amazoncognito.com/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )
    print(response.status_code)
    print(response.content)

    if response.status_code == 200:
        response_json = json.loads(response.content)
        print(response_json) 
        return response_json 

    return None

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
