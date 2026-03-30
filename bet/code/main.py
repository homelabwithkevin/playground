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
    grouped_events = {}
    with open('events.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for index, row in enumerate(reader):
            project = row[0]
            if project not in grouped_events:
                grouped_events[project] = []
            grouped_events[project].append(
                {
                    'index': index,
                    'title': row[1],
                    'over': row[2],
                    'under': row[3],
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
            <div class="flex justify-center pt-4 px-2 sm:px-0">
                <div class="w-full max-w-7xl">
                    <div class='text-white text-3xl'>
                        {pages.header(app_name=settings.app_name, slogan=settings.slogan)}
                    </div>
                    <div>
                        {event.events(grouped_events)}
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
        next(reader)  # Skip header row
        for index, row in enumerate(reader):
            if index == item:
                event_data = {
                    'index': index,
                    'title': row[1],
                    'over': row[2],
                    'under': row[3],
                    'votes': votes,
                }
                break

    # Generate and return the updated card HTML
    return event.generate_event_card(event_data)

@app.get("/clear", response_class=HTMLResponse)
async def clear_table():
    """Clear all items from the DynamoDB table."""
    table = dynamodb.Table(settings.table_name)

    # Get table key schema
    key_names = [key['AttributeName'] for key in table.key_schema]

    deleted_count = 0
    response = table.scan()

    with table.batch_writer() as batch:
        # Delete first page of items
        for item in response.get('Items', []):
            key = {k: item[k] for k in key_names}
            batch.delete_item(Key=key)
            deleted_count += 1

        # Handle pagination for remaining items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            for item in response.get('Items', []):
                key = {k: item[k] for k in key_names}
                batch.delete_item(Key=key)
                deleted_count += 1

    return f"""
    <html>
        <head>
            <title>Clear Votes</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body class="bg-slate-900">
            <div class="flex justify-center pt-4 px-2 sm:px-0">
                <div class="w-full max-w-7xl">
                    <div class="bg-slate-700 p-6 rounded-xl text-white">
                        <h1 class="text-2xl font-bold mb-4">Table Cleared</h1>
                        <p class="text-lg mb-4">Successfully deleted <span class="font-bold text-green-400">{deleted_count}</span> items from the table.</p>
                        <a href="/" class="text-blue-400 hover:text-blue-300">← Back to all bets</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/{project}", response_class=HTMLResponse)
async def view_project(project: str):
    project_events = []
    with open('events.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for index, row in enumerate(reader):
            if row[0] == project:
                project_events.append(
                    {
                        'index': index,
                        'title': row[1],
                        'over': row[2],
                        'under': row[3],
                        'votes': get_vote_counts_from_dynamodb(index),
                    }
                )

    return f"""
    <html>
        <head>
            <title>{settings.app_name} | {project}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        </head>
        <body class="bg-slate-900">
            <div class="flex justify-center pt-4 px-2 sm:px-0">
                <div class="w-full max-w-7xl">
                    <div class='text-white text-3xl mb-6'>
                        {pages.header(app_name=settings.app_name, slogan=project)}
                    </div>
                    <a href="/" class="text-blue-400 hover:text-blue-300 mb-4 inline-block">← Back to all bets</a>
                    <div>
                        {event.events(project_events)}
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

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

handler = Mangum(app, lifespan="off")