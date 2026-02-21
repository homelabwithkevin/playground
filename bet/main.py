import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic_settings import BaseSettings
from fastapi.responses import HTMLResponse
import csv

from templates import pages
from event import event

load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv('app_name')
    slogan: str = os.getenv('slogan')

settings = Settings()

app = FastAPI()


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    all_events = []
    with open('events.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            all_events.append(
                {
                    'title': row[0],
                    'over': row[1],
                    'under': row[2],
                }
            )

    return f"""
    <html>
        <head>
            <title>{settings.app_name} | {settings.slogan} </title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <div class="flex justify-center pt-4">
            <div>
                <div>
                    {pages.header(app_name=settings.app_name)}
                </div>
                <div>
                    {event.events(all_events)}
                </div>
            </div>
        </div>
    </html>
    """