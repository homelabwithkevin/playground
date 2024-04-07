import requests
import os
import json
import time

# Set your credentials
# export MUX_TOKEN_ID=
# export MUX_TOKEN_SECRET=

base_url = "https://api.mux.com/video/v1/assets"

MUX_TOKEN_ID = os.getenv('MUX_TOKEN_ID')
MUX_TOKEN_SECRET = os.getenv('MUX_TOKEN_SECRET')

headers = {
    "Content-Type" : "application/json"
}

data =  {
    "input": "https://muxed.s3.amazonaws.com/leds.mp4",
    "playback_policy": "public",
    "encoding_tier": "baseline"
}

def upload(data):
    response = requests.post(
        base_url,
        headers=headers,
        json=data,
        auth=(MUX_TOKEN_ID, MUX_TOKEN_SECRET)
    )

    response_data = json.loads(response.content)['data']
    _id = response_data['id']
    playback_ids = response_data['playback_ids']
    print(f'Asset ID: {_id}')   
    print(f'Playback ID: {playback_ids}')
    return _id

def get_status(asset_id):
    status = None
    print(f'Asset Id: {asset_id}')
    while True:
        response = requests.get(
            f'{base_url}/{asset_id}',
            headers=headers,
            auth=(MUX_TOKEN_ID, MUX_TOKEN_SECRET)
        )
        response_data = json.loads(response.content)['data']
        status = response_data['status']
        print(f'Status: {status}')
        if status == 'ready':
            break
        time.sleep(5)

def list_asssets():
    list_of_assets = []

    response = requests.get(
        f'{base_url}',
        headers=headers,
        auth=(MUX_TOKEN_ID, MUX_TOKEN_SECRET)
    )

    response_data = json.loads(response.content)['data']

    for data in response_data:
        _id = data['id']
        duration = data['duration']
        # print(f'Asset ID: {_id} Duration: {duration}')
        list_of_assets.append(_id)

    return list_of_assets

def delete_asset(asset_id):
    url = f"{base_url}/{asset_id}"
    response = requests.delete(
        url,
        headers=headers,
        auth=(MUX_TOKEN_ID, MUX_TOKEN_SECRET)
    )
    if response.status_code == 204:
        print(f"Asset {asset_id} deleted successfully")
    else:
        print(f"Failed to delete asset {asset_id}. Error: {response.content}")