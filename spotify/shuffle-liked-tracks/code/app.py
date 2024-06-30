import os
from functions import authorization, spotify, utils

def lambda_handler(event, context):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    print(client_id, client_secret, redirect_uri)