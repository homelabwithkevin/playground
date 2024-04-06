import logging
import json

from functions.utils import get_channel_entries

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LIMIT = 10
CHANNEL_URL = 'https://www.youtube.com/@MrBeast/videos'
# VIDEO_URL = 'https://www.youtube.com/watch?v=erLbbextvlY'

def lambda_handler(event, context):
    entries = get_channel_entries(URL=CHANNEL_URL, LIMIT=LIMIT)
    return {
        'statusCode': 200,
        'body': json.dumps(entries)
    }