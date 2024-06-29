from dotenv import load_dotenv
import os

from functions import authorization

# Load environment variables from .env file
load_dotenv()

# Accessing variables
client_id = os.getenv('client_id')
client_secret = os.getenv('secret_id')

authorization.request_user_authorization(client_id, client_secret)