import os
from functions import db, sqs, batch

table = os.getenv('TABLE_NAME')
queue = os.getenv("QUEUE_URL_CONTAINER")

def handler(event, context):
    items = db.scan(table)
    for item in items:
        print(item)
        url = item['url']['S']
        sqs.publish(queue, url)
        batch.create()
        break

if __name__ == "__main__":
    handler(None, None)