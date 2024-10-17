import boto3

client = boto3.client('dynamodb')

def put_initial_archive_item():
    previous = [
        '2024-09-15-newsletter',
        '2024-09-21-newsletter',
        '2024-09-28-newsletter',
        '2024-10-06-newsletter',
        '2024-10-13-newsletter',
    ]

    for item in previous:
        print(item)

put_initial_archive_item()
