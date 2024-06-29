import requests
from datetime import datetime
from PIL import Image

# Setup Dotenv
from dotenv import load_dotenv
import os
load_dotenv()

# Setup Logging
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# Configurations
api_key = os.getenv('API_KEY')
folder = os.getenv('FOLDER')
storage_zone = os.getenv('STORAGE_ZONE')
base_url = "https://ny.storage.bunnycdn.com/"

headers = {
    "accept": "application/json",
    "AccessKey": api_key
}

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def list_files():
    response = requests.get(f'{base_url}/{storage_zone}', headers=headers)
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

def upload_file(file_path, file):
    headers = {
        "AccessKey": api_key,
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    with open(file_path, 'rb') as file_data:
        url = f'{base_url}/{storage_zone}/{file}'
        response = requests.put(url, headers=headers, data=file_data)

    message = response.status_code, response.text, file
    logger.info(message)

def list_files_and_upload(file_path, testing=False):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            logger.info(f'Trying to upload {file}')
            desired_picture = os.path.join(root, file)
            upload_file(desired_picture, file)

            if testing:
                break

def create_thumbnail(file_path, testing=False):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            logger.info(f'Trying to create thumbnail {file}')
            desired_picture = os.path.join(root, file)
            thumbnail_path = f'thumbnails/{file}'

            try:
                with Image.open(desired_picture) as img:
                    width, height = img.size
                    # img.thumbnail((width * .8, height * .8))
                    img.thumbnail((width * .3, height * .3))
                    img.save(thumbnail_path, 'JPEG')

                upload_file(thumbnail_path, f'eighty/{file}')
                upload_file(thumbnail_path, f'thumbnails/{file}')
            except Exception as e:
                print(e)
                pass

            if testing:
                break

create_thumbnail(folder, testing=False)
# list_files_and_upload(folder, testing=False)