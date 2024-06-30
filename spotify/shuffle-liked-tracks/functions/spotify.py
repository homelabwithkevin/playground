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

def get_liked_songs(access_token, limit):
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

    x = 0
    while True:
        response = requests.get(url, headers=headers, params=params)
        response_json = json.loads(response.content)
        all_tracks.append(response_json)

        x += 1
        if x == limit:
            break

        if not response_json['next']:
            break
        else:
            url = (response_json['next'])

    return all_tracks

def create_shuffled_playlist(access_token, tracks, name, user_id, playlist_id=None):
    print(f'Creating shuffled playlist...')

    if not playlist_id:
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

def get_playlist_items(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    response_json = json.loads(response.content)

    list_tracks = []
    for item in response_json['tracks']['items']:
        list_tracks.append({"uri":item['track']['uri']})

    return list_tracks, response_json['snapshot_id'], response_json['name']

def delete_playlist_items(playlist_id, access_token):
    tracks, snapshot_id, name = get_playlist_items(playlist_id, access_token)

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        "tracks": tracks,
        "snapshot_id": snapshot_id
    }

    requests.delete(url, headers=headers, json=data)
    return playlist_id, name