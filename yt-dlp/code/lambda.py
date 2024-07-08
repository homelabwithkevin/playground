import os
from functions import db, sqs

table = "hlb-yt-dlp-TableCD117FA1-1B6DOH7B3U9CE"
queue = os.getenv("QUEUE_URL")

def handler(event, context):
    items = db.scan(table)
    for item in items:
        print(item)
        sqs.publish(queue, item)
        break

if __name__ == "__main__":
    handler(None, None)