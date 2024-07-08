import boto3
import json

def publish(queue, message):
    client = boto3.client('sqs')

    client.send_message(
        QueueUrl=queue,
        MessageBody=json.dumps(message)
    )