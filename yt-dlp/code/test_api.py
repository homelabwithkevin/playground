import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
base_url = f'https://{api_id}.execute-api.us-east-1.amazonaws.com/Prod?url'

video_id = '4SNThp0YiU4'
channel_id = '@MrBeast'
playlist_id = 'PLLGT0cEMIAzcgeiwgZSZ81S06WQQG4rFk'

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

def test_playlist():
    test_url = f'{base_url}=https://www.youtube.com/playlist?list={playlist_id}'
    response = requests.get(test_url)
    response_id = response.json()['playlist_info']['id']
    assert response.status_code == 200
    assert response_id == playlist_id

def urls():
    test_urls = [
        f'{base_url}=https://youtu.be/{video_id}',
        f'{base_url}=https://youtube.com/watch?={video_id}',
        f'{base_url}=https://www.youtube.com/{channel_id}',
        f'{base_url}=https://www.youtube.com/{channel_id}/videos',
        f'{base_url}=https://www.youtube.com/playlist?list={playlist_id}'
    ]
    for url in test_urls:
        print(url)

if __name__ == '__main__':
    urls()
