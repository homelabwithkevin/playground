import os
from dotenv import load_dotenv
from flask import Flask, request, make_response, render_template, redirect, url_for
from functions import authorization, spotify, utils

# Load environment variables from .env file
load_dotenv()

# Accessing variables
redirect_uri = os.getenv('redirect_uri')
client_id = os.getenv('client_id')
client_secret = os.getenv('secret_id')

url = authorization.request_user_authorization(redirect_uri, client_id, client_secret)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', url=url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    access_token, refresh_token = authorization.request_access_token(client_id, client_secret, code)

    user_profile = spotify.get_user_profile(access_token)

    response = make_response(render_template('profile.html',
                                            access_token=access_token,
                                            refresh_token=refresh_token,
                                            user_profile=user_profile
                                            ))

    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)

    return response

@app.route("/profile")
def profile():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    playlist_id = request.cookies.get('playlist_id')

    if access_token:
        user_profile = spotify.get_user_profile(access_token)

        response = make_response(render_template('profile.html', access_token=access_token, refresh_token=refresh_token, user_profile=user_profile, playlist_id=playlist_id))
        response.set_cookie('user_id', user_profile['id'])
        return response
    else:
        return """Could not get access token."""

@app.route('/playlist', methods=['POST'])
def playlist():
    access_token = request.cookies.get('access_token')
    user_id = request.cookies.get('user_id')

    # Get Liked Songs
    liked_songs = spotify.get_liked_songs(access_token=access_token, limit=100)

    # Shuffle Liked Songs
    list_liked_songs = utils.handle_liked_songs(liked_songs)
    shuffled_songs = utils.shuffle_songs(list_liked_songs)

    if 'playlist_id' in request.form:
        playlist_id = request.form['playlist_id']

        # I am not sure if you need to delete the playlist items, but I'll do it anyways.
        playlist_id, name = spotify.delete_playlist_items(playlist_id, access_token)
    else:
        name = request.form['name']
        playlist_id = None

    # Create Shuffled Playlist
    result_playlist_id = spotify.create_shuffled_playlist(access_token=access_token,
                                    tracks=shuffled_songs,
                                    name=f"{name} - HLB",
                                    user_id=user_id,
                                    playlist_id=playlist_id
                                    )

    response = make_response(render_template('playlist.html', playlist_id=result_playlist_id, playlist_name=name))
    response.set_cookie('playlist_id', result_playlist_id)
    return response

app.run(port=8888)