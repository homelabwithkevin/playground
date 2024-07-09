import json
from functions import utils

def handler(event, context):
    print(event)
    for record in event['Records']:
        message = json.loads(record['body'])
        id = message['id']['S']
        id = "erLbbextvlY"

    URL = f'https://www.youtube.com/watch?v={id}'
    result = utils.parse_video_information(URL=URL, VIDEO=True)
    print(result)