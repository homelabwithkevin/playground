import boto3
import json


client = boto3.client('sqs', region_name='us-east-1')

def publish(queue, message):
    client.send_message(
        QueueUrl=queue,
        MessageBody=json.dumps(message)
    )

def delete_message(queue_url, receipt_handle):
    client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    ) 

def receive_message(queue_url):
    response = client.receive_message(
        QueueUrl=queue_url,
        MessageSystemAttributeNames=["All"],
        MaxNumberOfMessages=1,
    )

    if 'Messages' in response:
        for message in response['Messages']:
            receipt_handle = message['ReceiptHandle']
            body = message['Body']
            delete_message(queue_url, receipt_handle)
            return body

    return None