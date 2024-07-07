import requests
import boto3

limit = 1 * 10
channel_id = "@MrBeast"
url = f"http://127.0.0.1:5000/channel_id/{channel_id}?limit={limit}"
table = "hlb-yt-dlp-TableCD117FA1-1B6DOH7B3U9CE"

def put_item(item):
    client = boto3.client('dynamodb', region_name='us-east-1')

    response = client.put_item(
        TableName=table,
        Item=item
    )

    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'Failed to put_item')

def request():
    response = requests.get(url)
    response_json = response.json()

    item = {}

    for entry in response_json['entries']:
        for key, value in enumerate(entry):
            item[value] = {
                'S': str(entry[value])
            }

        put_item(item)
        print(item)

if __name__ == "__main__":
    request()