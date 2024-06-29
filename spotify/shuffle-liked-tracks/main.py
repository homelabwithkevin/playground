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
def hello_world():
    return f"<a href={url}>{url}</a>"

@app.route("/callback")
def callback():
    code = request.args.get('code')
    access_token, refresh_token = authorization.request_access_token(client_id, client_secret, code)

    user_profile = spotify.get_user_profile(access_token)
    liked_songs = spotify.get_liked_songs(access_token)
    list_liked_songs = utils.handle_liked_songs(liked_songs)

    print(list_liked_songs)

    response = make_response(render_template('profile.html',
                                            access_token=access_token,
                                            refresh_token=refresh_token,
                                            user_profile=user_profile,
                                            liked_songs=list_liked_songs
                                            ))

    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)

    return response

@app.route("/profile")
def profile():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    if access_token:
        user_profile = spotify.get_user_profile(access_token)

        response = make_response(render_template('profile.html', access_token=access_token, refresh_token=refresh_token, user_profile=user_profile))
        response.set_cookie('user_id', user_profile['id'])
        return response
    else:
        return """Could not get access token."""

@app.route('/playlist', methods=['POST'])
def playlist():
    name = request.form['name']
    spotify.create_playlist(request.cookies.get('access_token'), name, request.cookies.get('user_id'))
    return redirect(url_for('profile'))

app.run(port=8888)