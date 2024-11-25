import json
import os
import boto3

topic = os.environ['TOPIC']

def publish(topic, message=None):
    print(f'Publishing to {topic}')

    client = boto3.client('sns')
    topic_message = 'Motion detected'

    if message:
        topic_message = message

    response = client.publish(
        TopicArn = topic,
        Message = topic_message
    )

def lambda_handler(event, context):
    publish(topic, message)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
