import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_URL = os.getenv('API_URL')

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
                'Content-Type': '*/*',
        },
        'body': f"""
        <script src="https://unpkg.com/htmx.org@2.0.1"></script>
        <html>
            <body>
                <h1>hlb-yt-dlp</h1>

                <form id="form" hx-encoding="application/x-www-form-urlencoded" hx-post="https://{API_URL}.execute-api.us-east-1.amazonaws.com/Prod" hx-target="#search-results">
                    <label for="data">Data:</label><br>
                    <input type="text" id="data" name="data" size="40"><br>
                    <button class="btn-primary">
                    Click Me
                    </button>
                </form> 

                <div>Results</div>
                <div id="search-results">
                </div>
            </body>
        </html>
        """
    }