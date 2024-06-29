import os
from dotenv import load_dotenv
from flask import Flask
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

app.run(port=8888)