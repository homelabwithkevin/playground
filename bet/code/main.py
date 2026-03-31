import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import base64
import urllib.parse
import string
import random

from fastapi import FastAPI, Form, Request
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
    votes_table_name: str = os.getenv('votes_table_name')
    bets_table_name: str = os.getenv('bets_table_name')
    allowed_clear_ips: str = os.getenv('allowed_clear_ips', '127.0.0.1,localhost')

settings = Settings()

app = FastAPI()

vote_counts = {}
vote_records = []

dynamodb = boto3.resource('dynamodb')

def save_vote_to_dynamodb(timestamp: str, event_id: str, vote: str):
    """Save a vote record to DynamoDB."""
    print(f'Saving to table')
    table = dynamodb.Table(settings.votes_table_name)
    table.put_item(
        Item={
            'timestamp': timestamp,
            'event_id': event_id,
            'vote': vote
        }
    )

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

def encode_event_id(event_id: str) -> str:
    """Encode event_id for safe use in HTML selectors and attributes."""
    return base64.urlsafe_b64encode(event_id.encode()).decode().rstrip('=')

def decode_event_id(encoded_id: str) -> str:
    """Decode event_id from HTML-safe format back to original."""
    # Add padding back if needed
    padding = 4 - (len(encoded_id) % 4)
    if padding != 4:
        encoded_id += '=' * padding
    return base64.urlsafe_b64decode(encoded_id.encode()).decode()

def generate_project_id(length: int = 8) -> str:
    """Generate a random project ID with uppercase, lowercase, and numbers."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_vote_counts_from_dynamodb(event_id: int):
    """Fetch vote counts for an event from DynamoDB."""
    table = dynamodb.Table(settings.votes_table_name)

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

def save_bet_to_dynamodb(event_id: str, project: str, title: str):
    """Save a bet to the bets table in DynamoDB."""
    print(f'Saving bet {event_id} to bets table')
    table = dynamodb.Table(settings.bets_table_name)
    table.put_item(
        Item={
            'event_id': event_id,
            'project': project,
            'title': title,
            'created_at': get_timestamp()
        }
    )

def get_all_bets_from_dynamodb():
    """Fetch all bets from DynamoDB."""
    table = dynamodb.Table(settings.bets_table_name)
    response = table.scan()
    return response.get('Items', [])

def get_bets_by_project_from_dynamodb(project: str):
    """Fetch bets for a specific project from DynamoDB."""
    table = dynamodb.Table(settings.bets_table_name)
    response = table.query(
        IndexName='ProjectIndex',
        KeyConditionExpression='#proj = :project',
        ExpressionAttributeNames={
            '#proj': 'project'
        },
        ExpressionAttributeValues={
            ':project': project
        }
    )
    return response.get('Items', [])

def get_bet_by_event_id(event_id: str):
    """Fetch a bet by event_id from DynamoDB using scan."""
    table = dynamodb.Table(settings.bets_table_name)
    response = table.scan(
        FilterExpression='event_id = :event_id',
        ExpressionAttributeValues={
            ':event_id': event_id
        }
    )
    items = response.get('Items', [])
    return items[0] if items else {}

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    grouped_events = {}
    bets = get_all_bets_from_dynamodb()

    # Check if user's IP is allowed to create projects
    client_ip = request.client.host
    allowed_ips = [ip.strip() for ip in settings.allowed_clear_ips.split(',')]
    can_create_project = client_ip in allowed_ips

    for index, bet in enumerate(bets):
        project = bet.get('project')
        event_id = bet.get('event_id')
        if project not in grouped_events:
            grouped_events[project] = []
        grouped_events[project].append(
            {
                'index': encode_event_id(event_id),
                'title': bet.get('title'),
                'over': '',
                'under': '',
                'votes': get_vote_counts_from_dynamodb(event_id),
                'status': bet.get('status'),
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
                    {'<div class="bg-slate-700 p-6 rounded-xl mb-8"><h2 class="text-white text-2xl font-bold mb-2">Create New Stake</h2><p class="text-gray-300 text-sm mb-6">Start a new stake and get a unique stake ID.</p><form method="post" action="/create-project" class="space-y-4"><div><label class="block text-white text-sm font-semibold mb-2">Stake Name</label><input type="text" name="project_name" required class="w-full bg-slate-600 text-white px-4 py-2 rounded border border-slate-500 focus:outline-none focus:border-blue-400" placeholder="My awesome stake"></div><button type="submit" class="w-full bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2 rounded transition-all active:scale-95">Create Stake</button></form></div>' if can_create_project else ''}
                    <div class="bg-slate-700 p-6 rounded-xl mb-8">
                        <h2 class="text-white text-2xl font-bold mb-2">Go to Stake</h2>
                        <p class="text-gray-300 text-sm mb-6">Enter a stake name to view all bets and votes for that stake.</p>
                        <form method="post" action="/go-to-project" class="space-y-4">
                            <div>
                                <label class="block text-white text-sm font-semibold mb-2">Stake Name</label>
                                <input type="text" name="project" required class="w-full bg-slate-600 text-white px-4 py-2 rounded border border-slate-500 focus:outline-none focus:border-blue-400" placeholder="Stake name">
                            </div>
                            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded transition-all active:scale-95">Go to Stake</button>
                        </form>
                    </div>
                    <div class="bg-slate-700 p-6 rounded-xl">
                        <h2 class="text-white text-2xl font-bold mb-2">Add New Bet</h2>
                        <p class="text-gray-300 text-sm mb-6">Create a new bet by specifying a stake and describing what you're betting on. Then share it with others to vote.</p>
                        <form method="post" action="/add-bet" class="space-y-4">
                            <div>
                                <label class="block text-white text-sm font-semibold mb-2">Stake</label>
                                <input type="text" name="project" required class="w-full bg-slate-600 text-white px-4 py-2 rounded border border-slate-500 focus:outline-none focus:border-blue-400" placeholder="Stake name">
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

@app.post("/create-project", response_class=HTMLResponse)
async def create_project(project_name: str = Form()):
    """Create a new stake and display its unique ID."""
    project_id = generate_project_id()
    return f"""
    <html>
        <head>
            <title>Stake Created</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body class="bg-slate-900">
            <div class="flex justify-center pt-4 px-2 sm:px-0">
                <div class="w-full max-w-4xl">
                    <a href="/" class="text-blue-400 hover:text-blue-300 mb-4 inline-block">← Back to home</a>
                    <div class="bg-slate-700 p-8 rounded-xl text-white space-y-6">
                        <h1 class="text-4xl font-bold text-green-400">Stake Created!</h1>
                        <div class="bg-slate-600 p-6 rounded-lg space-y-4">
                            <div>
                                <p class="text-sm text-gray-300 mb-2">Stake Name</p>
                                <p class="text-2xl font-bold text-white">{project_name}</p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-300 mb-2">Stake ID</p>
                                <p class="text-2xl font-mono font-bold text-blue-400">{project_id}</p>
                                <p class="text-xs text-gray-400 mt-2">Use this ID to share your stake or reference it later</p>
                            </div>
                        </div>
                        <button onclick="copyProjectID()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded transition-all active:scale-95">
                            Copy Stake ID
                        </button>
                        <a href="/" class="block w-full bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2 rounded text-center transition-all active:scale-95">Start Adding Bets</a>
                    </div>
                </div>
            </div>
            <script>
                function copyProjectID() {{
                    const projectID = "{project_id}";
                    navigator.clipboard.writeText(projectID).then(() => {{
                        const button = event.target;
                        const originalText = button.innerHTML;
                        button.innerHTML = 'Copied!';
                        button.classList.add('bg-green-600');
                        button.classList.remove('bg-blue-600', 'hover:bg-blue-500');
                        setTimeout(() => {{
                            button.innerHTML = originalText;
                            button.classList.remove('bg-green-600');
                            button.classList.add('bg-blue-600', 'hover:bg-blue-500');
                        }}, 2000);
                    }});
                }}
            </script>
        </body>
    </html>
    """

@app.post("/go-to-project")
async def go_to_project(project: str = Form()):
    """Redirect to a specific project page."""
    return RedirectResponse(url=f"/{project}", status_code=303)

@app.post("/add-bet")
async def add_bet(project: str = Form(), title: str = Form()):
    """Add a new bet to DynamoDB."""
    event_id = get_timestamp()  # Use timestamp as unique event_id
    save_bet_to_dynamodb(event_id, project, title)
    return RedirectResponse(url=f"/{project}", status_code=303)

@app.post("/event/{item}", response_class=HTMLResponse)
async def event_vote(item: str, vote: str):
    try:
        # Decode the event_id from the encoded format
        event_id = decode_event_id(item)
        timestamp = get_timestamp()

        # Store individual vote record with timestamp
        vote_records.append({
            'timestamp': timestamp,
            'event_id': event_id,
            'vote': vote
        })

        # Save vote to DynamoDB
        save_vote_to_dynamodb(timestamp, event_id, vote)

        # Get updated vote counts from DynamoDB
        votes = get_vote_counts_from_dynamodb(event_id)

        # Read the event data from DynamoDB
        bet = get_bet_by_event_id(event_id)

        event_data = {
            'index': item,  # Use the encoded ID for the HTML
            'title': bet.get('title', ''),
            'over': '',
            'under': '',
            'votes': votes,
            'status': bet.get('status'),
        }

        # Generate and return the updated card HTML
        return event.generate_event_card(event_data)
    except Exception as e:
        return f"""
        <div class="bg-red-900 p-4 rounded text-white">
            <h3 class="font-bold mb-2">Error voting:</h3>
            <p class="text-sm font-mono">{str(e)}</p>
            <p class="text-xs mt-2">Item: {item}, Vote: {vote}</p>
        </div>
        """

@app.get("/clear", response_class=HTMLResponse)
async def clear_table(request: Request):
    """Clear all items from the DynamoDB table."""
    # Check IP address
    client_ip = request.client.host
    allowed_ips = [ip.strip() for ip in settings.allowed_clear_ips.split(',')]

    if client_ip not in allowed_ips:
        return f"""
        <html>
            <head>
                <title>Access Denied</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            </head>
            <body class="bg-slate-900">
                <div class="flex justify-center pt-4 px-2 sm:px-0">
                    <div class="w-full max-w-4xl">
                        <a href="/" class="text-blue-400 hover:text-blue-300 mb-4 inline-block">← Back to home</a>
                        <div class="bg-slate-700 p-8 rounded-xl text-white space-y-6">
                            <h1 class="text-4xl font-bold text-red-400">Whoa There!</h1>
                            <div class="space-y-4 text-lg">
                                <p>We appreciate your enthusiasm for clearing things, but your IP address <span class="font-bold text-red-300">({client_ip})</span> isn't on the VIP list.</p>
                                <p>This endpoint is restricted to authorized addresses only. Think of it as the pit boss watching over our high-stakes betting floor—except instead of card tables, we're protecting votes, and instead of a suit, the pit boss is IP filtering.</p>
                                <div class="bg-slate-600 p-4 rounded space-y-2">
                                    <h3 class="font-semibold text-blue-300">Why is this restricted?</h3>
                                    <ul class="list-disc list-inside space-y-1 text-sm">
                                        <li>We actually like our data</li>
                                        <li>Accidentally clearing votes would ruin everyone's progress</li>
                                        <li>Security theater is still theater, but it feels good</li>
                                    </ul>
                                </div>
                                <p class="text-sm text-gray-400">If you believe this is an error, you'll need to either:</p>
                                <ul class="list-disc list-inside space-y-1 text-sm">
                                    <li>Configure <span class="font-mono bg-slate-600 px-2 py-1 rounded">allowed_clear_ips</span> to include your IP</li>
                                    <li>Change your IP (kidding, don't do this)</li>
                                    <li>Accept that the votes are eternal</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """

    table = dynamodb.Table(settings.votes_table_name)

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
    return pages.about(app_name=settings.app_name, slogan=settings.slogan)

@app.get("/{project}", response_class=HTMLResponse)
async def view_project(project: str):
    project_events = []
    bets = get_bets_by_project_from_dynamodb(project)

    for bet in bets:
        event_id = bet.get('event_id')
        project_events.append(
            {
                'index': encode_event_id(event_id),
                'title': bet.get('title'),
                'over': '',
                'under': '',
                'votes': get_vote_counts_from_dynamodb(event_id),
                'status': bet.get('status'),
            }
        )

    if not project_events:
        return f"""
        <html>
            <head>
                <title>{settings.app_name} | {project}</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            </head>
            <body class="bg-slate-900">
                <div class="flex justify-center pt-4 px-2 sm:px-0">
                    <div class="w-full max-w-4xl">
                        <a href="/" class="text-blue-400 hover:text-blue-300 mb-4 inline-block">← Back to home</a>
                        <div class="bg-slate-700 p-8 rounded-xl text-white space-y-6">
                            <h1 class="text-4xl font-bold">Stake Not Found</h1>
                            <div class="space-y-4 text-lg">
                                <p>We searched high and low for "<span class="font-bold text-blue-400">{project}</span>" but couldn't find it.</p>
                                <p>This could mean:</p>
                                <ul class="list-disc list-inside space-y-2 ml-2">
                                    <li>The bet was never made (unlikely, everyone forgets eventually)</li>
                                    <li>You spelled it wrong (we've all been there)</li>
                                    <li>Someone deleted it out of embarrassment (very relatable)</li>
                                    <li>It exists in an alternate timeline where better decisions were made</li>
                                </ul>
                                <p class="pt-4">Try going back and creating a new bet, or checking the spelling. We won't judge you for trying again.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """

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
                    <div class="flex gap-4 mb-4">
                        <a href="/" class="text-blue-400 hover:text-blue-300 inline-block">← Back to home</a>
                        <button onclick="copyToClipboard(this)" class="text-blue-400 hover:text-blue-300 inline-flex items-center gap-2 whitespace-nowrap">
                            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                            </svg>
                            Share Stake
                        </button>
                    </div>
                    <script>
                        function copyToClipboard(button) {{
                            const url = window.location.href;
                            navigator.clipboard.writeText(url).then(() => {{
                                const originalText = button.innerHTML;
                                button.innerHTML = '<svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Copied!';
                                button.classList.add('text-green-400');
                                setTimeout(() => {{
                                    button.innerHTML = originalText;
                                    button.classList.remove('text-green-400');
                                }}, 2000);
                            }});
                        }}
                    </script>
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
    table = dynamodb.Table(settings.votes_table_name)

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