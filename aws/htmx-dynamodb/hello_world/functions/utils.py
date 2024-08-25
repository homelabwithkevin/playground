import boto3
import os
from datetime import datetime

table_name = os.environ["TABLE_NAME"]

def today():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def put_item(message):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item={"id": today(), "message": message})
