from datetime import datetime
import random
import string
import boto3

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today_newsletter():
    return datetime.now().strftime("%Y-%m-%d")

def upload_file(bucket_name, file, cdn_path, content_type="image/jpeg"):
    client = boto3.client('s3')
    try:
        client.upload_file(file, bucket_name, cdn_path, ExtraArgs={'ContentType': content_type})
        print('File uploaded to S3')
    except Exception as e:
        print(f'Error uploading {file} to S3: {e}')

# https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python
def randomword(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
