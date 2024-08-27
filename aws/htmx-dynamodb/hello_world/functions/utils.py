import boto3
import os
from datetime import datetime
from urllib.parse import unquote

import random

table_name = os.environ["TABLE_NAME"]

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def put_item(message):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item={"id": today(), "message": message})

def url_decode(message):
    return unquote(message)

def random_string(length=10):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))

def generate_presigned_url(method, bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(method,
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None

    print(response)
    return response
