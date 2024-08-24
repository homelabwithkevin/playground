import requests
from datetime import datetime

put_method = "put_object"
get_method = "get_object"

base_url = "https://[redacted].execute-api.us-east-1.amazonaws.com/Prod/"

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def get(file):
    get_req = requests.get(base_url + f"?object_name={file}&method={get_method}")

    get_url = get_req.text

    get_res = requests.get(get_url)

    print(get_res.text)

def put(file):
    put_req = requests.get(base_url + f"?object_name={file}&method={put_method}")

    put_url = put_req.text

    put_res = requests.put(put_url, data="testing put")

    print(put_res.status_code)

my_file = f"testing-{today()}.txt"

print(my_file)
put(my_file)
get(my_file)