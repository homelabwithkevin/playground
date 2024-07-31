import boto3
import json

import yt_dlp
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from functions import sqs, utils, s3

queue_url = "https://sqs.us-east-1.amazonaws.com/654654599343/hlb-yt-dlp-QueueContainer-109Cpmlivp0o"
bucket = 'hlb-yt-dlp'

temp = False

if temp:
    youtube_video = 'https://www.youtube.com/watch?v=I7-hxTbpscU'

    sqs.publish(queue_url, youtube_video)

url = sqs.receive_message(queue_url=queue_url)

if url:
    print(url)
    url = json.loads(url)
    video_id = url.split('=')[1]
    utils.download(url, '/media/')
    s3.upload_file(f'/media/{video_id}/{video_id}.mp4', bucket, f'{video_id}/{video_id}.mp4')
else:
    print('No messages.')