import os
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("key")
secret = os.getenv("secret")
base_url = os.getenv("base_url")
headers = {'Content-Type':'application/json'}

# Base URL
# https://opnsense.local/api/<module>/<controller>/<command>/[<param1>/[<param2>/...]]

service_url = f'{base_url}/haproxy/service'
settings_url = f'{base_url}/haproxy/settings'

def service(action):
    url = f'{service_url}/{action}'

    if action == 'status' or action == 'configtest':
        response = requests.get(url, auth=HTTPBasicAuth(key, secret), verify=False)
    else:
        response = requests.post(url, auth=HTTPBasicAuth(key, secret), verify=False)

    response_json = json.loads(response.content)
    print(response_json)
    return response_json

def backend(action):
    if action == 'search':
        url = f'{settings_url}/searchBackends'
        response = requests.get(url, auth=HTTPBasicAuth(key, secret), verify=False)
        response_json = json.loads(response.content)
        return response_json['rows']

def server(action='search', name=None, description=None, address=None, port=None):
    if action == 'search':
        url = f'{settings_url}/searchServers'
        response = requests.get(url, auth=HTTPBasicAuth(key, secret), verify=False)
        response_json = json.loads(response.content)
        return response_json['rows']

    if action == 'add':
        url = f'{settings_url}/addServer'
        content = {
            "server":{
                "enabled": "1",
                "name": name,
                "description": description,
                "type": "static",
                "address": address,
                "port": port,
                "mode": "active",
                "multiplexer_protocol": "unspecified",
                "ssl": "0",
                "sslSNI": "",
                "sslVerify": "0",
            }
        }
        response = requests.post(url, auth=HTTPBasicAuth(key, secret), verify=False,headers=headers, data=json.dumps(content))
        response_json = json.loads(response.content)
        print(response_json)
        return response_json

server('add', name='kevin', description='kevin',address='127.0.0.1', port='69')