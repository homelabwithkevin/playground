import requests

def get_user_profile(access_token):
    url = 'https://api.spotify.com/v1/me'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json()

def create_playlist(access_token, name, user_id):
    url = f"https://api.spotify.com/v1/users/me/playlists"

    data = {
        "name": f"{name}-hlb",
        "description": f"{name}-hlb",
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    print(url)
    response = requests.post(url, json=data, headers=headers)

    print(response.text)