import os
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("key")
secret = os.getenv("secret")
base_url = os.getenv("base_url")

# Base URL
# https://opnsense.local/api/<module>/<controller>/<command>/[<param1>/[<param2>/...]]

haproxy_url = f'{base_url}/haproxy/service/status'

def status():
    response = requests.get(haproxy_url, auth=HTTPBasicAuth(key, secret), verify=False)
    return json.loads(response.content)


print(status())