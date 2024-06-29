import os
from dotenv import load_dotenv
from flask import Flask, request
from functions import authorization

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

    return f"""
    <h1>Spotify Tokens</h1>
    <p>Access token: {access_token}</p>
    <p>Refresh token: {refresh_token}</p>
    """

app.run(port=8888)