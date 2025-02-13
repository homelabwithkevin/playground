import json

from functions import db

def lambda_handler(event, context):
    body = None
    try:
        body = json.loads(event['body'])
    except:
        body = event['body']

    print(body)

    try:
        db.put_item(body)
    except Exception as e:
        print(f'Failed to save to database: {e}')
        print(f'Body: {body}')

    channel_name = body['channel_name']
    user_name = body['user_name']
    text = body['text']
    message_id = body['message_id']

    return {
        "statusCode": 200,
        "body": f"Confirmed: {message_id}!",
    }
