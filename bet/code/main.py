import os
from dotenv import load_dotenv
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic_settings import BaseSettings
from fastapi.responses import HTMLResponse
from mangum import Mangum

import csv

from templates import pages
from event import event

load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv('app_name')
    slogan: str = os.getenv('slogan')

settings = Settings()

app = FastAPI()

vote_counts = {}
vote_records = []

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

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
                    'votes': vote_counts.get(index, {'yes': 0, 'no': 0}),
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
                        {pages.header(app_name=settings.app_name)}
                    </div>
                    <div>
                        {event.events(all_events)}
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/event/{item}")
async def event_vote(item: int, vote: str):
    timestamp = get_timestamp()

    # Store individual vote record with timestamp
    vote_records.append({
        'timestamp': timestamp,
        'event_id': item,
        'vote': vote
    })

    # Update vote counts for display
    if item not in vote_counts:
        vote_counts[item] = {}
    if vote not in vote_counts[item]:
        vote_counts[item][vote] = 0
    vote_counts[item][vote] += 1
    print(vote_counts)
    return vote_counts[item]

handler = Mangum(app, lifespan="off")