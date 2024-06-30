from urllib.parse import urlencode
from functions.utils import generate_random_string

import requests
from requests.auth import HTTPBasicAuth
import json

def request_user_authorization(redirect_uri, client_id, client_secret):
    permissions =[
        'user-library-read',
        'user-read-email',
        'playlist-modify-public',
        'playlist-modify-private',
        'playlist-read-private'
    ]

    scope = ' '.join(permissions)

    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': generate_random_string(16)
    }

    url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
    print(f'Navigate to this URL in your browser: \n{url}')
    return url

def request_access_token(client_id, client_secret, code, redirect_uri):
    url = 'https://accounts.spotify.com/api/token'

    basic_auth = HTTPBasicAuth(client_id, client_secret)

    data = {
        'code': code,
        'grant_type' : 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, auth=basic_auth, data=data)
    response_json = json.loads(response.content)

    access_token = response_json['access_token']
    refresh_token = response_json['refresh_token']

    return access_token, refresh_token