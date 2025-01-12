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

service_url = f'{base_url}/haproxy/service'

def service(action):
    url = f'{service_url}/{action}'

    if action == 'status' or action == 'configtest':
        response = requests.get(url, auth=HTTPBasicAuth(key, secret), verify=False)
    else:
        response = requests.post(url, auth=HTTPBasicAuth(key, secret), verify=False)

    response_json = json.loads(response.content)
    print(response_json)
    return response_json

service('status')['status']