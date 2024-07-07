"""
    Runs Flask app to get YouTube channel entries and video information.
"""
from flask import Flask, request
from functions.utils import get_channel_entries, parse_video_information

LIMIT = 1
CHANNEL_URL = 'https://www.youtube.com/@MrBeast/videos'
# VIDEO_URL = 'https://www.youtube.com/watch?v=erLbbextvlY'

app = Flask(__name__)

@app.route("/")
def index():
    return get_channel_entries(URL=CHANNEL_URL, LIMIT=LIMIT)

@app.route("/channel_id/<id>")
def channel_id(id):
    limit = request.args.get('limit')

    if not limit:
        limit = LIMIT

    URL = f'https://www.youtube.com/{id}/videos'
    return get_channel_entries(URL=URL, LIMIT=limit)

@app.route("/video_id/<id>")
def video_id(id):
    URL = f'https://www.youtube.com/watch?v={id}'
    return parse_video_information(URL=URL, VIDEO=True)

@app.route("/upload_date/<id>")
def upload_date(id):
    return id

if __name__ == "__main__":
    app.run()