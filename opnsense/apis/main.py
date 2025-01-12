import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("key")
secret = os.getenv("secret")

# Base URL
# https://opnsense.local/api/<module>/<controller>/<command>/[<param1>/[<param2>/...]]

print(key, secret)