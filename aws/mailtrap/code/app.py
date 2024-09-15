import boto3
import random
import string
import json
import os

bucket = os.environ['BUCKET_NAME']
client = boto3.client('s3')

# https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python
def randomword(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def copy_object(key):
    extension = key.split('.')[-1]
    folder = key.split('/')[1]
    if '.jpg' in folder:
        new_key = f'cdn/{randomword()}.{extension}'
    else:
        new_key = f'cdn/{folder}/{randomword()}.{extension}'

    print(f'Copying {key} to {new_key}')
    client.copy_object(Bucket=bucket, CopySource=f'{bucket}/{key}', Key=new_key)
    print(f'Successful copy')

def lambda_handler(event, context):
    for record in event['Records']:
        s3_key = record['s3']['object']['key']
        copy_object(s3_key)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

