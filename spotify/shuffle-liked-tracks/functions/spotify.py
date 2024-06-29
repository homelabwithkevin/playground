import requests
import json

def get_user_profile(access_token):
    url = 'https://api.spotify.com/v1/me'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json()

def create_playlist(access_token, name, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    data = {
        "name": f"{name}-hlb",
        "description": f"{name}-hlb",
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    response_json = response.json()
    playlist_id = response_json['id']
    return playlist_id

def get_liked_songs(access_token):
    all_tracks = []
    url = 'https://api.spotify.com/v1/me/tracks'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {'limit' : 50, 'offset': 0}

    response = requests.get(url, headers=headers, params=params)

    response_json = json.loads(response.content)

    all_tracks.append(response_json)

    if not response_json['next']:
        return
    else:
        url = (response_json['next'])

    while True:
        break
        response = requests.get(url, headers=headers, params=params)
        response_json = json.loads(response.content)
        all_tracks.append(response_json)

        if not response_json['next']:
            break
        else:
            url = (response_json['next'])

    return all_tracks