import json
from functions import utils, db
import os

table = os.getenv('TABLE_NAME')

def handler(event, context):
    print(event)

    for record in event['Records']:
        message = json.loads(record['body'])
        id = message['id']['S']

    URL = f'https://www.youtube.com/watch?v={id}'
    video_info = utils.parse_video_information(URL=URL, VIDEO=True)

    parsed_item = utils.make_string_item(data=video_info, video=True)
    db.put_item(table, parsed_item)