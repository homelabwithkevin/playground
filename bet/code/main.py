import os
from dotenv import load_dotenv
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic_settings import BaseSettings
from fastapi.responses import HTMLResponse
from mangum import Mangum

import csv
import boto3

from templates import pages
from event import event

load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv('app_name')
    slogan: str = os.getenv('slogan')
    table_name: str = os.getenv('table_name')

settings = Settings()

app = FastAPI()

vote_counts = {}
vote_records = []

dynamodb = boto3.resource('dynamodb')

def save_vote_to_dynamodb(timestamp: str, event_id: str, vote: str):
    """Save a vote record to DynamoDB."""
    print(f'Saving to table')
    table = dynamodb.Table(settings.table_name)
    table.put_item(
        Item={
            'timestamp': timestamp,
            'event_id': event_id,
            'vote': vote
        }
    )

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

def get_vote_counts_from_dynamodb(event_id: int):
    """Fetch vote counts for an event from DynamoDB."""
    table = dynamodb.Table(settings.table_name)

    response = table.scan(
        FilterExpression='event_id = :event_id',
        ExpressionAttributeValues={
            ':event_id': str(event_id)
        }
    )

    votes = {'yes': 0, 'no': 0}
    for item in response.get('Items', []):
        vote_type = item.get('vote', '')
        if vote_type in votes:
            votes[vote_type] += 1

    return votes

def save_event_to_dynamodb(event_id: str, title: str, date: str):
    """Save an event record to DynamoDB."""
    print(f'Saving event {event_id} to DynamoDB')
    table = dynamodb.Table(settings.table_name)
    table.put_item(
        Item={
            'event_id': event_id,
            'event_type': 'event_record',
            'title': title,
            'date': date,
            'created_at': get_timestamp()
        }
    )

@app.get("/", response_class=HTMLResponse)
async def read_items():
    all_events = []
    with open('events.csv', newline='') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            all_events.append(
                {
                    'index': index,
                    'title': row[0],
                    'over': row[1],
                    'under': row[2],
                    'votes': get_vote_counts_from_dynamodb(index),
                }
            )

    return f"""
    <html>
        <head>
            <title>{settings.app_name} | {settings.slogan} </title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        </head>
        <body class="bg-slate-900">
            <div class="flex justify-center pt-4">
                <div>
                    <div class='text-white text-3xl'>
                        {pages.header(app_name=settings.app_name, slogan=settings.slogan)}
                    </div>
                    <div>
                        {event.events(all_events)}
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/event/{item}", response_class=HTMLResponse)
async def event_vote(item: int, vote: str):
    timestamp = get_timestamp()

    # Store individual vote record with timestamp
    vote_records.append({
        'timestamp': timestamp,
        'event_id': item,
        'vote': vote
    })

    # Save vote to DynamoDB
    save_vote_to_dynamodb(timestamp, str(item), vote)

    # Get updated vote counts from DynamoDB
    votes = get_vote_counts_from_dynamodb(item)

    # Read the event data from CSV
    with open('events.csv', newline='') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            if index == item:
                event_data = {
                    'index': index,
                    'title': row[0],
                    'over': row[1],
                    'under': row[2],
                    'votes': votes,
                }
                break

    # Generate and return the updated card HTML
    return event.generate_event_card(event_data)

@app.get("/votes/{event_id}")
async def get_votes(event_id: int):
    """Retrieve all votes for a specific event from DynamoDB."""
    table = dynamodb.Table(settings.table_name)

    response = table.scan(
        FilterExpression='event_id = :event_id',
        ExpressionAttributeValues={
            ':event_id': str(event_id)
        }
    )

    return {
        'event_id': event_id,
        'votes': response.get('Items', []),
        'total_votes': response.get('Count', 0)
    }

@app.get("/clear")
async def clear_table():
    """Clear all items from the DynamoDB table."""
    table = dynamodb.Table(settings.table_name)

    # Scan to get all items
    response = table.scan()
    items = response.get('Items', [])

    # Delete items in batches
    deleted_count = 0
    with table.batch_writer(
        overwrite_by_pkeys=['timestamp', 'event_id']
    ) as batch:
        for item in items:
            batch.delete_item(Key={'timestamp': item['timestamp'], 'event_id': item['event_id']})
            deleted_count += 1

    return {
        'message': 'Table cleared successfully',
        'deleted_count': deleted_count
    }

handler = Mangum(app, lifespan="off")