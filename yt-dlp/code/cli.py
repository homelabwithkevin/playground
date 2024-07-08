import requests
import boto3

from functions import utils, db

limit = 1 * 2
channel_id = "@MrBeast"
url = f"http://127.0.0.1:5000/channel_id/{channel_id}?limit={limit}"
table = "hlb-yt-dlp-TableCD117FA1-1B6DOH7B3U9CE"

def request():
    response = requests.get(url)
    response_json = response.json()

    item = {}

    for entry in response_json['entries']:
        for key, value in enumerate(entry):
            item[value] = {
                'S': str(entry[value])
            }

        db.put_item(table, item)
        print(item)

if __name__ == "__main__":
    request()