import json
import os
import boto3
from datetime import datetime

topic = os.environ['TOPIC']

def today():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def publish(topic, message=None, subject=None):
    print(f'Publishing to {topic}')

    client = boto3.client('sns')
    topic_message = 'Motion detected'
    topic_subject = f'MotionEye - {today()}'

    if message:
        topic_message = message

    response = client.publish(
        TopicArn = topic,
        Message = topic_message,
        Subject = topic_subject
    )

def lambda_handler(event, context):
    publish(topic)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
