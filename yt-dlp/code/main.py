"""
    Runs Flask or Retrieves channel entries from the given URL.
"""
import yt_dlp

from flask import Flask
from functions.utils import get_channel_entries

LIMIT = 10
CHANNEL_URL = 'https://www.youtube.com/@MrBeast/videos'
# VIDEO_URL = 'https://www.youtube.com/watch?v=erLbbextvlY'

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

website()

# get_channel_entries(URL=CHANNEL_URL, LIMIT=LIMIT)
