import boto3
import json

import yt_dlp
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from functions import sqs, utils

queue_url = "https://sqs.us-east-1.amazonaws.com/654654599343/hlb-yt-dlp-QueueEC2-0H6PML5o97qd"

temp = False

if temp:
    youtube_video = 'https://youtube.com/watch?v=4SNThp0YiU4'

    sqs.publish(queue_url, youtube_video)

url = sqs.receive_message(queue_url=queue_url)

ydl_opts = {
        'outtmpl': '%(id)s/%(id)s.%(ext)s',
        'playlistend': 1,
        'ignoreerrors': True,
        'format': 'bestvideo*+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'cachedir': False,
        'extract_flat': True,
    }

if url:
    print(url)
    # utils.download(url, ydl_opts)
else:
    print('No messages.')