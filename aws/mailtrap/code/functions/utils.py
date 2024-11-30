from datetime import datetime
import random
import string
import boto3

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def year():
    return datetime.now().strftime("%Y")

def year_month():
    return datetime.now().strftime("%Y-%m")

def year_month_day():
    return datetime.now().strftime("%Y-%m-%d")

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

def list_bucket(bucket, prefix):
    files = []
    client = boto3.client('s3')
    prefix = f'cdn/{prefix}/'
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    for content in response.get('Contents', []):
        files.append(content['Key'])

    return files

def publish(topic, subject, message):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn=topic,
        Message=message,
        Subject=subject
    )
    return response
