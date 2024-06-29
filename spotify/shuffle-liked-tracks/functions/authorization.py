from urllib.parse import urlencode

from functions.utils import generate_random_string

def request_user_authorization(redirect_uri, client_id, client_secret):
    permissions =[
        'user-library-read',
        'user-read-email'
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