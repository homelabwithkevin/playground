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
    video = False
    channel = False

    # Handle URL query parameter
    try:
        url = request.args.get('url')

        # https://youtu.be/4SNThp0YiU4
        if 'youtu.be' in url:
            video = True
            id = url.split('/')[3]
            id = id.split('?')[0]
            url = f'https://www.youtube.com/watch?v={id}'

        # https://www.youtube.com/watch?v=4SNThp0YiU4
        elif 'watch' in url:
            video = True
            id = url.split('=')[1]
            url = f'https://www.youtube.com/watch?v={id}'

        # https://www.youtube.com/@MrBeast
        # https://www.youtube.com/@MrBeast/videos
        else:
            channel = True
            if '/videos' not in url:
                url = url + '/videos'
            print(f'default: {url}')
    except:
        pass

    if video:
        return parse_video_information(URL=url, VIDEO=True)
    elif channel:
        return get_channel_entries(URL=url, LIMIT=LIMIT)
    else:
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