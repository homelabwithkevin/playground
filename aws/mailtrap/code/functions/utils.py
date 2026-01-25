from datetime import datetime
import random
import string
import boto3
import os
import pandas as pd

from functions import db

# table_vote = os.environ["TABLE_VOTE"]
# table_archive = os.environ["TABLE_ARCHIVE"]
# cdn_url = os.environ["CLOUDFRONT_URL"]

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

def today_file_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

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

def get_monthly_votes(limit=3):
    archived_items = db.get_archive_items(table_archive)

    totals = []

    # Iterate through Archived Items
    # For Each Archived Item, Get Votes for all pictures
    # Return Pandas Dataframe with all the data

    for archived_item in archived_items:
        newsletter = archived_item.split('-newsletter')[0]
        votes = db.get_votes(table_vote, newsletter)
        _totals = {}

        x = 0
        for key, file in enumerate(votes):
            x += 1
            if x > limit:
                break
            file_path = f'{cdn_url}/cdn/{newsletter}-newsletter/{file}'

            _totals = {
                'newsletter': newsletter,
                'rank': key,
                'file': file,
                'file_path': file_path,
                'votes': votes[file]
            }

            totals.append(_totals)

    return totals

def save_dataframe(dataframe, filename):
    """
        Helper function to save dataframe to a file.
    """
    try:
        name = f'{filename}-{today_file_timestamp()}.csv'
        dataframe.to_csv(name, index=0)
        print(f'Saved dataframe to {name}')
    except Exception as e:
        print(f'Failed to save dataframe: {e}')