import boto3
import json

import yt_dlp
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from functions import sqs, utils

queue_url = "https://sqs.us-east-1.amazonaws.com/654654599343/hlb-yt-dlp-QueueEC2-0H6PML5o97qd"

temp = True

if temp:
    youtube_video = 'https://www.youtube.com/watch?v=I7-hxTbpscU'

    sqs.publish(queue_url, youtube_video)

url = json.loads(sqs.receive_message(queue_url=queue_url))

if url:
    print(url)
    video_id = url.split('=')[1]
    # utils.download(json.loads(url), '/media/')
else:
    print('No messages.')