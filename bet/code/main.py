import os
from dotenv import load_dotenv
from datetime import datetime, timezone

from fastapi import FastAPI, Form
from pydantic_settings import BaseSettings
from fastapi.responses import HTMLResponse, RedirectResponse
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
                    <div class='text-white text-3xl mb-8'>
                        {pages.header(app_name=settings.app_name, slogan=settings.slogan)}
                    </div>
                    <div class="bg-slate-700 p-6 rounded-xl mb-8">
                        <h2 class="text-white text-2xl font-bold mb-6">Go to Project</h2>
                        <form method="post" action="/go-to-project" class="space-y-4">
                            <div>
                                <label class="block text-white text-sm font-semibold mb-2">Project Name</label>
                                <input type="text" name="project" required class="w-full bg-slate-600 text-white px-4 py-2 rounded border border-slate-500 focus:outline-none focus:border-blue-400" placeholder="Project name">
                            </div>
                            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded transition-all active:scale-95">Go to Project</button>
                        </form>
                    </div>
                    <div class="bg-slate-700 p-6 rounded-xl">
                        <h2 class="text-white text-2xl font-bold mb-6">Add New Bet</h2>
                        <form method="post" action="/add-bet" class="space-y-4">
                            <div>
                                <label class="block text-white text-sm font-semibold mb-2">Project</label>
                                <input type="text" name="project" required class="w-full bg-slate-600 text-white px-4 py-2 rounded border border-slate-500 focus:outline-none focus:border-blue-400" placeholder="Project name">
                            </div>
                            <div>
                                <label class="block text-white text-sm font-semibold mb-2">Bet Title</label>
                                <input type="text" name="title" required class="w-full bg-slate-600 text-white px-4 py-2 rounded border border-slate-500 focus:outline-none focus:border-blue-400" placeholder="Bet description">
                            </div>
                            <button type="submit" class="w-full bg-green-600 hover:bg-green-500 text-white font-semibold py-2 rounded transition-all active:scale-95">Add Bet</button>
                        </form>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/go-to-project")
async def go_to_project(project: str = Form()):
    """Redirect to a specific project page."""
    return RedirectResponse(url=f"/{project}", status_code=303)

@app.post("/add-bet")
async def add_bet(project: str = Form(), title: str = Form()):
    """Add a new bet to the events.csv file."""
    with open('events.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([project, title, "", ""])

    return RedirectResponse(url="/", status_code=303)

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

@app.get("/about", response_class=HTMLResponse)
async def about_page():
    """About page with some light satire."""
    return f"""
    <html>
        <head>
            <title>About {settings.app_name}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body class="bg-slate-900">
            <div class="flex justify-center pt-4 px-2 sm:px-0">
                <div class="w-full max-w-4xl">
                    <a href="/" class="text-blue-400 hover:text-blue-300 mb-4 inline-block">← Back to betting</a>
                    <div class="bg-slate-700 p-8 rounded-xl text-white space-y-6">
                        <h1 class="text-4xl font-bold">About {settings.app_name}</h1>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Our Mission</h2>
                            <p>We believe that the best way to make important life decisions is to gamble on them with your friends. Why have productive conversations when you can have <span class="italic">betting rounds</span>?</p>
                            <p>Our platform is designed with one core principle in mind: <span class="font-bold">democratizing disagreement through quantifiable loss</span>.</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">How We Operate</h2>
                            <p>We've streamlined the ancient art of wagering down to its purest form:</p>
                            <ol class="list-decimal list-inside space-y-2 ml-2">
                                <li>Create a bet about something that matters (or doesn't)</li>
                                <li>Convince others they're wrong</li>
                                <li>Watch votes accumulate in real-time like a stock ticker for bad decisions</li>
                                <li>Feel a sense of accomplishment regardless of the outcome</li>
                            </ol>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Why Bets?</h2>
                            <p>Traditional polling is boring. Surveys are slow. Asking people directly what they think requires effort and listening skills.</p>
                            <p>But bets? Bets cut right to the chase. They tell us not just what people think, but what they're <span class="font-bold">willing to stake on it</span>. It's the same principle as the stock market, except with lower stakes and higher confidence in incorrect predictions.</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Our Track Record</h2>
                            <p>We've successfully enabled thousands of people to document their poor judgment. Our users report a 99.7% satisfaction rate with how clearly they can see in hindsight that they were wrong.</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Data & Privacy</h2>
                            <p>We store your betting history in a database somewhere. We take your privacy very seriously—so seriously that we don't know where your data is either. What we do know is that it's probably fine.</p>
                            <p><span class="text-gray-400 text-sm">(All votes are recorded. Forever. There is no forgetting.</span>)</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Contact Us</h2>
                            <p>Have questions? Feature requests? Complaints about your poor decision-making? Unfortunately, we can't help with the last one. That's on you.</p>
                        </div>

                        <div class="mt-8 pt-6 border-t border-slate-600 text-center text-sm text-gray-400">
                            <p>{settings.app_name}: <span class="italic">"{settings.slogan}"</span></p>
                            <p class="mt-2">Making Bets Since We Could Afford the AWS Bill</p>
                        </div>
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