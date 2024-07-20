import boto3
import json

from functions import utils

def lambda_handler(event, context):
    print(event)

    url = 'https://www.youtube.com/@MrBeast/videos'
    limit = 1
    results = utils.get_channel_entries(URL=url, LIMIT=limit)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }