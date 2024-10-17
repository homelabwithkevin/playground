import boto3

from functions import db

client = boto3.client('dynamodb')
table = "hlb-mailtrap-archive-develop"

def initial_archive():
    previous = [
        '2024-09-15-newsletter',
        '2024-09-21-newsletter',
        '2024-09-28-newsletter',
        '2024-10-06-newsletter',
        '2024-10-13-newsletter',
    ]

    for item in previous:
        db.put_initial_archive_item(table, item)
