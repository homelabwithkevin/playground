import requests

base_url = 'https://[redacted].execute-api.us-east-1.amazonaws.com/Prod/?message=hello'

def get():
    response = requests.get(base_url)
    
    print(response.text)


def post():
    response = requests.post(base_url, json={'message': 'hello'})
    
    print(response.status_code)
    
    print(response.text)
