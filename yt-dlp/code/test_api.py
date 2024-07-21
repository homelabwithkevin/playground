
base_url = 'https://3mvh6tnzx3.execute-api.us-east-1.amazonaws.com/Prod?url'
# https://3mvh6tnzx3.execute-api.us-east-1.amazonaws.com/Prod?url=https://youtu.be/4SNThp0YiU4
# https://3mvh6tnzx3.execute-api.us-east-1.amazonaws.com/Prod?url=https://www.youtube.com/@MrBeast
# https://3mvh6tnzx3.execute-api.us-east-1.amazonaws.com/Prod?url=https://www.youtube.com/@MrBeast/videos
# https://3mvh6tnzx3.execute-api.us-east-1.amazonaws.com/Prod?url=https://youtu.be/4SNThp0YiU4

import requests


video_id = '4SNThp0YiU4'
channel_id = '@MrBeast'

def f():
    return 3


def test_share():
    test_url = f'{base_url}=https://youtu.be/{video_id}'
    response = requests.get(test_url)
    response_id = response.json()['id']
    assert response.status_code == 200
    assert response_id == video_id