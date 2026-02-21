import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic_settings import BaseSettings
from fastapi.responses import HTMLResponse

from templates import pages

load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv('app_name')
    slogan: str = os.getenv('slogan')

settings = Settings()

app = FastAPI()


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return f"""
    <html>
        <head>
            <title>{settings.app_name} | {settings.slogan} </title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <div class="flex justify-center pt-4">
            <div>
                {pages.header(app_name=settings.app_name)}
            </div>
        </div>
    </html>
    """