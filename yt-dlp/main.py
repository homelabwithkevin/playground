"""
    Runs Flask or Retrieves channel entries from the given URL.
"""
import yt_dlp

from flask import Flask
from functions.utils import parse_channel_entries

LIMIT = 100
CHANNEL_URL = 'https://www.youtube.com/@MrBeast/videos'
# VIDEO_URL = 'https://www.youtube.com/watch?v=erLbbextvlY'

def get_channel_entries(URL, LIMIT):
    """
    Retrieves channel entries from the given URL.

    Args:
        URL (str): The URL of the channel.
        limit (int): The maximum number of entries to retrieve.

    Returns:
        dict: A dictionary containing the channel entries.

    """
    ydl_opts = {
            'outtmpl': '%(id)s/%(id)s.%(ext)s',
            'playlistend': LIMIT,
            'ignoreerrors': True,
            'format': 'bestvideo*+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cachedir': False,
            'extract_flat': True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)

        # for key, value in enumerate(info):
        #     print(f'{value} = info["{value}"]')

        channel = True

        if channel:
            entries = info['entries']
            uploader_id = info['uploader_id']

            return parse_channel_entries(uploader_id=uploader_id, entries=entries, parse_video=False)

        return info

def website():
    """
    Run a Flask web application that returns channel entries.

    Returns:
        Flask Website
    """
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return get_channel_entries(URL=CHANNEL_URL, LIMIT=LIMIT)

    app.run()

# website()

get_channel_entries(URL=CHANNEL_URL, LIMIT=LIMIT)
