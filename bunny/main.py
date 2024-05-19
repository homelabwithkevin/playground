import requests
from datetime import datetime

from dotenv import load_dotenv
import os

api_key = os.getenv('API_KEY')
base_url = "https://ny.storage.bunnycdn.com/"

headers = {
    "accept": "application/json",
    "AccessKey": api_key
}

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def list_files():
    response = requests.get(f'{base_url}/playground', headers=headers)
    files = response.json()
    for file in files:
        file_info = {
            'Guid': file['Guid'],
            'StorageZoneName': file['StorageZoneName'],
            'Path': file['Path'],
            'ObjectName': file['ObjectName'],
            'IsDirectory': file['IsDirectory'],
            'DateCreated': file['DateCreated']
        }
        print(file_info)

def upload_file(file_path):
    headers = {
        "AccessKey": api_key,
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    with open(file_path, 'rb') as file_data:
        url = f'{base_url}/playground/test/{file_path}.{today()}.jpg'
        response = requests.put(url, headers=headers, data=file_data)

    print(response.status_code, response.text)