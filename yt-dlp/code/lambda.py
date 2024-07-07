import os
from functions import db

table = "hlb-yt-dlp-TableCD117FA1-1B6DOH7B3U9CE"

def handler(event, context):
    items = db.scan(table)
    for item in items:
        print(item)

if __name__ == "__main__":
    handler(None, None)