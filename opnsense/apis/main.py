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

def status():
    url = f'{service_url}/status'
    response = requests.get(url, auth=HTTPBasicAuth(key, secret), verify=False)
    return json.loads(response.content)

haproxy_status = status()['status']
print(haproxy_status)