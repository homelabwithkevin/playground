import os
from dotenv import load_dotenv
from flask import Flask, request, make_response, render_template, redirect, url_for
from functions import authorization, spotify

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

    response = make_response(render_template('profile.html', access_token=access_token, refresh_token=refresh_token))

    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)

    return redirect(url_for('profile'))

@app.route("/profile")
def profile():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    user_profile = spotify.get_user_profile(access_token)

    response = make_response(render_template('profile.html', access_token=access_token, refresh_token=refresh_token, user_profile=user_profile))
    return response

app.run(port=8888)