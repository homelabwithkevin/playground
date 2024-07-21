import boto3
import json

from functions import utils

def lambda_handler(event, context):
    print(event)

    # Defaults
    url = 'https://www.youtube.com/@MrBeast/videos'
    limit = 1
    _type = 'channel'
    results = None

    if 'queryStringParameters' in event:
        if 'url' in event['queryStringParameters']:
            query_parameter_url = event['queryStringParameters']['url']
            url, _type = utils.handle_url(url=query_parameter_url)

        print(url, _type)

        if _type == 'video':
            results = utils.parse_video_information(URL=url, VIDEO=True)

        elif _type == 'channel':
            results = utils.get_channel_entries(URL=url, LIMIT=limit)


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