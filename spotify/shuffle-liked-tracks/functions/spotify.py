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
        "name": f"{name}",
        "description": f"{name}",
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

def create_shuffled_playlist(access_token, tracks, name, user_id):
    print(f'Creating shuffled playlist...')

    playlist_id = create_playlist(access_token, name, user_id)
    spotify_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    headers = {
        'Authorization' : 'Bearer ' + str(access_token),
        'Content-Type' : 'application/json'
    }

    body = {
        'uris': tracks
    }

    response = requests.post(spotify_url, headers=headers, json=body)

    status_code = response.status_code

    if not status_code == 201:
        print(f'Failed to Create Shuffled Playlist: {name}')
        return False
    else:
        response_json = json.loads(response.content)
        print(response_json)
        return playlist_id