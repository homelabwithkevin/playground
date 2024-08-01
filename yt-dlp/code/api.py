import boto3
import json
import os
from urllib.parse import unquote

from functions import utils, db, utils

table_name = os.getenv('TABLE_NAME')
table_channels = os.getenv('TABLE_CHANNELS')

def lambda_handler(event, context):
    print(event)

    http_method = event['httpMethod']

    # Defaults
    url = 'https://www.youtube.com/@MrBeast/videos'
    limit = 1
    _type = 'channel'
    results = None

    if http_method == 'POST':
        body = event['body']
        split_body = body.split('data=')
        data = unquote(split_body[1])
        print(data)

        if 'youtube.com' in data:
            data_url = data
            url, _type = utils.handle_url(url=data_url)
        else:
            return {
                "statusCode": 200,
                "body": "Invalid URL."
            }

    elif http_method == 'GET':
        if 'queryStringParameters' in event:
            if 'url' in event['queryStringParameters']:
                query_parameter_url = event['queryStringParameters']['url']
                url, _type = utils.handle_url(url=query_parameter_url)

    if _type == 'playlist':
        results = utils.parse_playlist(URL=url)

    elif _type == 'video':
        results = utils.parse_video_information(URL=url, VIDEO=True)
        db.put_item(
            table_name,
            utils.make_string_item(data=results, video=True)
        )

    elif _type == 'channel':
        results = utils.get_channel_entries(URL=url, LIMIT=limit)
        db.put_item(
            table_name,
            utils.make_string_item(data=results['entries'][0], video=True)
        )

        db.put_item(
            table_channels,
            utils.make_string_item(data=results['info'], channel=True)
        )

    if not results:
        return {
            "statusCode": 500,
            "body": json.dumps({'error': 'No results found'})
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(results)
        }