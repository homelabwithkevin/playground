
base_url = 'https://3mvh6tnzx3.execute-api.us-east-1.amazonaws.com/Prod?url'

import requests

video_id = '4SNThp0YiU4'
channel_id = '@MrBeast'

def test_share():
    test_url = f'{base_url}=https://youtu.be/{video_id}'
    response = requests.get(test_url)
    response_id = response.json()['id']
    assert response.status_code == 200
    assert response_id == video_id

def test_video():
    test_url = f'{base_url}=https://youtube.com/watch?={video_id}'
    response = requests.get(test_url)
    response_id = response.json()['id']
    assert response.status_code == 200
    assert response_id == video_id

def test_channel():
    test_url = f'{base_url}=https://www.youtube.com/{channel_id}'
    response = requests.get(test_url)
    response_id = response.json()['uploader_id']
    assert response.status_code == 200
    assert response_id == channel_id

def test_channel_videos():
    test_url = f'{base_url}=https://www.youtube.com/{channel_id}/videos'
    response = requests.get(test_url)
    response_id = response.json()['uploader_id']
    assert response.status_code == 200
    assert response_id == channel_id