import os
import boto3

from functions import utils

table = os.environ["TABLE"]
client = boto3.client('dynamodb')

def put_item(first_name, email):
    response = client.put_item(
        TableName=table,
        Item={
            'id': {
                'S': str(utils.today())
            },
            'first_name': {
                'S': first_name
            },
            'email': {
                'S': email
            },
        }
    )
